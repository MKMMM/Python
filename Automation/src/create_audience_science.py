#! /usr/bin/python
# coding: utf-8

import sys
import os
import csv 
import hashlib
import re
import time
import argparse
import logging
from logging.handlers import TimedRotatingFileHandler
from time import sleep 

sys.path.append('/nfs/shared/py_packages/facebook-python') # Replace this with the place you installed facebookads using pip
sys.path.append('/nfs/shared/py_packages/facebook-python') # same as above

# format the log entries
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
handler = TimedRotatingFileHandler('Audience.log',  when='midnight', backupCount=1)
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.customaudience import CustomAudience
from facebook_business.adobjects.user import User
import configparser

def create_audience(ad_account_id,audience_name, dhid):

	ad_account = AdAccount('act_'+ad_account_id)
	fields = []
	params = {
	  'name': audience_name,
	  'subtype': 'CUSTOM',
	  'options': dhid,
	  'customer_file_source': 'USER_PROVIDED_ONLY',
	  'opt_out_link': 'https://www.tesco.com/help/privacy-and-cookies/privacy-centre/tesco-and-your-data/our-commitment/'
	}
	custom_audience = ad_account.create_custom_audience(fields=fields, params=params)
	custom_audience_id = custom_audience['id']
	return custom_audience_id

def add_users(audience_file, custom_audience_id):

	# Open the CSV 
	f = open(audience_file, newline='',encoding = "ISO-8859-1")  
	reader = csv.DictReader(f, delimiter='|', fieldnames = ( "CustomerID","FIRSTNAME","LASTNAME","ADDRESS1","ADDRESS2","ADDRESS3","ADDRESS4","ADDRESS5","TOWN","COUNTY","POSTCODE","EMAIL1","MOBILE1"))

	print("\nProcessing...\n"),

	# Prepare the data in json format and split in batches of 10K
	api_calls = 0
	i = 0
	fields = []
	schema = ["EXTERN_ID","EMAIL","PHONE","FN","LN","COUNTRY","CT","ST","ZIP"]
	data = []
	gb = 'gb' 
	country_GB = hashlib.sha256(gb.encode('utf-8')).hexdigest()
	for row in reader:
		# Normalize and hash data for Facebook API
		dhid = hashlib.sha256(row['CustomerID'].encode('utf-8')).hexdigest()
		fn = hashlib.sha256(re.sub('[^A-Za-z0-9]+', '', row['FIRSTNAME']).encode('utf-8').lower()).hexdigest() if len(row['FIRSTNAME'])>0 else ''
		ln = hashlib.sha256(re.sub('[^A-Za-z0-9]+', '', row['LASTNAME']).encode('utf-8').lower()).hexdigest() if len(row['LASTNAME'])>0 else ''
		post = hashlib.sha256(row['POSTCODE'][:-2].replace(" ", "").encode('utf-8').lower()).hexdigest() if len(row['POSTCODE'])>0 else ''
		email = hashlib.sha256(re.sub('[^A-Za-z0-9_.+-@]+', '', row['EMAIL1']).encode('utf-8').strip().lower()).hexdigest() if len(row['EMAIL1'])>0 else ''
		phone = hashlib.sha256(re.sub(r'[\D]', '', row['MOBILE1']).encode('utf-8')).hexdigest() if len(row['MOBILE1'])>0 else ''
		ct = hashlib.sha256(re.sub('[^A-Za-z0-9]+', '', row['TOWN']).encode('utf-8').lower()).hexdigest() if len(row['TOWN'])>0 else ''
		st = hashlib.sha256(re.sub('[^A-Za-z0-9]+', '', row['COUNTY']).encode('utf-8').lower()).hexdigest() if len(row['COUNTY'])>0 else ''
		if i > 0:
			data.append([dhid,email,phone,fn,ln,country_GB,ct,st,post])
			print("\rRows processed: "+str(i)+" ................. "),
			if i % 10000 == 0:
				# Make requests to add users (in batches of 10K)
				params = {'payload': {'schema': schema,'data': data}}
				user_response = CustomAudience(custom_audience_id).create_user(fields=fields,params=params)
				api_calls = api_calls+1
				data = []
				print("\nRows processed: "+str(i)+" ................. "),
				sys.stdout.flush()
		i = i+1

	params = {'payload': {'schema': schema,'data': data}}
	user_response = CustomAudience(custom_audience_id).create_user(fields=fields,params=params)
	recs = i-1
	return recs


def main():

	parser = argparse.ArgumentParser(description="Create an audience on Facebook and add users from an audience file.")
	parser.add_argument("--existing", dest="custom_audience_id", help="add users to an existing audience.", metavar="audience_id")
	parser.add_argument("audience_file",  help="input audience file", metavar="audience_file.psv")
	parser.add_argument("audience_name",  help="audience name in platform", metavar="DOM_12345_PR_PB")
	parser.add_argument("config_file",  help="config file", metavar="config.ini")
	args = parser.parse_args()
	
	config = configparser.ConfigParser()
	config.read(args.config_file)

	business_manager_id = config.get('DEFAULT', 'BUSINESS_MANAGER_ID')
	app_id = config.get('DEFAULT', 'APP_ID')
	app_secret = config.get('DEFAULT', 'APP_SECRET')
	access_token = config.get('DEFAULT', 'ACCESS_TOKEN')
	dhid = config.get("CAMPAIGN", "DH_CAMPAIGN_ID")
	campaign_name = config.get("CAMPAIGN", "CAMPAIGN_NAME")

	ad_account_id = config.get('CAMPAIGN', 'AD_ACCOUNT_ID')

	FacebookAdsApi.init(app_id, app_secret, access_token)

	if args.custom_audience_id:
		custom_audience_id = args.custom_audience_id
	else:
		custom_audience_id = create_audience(ad_account_id, args.audience_name, dhid)

	rows = add_users(args.audience_file, custom_audience_id)
	print("\nAudience for campaign: " + campaign_name +" was created with id "+str(custom_audience_id)+" - "+str(rows)+" records processed" + " for " + args.audience_file)
	logger.info("\nAudience for campaign: " + campaign_name +" was created with id "+str(custom_audience_id)+" - "+str(rows)+" records processed"+ " for " + args.audience_file)
	
	#Run last process - create a campaign skeleton by running the campaign creator script with a newly created audience name, audience id, and its config file
	strDoneFolder = args.config_file.split("Config/")
	strDoneFolder = strDoneFolder[0] + "Config/Done/" + strDoneFolder[1]
	print("Creating campaign: " + campaign_name + " with ID:" + custom_audience_id + " for config file: " + strDoneFolder)
	logger.info("Creating campaign: " + campaign_name + " with ID:" + custom_audience_id + " with audience name: " + args.audience_name + " for config file: " + strDoneFolder)
	os.system("python3 /nfs/science/tesco_uk/OFFSITE/AudienceTest/Version/create_campaign_auto.py " + args.audience_name + " " + custom_audience_id + " " + strDoneFolder )


if __name__ == "__main__":
	main()

