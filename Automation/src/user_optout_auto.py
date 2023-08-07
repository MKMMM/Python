#! /usr/bin/python
# coding: utf-8

import sys
import glob
import csv 
import hashlib
import re
import time
import datetime
import argparse 
sys.path.append('/nfs/shared/py_packages/facebook-python') # Replace this with the place you installed facebookads using pip
sys.path.append('/nfs/shared/py_packages/facebook-python') # same as above
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.customaudience import CustomAudience
from facebook_business.adobjects.user import User
from facebook_business import FacebookSession
from facebook_business.adobjects.adaccountuser import AdAccountUser as AdUser

#Add some text colors
CEND      = '\33[0m'
CBLACK  = '\33[30m'
CRED    = '\33[31m'
CGREEN  = '\33[32m'
CYELLOW = '\33[33m'
CBLUE   = '\33[34m'
CVIOLET = '\33[35m'
CBEIGE  = '\33[36m'
CWHITE  = '\33[37m'
CGREY    = '\33[90m'
CRED2    = '\33[91m'
CGREEN2  = '\33[92m'
CYELLOW2 = '\33[93m'
CBLUE2   = '\33[94m'
CVIOLET2 = '\33[95m'
CBEIGE2  = '\33[96m'
CWHITE2  = '\33[97m'

def remove_users(audience_file,ad_account_id):

	# Open the CSV 
	f = open(audience_file, 'rU' )  
	reader = csv.DictReader(f, delimiter='|', fieldnames = ( "CustomerID","FIRSTNAME","LASTNAME","ADDRESS1","ADDRESS2","ADDRESS3","ADDRESS4","ADDRESS5","TOWN","COUNTY","POSTCODE","EMAIL1","MOBILE1"))

	print ("\nProcessing ad account "+ad_account_id+" ...\n")

	# Prepare the data in json format and split in batches of 10K
	api_calls = 0
	i = 0
	fields = []
	schema = ["EXTERN_ID"]
	data = []
	gb = 'gb' 
	country_GB = hashlib.sha256(gb.encode('utf-8')).hexdigest()
	
	ad_account = AdAccount(ad_account_id)
	for row in reader:
		# Normalize and hash data for Facebook API
		dhid = hashlib.sha256(row['CustomerID'].encode('utf-8')).hexdigest()
		if i > 0:
			data.append([dhid])
			print ("\rRows processed: "+str(i)+" ................. ")
			if i % 1000 == 0:
				# Make requests to add users (in batches of 10K)
				params = {'payload': {'schema': schema,'data': data}}
				user_response = ad_account.delete_users_of_any_audience(fields=fields,params=params)
				api_calls = api_calls+1
				data = []
				print ("\nRows processed: "+str(i)+" ................. ")
				sys.stdout.flush()
		i = i+1

	params = {'payload': {'schema': schema,'data': data}}
	user_response = ad_account.delete_users_of_any_audience(fields=fields,params=params)
	recs = i-1
	f.close()
	return recs


def main():

	if len(sys.argv) == 1:
		strToday = datetime.datetime.utcnow().strftime('%d%m%Y')
	else:
		strToday = sys.argv[1]

	#strFileNameWithPath = sys.argv[1]
	#Select file name with path for the splitter script
	strFiles = glob.glob('/nfs/tesco_gb/marketplace_etl_dropzone/FB_Audience_Load/TUK_Test/Google/LiveRamp_UK_Dunnhumby_optout_optout_*' + strToday + "*.psv")

	access_token = 'EAADwubHpNPoBAJyUwGzciZBjsha3pZAvjpJmUwoqcfLQnjI56CxGykci7ziyjCi8408FTz3D1jvIFG0Um4IMguNE7dxeZAnozX9sNm8SGh0oxdfGLaPhdVqBzYRYMmrqcvb8cILBdfyXpJBZCAHzxVGJRlxRd4RqNGfcyAeZAqRbAUUZBfOBH8S6Sp617qwknceob7T43s3wZDZD'
	app_secret = '1d9a17e56a843e59a18f873032b48a3f'
	app_id = '264680344466682'

	session = FacebookSession(app_id,app_secret,access_token)
	api = FacebookAdsApi(session)

	# parser = argparse.ArgumentParser(description="Remove users from Facebook.")
	# parser.add_argument("audience_file",  help="input audience file", metavar="audience_file.psv")
	# #parser.add_argument("config_file",  help="config file", metavar="config_file.ini")
	# args = parser.parse_args()
	if len(strFiles) != 0:
		FacebookAdsApi.init(app_id, app_secret, access_token)
		FacebookAdsApi.set_default_api(api)

		### Setup user and pull the ad accounts ###
		me = AdUser(fbid='me')
		fields = []
		params = {}
		ad_accounts = []

		my_accounts_iterator = me.get_ad_accounts()
		print('Generating the list of accounts')
		for account in my_accounts_iterator:
			print(account["id"] + ",")
			ad_accounts.append(account["id"])

		#ad_accounts = ['act_481423986052632','act_2537774899610107','act_2934852626528871','act_438194746809428','act_3300021086707284','act_706901063380033','act_693039611157017','act_131927774891965','act_395724961329244','act_2129846587308633','act_1172410416277512','act_206077127427905','act_523997924868710','act_434675067198810','act_446905932834083','act_473392113615742','act_694914100987135','act_1466598723495922','act_1809461802522542','act_447096735924892','act_340591696822851','act_648648332338954','act_621172908417701','act_2721931827887232','act_798182890627285','act_476980339575408','act_2584839464942173','act_820348215073088','act_987041654999717','act_520306815432944','act_188219839237477','act_537308417105175','act_754607051688211','act_3174635396094886','act_420656225267987','act_605475276660439','act_1159488227570904','act_896409040732506','act_3430288210330184','act_452141772370480','act_195050298218982','act_487325098550072','act_591489068086704','act_1592198374253769','act_540265339955292','act_613239442717187','act_411785946420220','act_1326725310822626','act_2672007102852105','act_1846853352118087','act_256203872121352']
		

		for ad_account_id in ad_accounts:
			rows = remove_users(strFiles[0],ad_account_id)
			print("\nRemoved "+str(rows)+" users from ad_account "+ad_account_id+".\n")
	else:
		print(CRED + "No opt out files found today!" + CEND)
if __name__ == "__main__":
	main()
