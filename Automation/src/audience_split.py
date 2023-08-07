#! /usr/bin/python
# coding: utf-8

import sys
import csv 
import hashlib
import re
import time
import datetime
import argparse 
import json 
import pandas as pd

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

# Function to split the audience in segment files for Facebook
# A second script is used to parse the output files and push them via Facebook API
def split_facebook(audience_df,segments,filename,campaign_id):
	i = 0
	for s in segments:
		segment_df = audience_df.loc[(audience_df['SEGMENT'] == s), audience_df.columns != 'SEGMENT'].rename(columns = {"CUSTOMERID": "CustomerID","PHONENUMBER": "MOBILE1"}) 
		output_file = "/nfs/science/tesco_uk/OFFSITE/AudienceTest/Facebook/DOM_" + campaign_id + "_" + segments[s]['name'] + "_FB.psv"
		segment_df.to_csv(output_file, sep='|', index=None, header=True)
		i = i + 1
	return i

# Function to split the audience in segment files for LiveRamp
def split_liveramp(audience_df,segments,filename,campaign_id):
	today = datetime.datetime.utcnow().strftime("%m%d%Y")
	i = 0
	for s in segments:

		actualFilename = filename.split('/')[-1]
		nameOfSegment = actualFilename.split('_')[6]
		audienceUUID = nameOfSegment[:32]
		segmentUUID = nameOfSegment[-32:]
		nameOfSegment = nameOfSegment[32:-32]

		print(CGREEN + "Filename: " + CEND + CYELLOW + actualFilename + CEND)
		print(CGREEN + "Segments NAME: " + CEND + CYELLOW + segments[s]['name'] + CEND)

		if len(nameOfSegment) != 0:
			segment_name = "DOM_" + campaign_id + "_" + nameOfSegment + "_" + audienceUUID + "_" + segmentUUID
		else:
			segment_name = "DOM_" + campaign_id + "_" + segments[s]['name']

		print(CGREEN + "Name of segment: " +CEND + CYELLOW + segment_name + CEND)

		segment_df = audience_df.loc[(audience_df['SEGMENT'] == s), ["CUSTOMERID","FIRSTNAME","LASTNAME","ADDRESS1","ADDRESS2","ADDRESS3","ADDRESS4","ADDRESS5","COUNTY","POSTCODE","EMAIL1","PHONENUMBER"]].rename(columns = {"CUSTOMERID":"CustomerID","ADDRESS5":"TOWN","PHONENUMBER":"MOBILE1"}) 
		segment_df.insert(len(segment_df.columns), segment_name, '1')
		output_file = "/nfs/science/tesco_uk/OFFSITE/AudienceTest/Liveramp/LiveRamp_UK_Dunnhumby_" + segment_name + "_" + today + ".psv"
		segment_df.to_csv(output_file, sep='|', index=None, header=True)
		i = i + 1
	return i

# Function to split the audience in segment files for Google Customer Match
# Customer Match formatting guide here: https://support.google.com/google-ads/answer/7659867
def split_customer(audience_df,segments,filename,campaign_id):
	i = 0
	regex_names = re.compile(r'[^A-Za-z0-9\-\s]+')
	regex_email = re.compile(r'[^A-Za-z0-9_.+-@]+')
	regex_phone = re.compile(r'[\D]+')
	for s in segments:
		segment_df = audience_df.loc[(audience_df['SEGMENT'] == s), ['FIRSTNAME','LASTNAME','POSTCODE','EMAIL1','PHONENUMBER']].rename(columns = {"FIRSTNAME":"First Name","LASTNAME":"Last Name","POSTCODE":"Zip","EMAIL1":"Email","PHONENUMBER":"Phone"}) 
		segment_df.insert(2, 'Country', 'GB')
		segment_df['First Name'] = segment_df['First Name'].str.replace(regex_names,'').apply(hash_string)
		segment_df['Last Name'] = segment_df['Last Name'].str.replace(regex_names,'').apply(hash_string)
		segment_df['Zip'] = segment_df['Zip']
		segment_df['Email'] = segment_df['Email'].str.replace(regex_email,'').apply(hash_string)
		segment_df['Phone'] = segment_df['Phone'].str.replace(regex_phone,'').apply(phone_string).apply(hash_string)
		# We split the files in 250K rows, as uploading the files through DV360 interface is problematic with larger files. 
		# Ideally we won't have to do this in the future if we can upload via API.
		file_size = 250000
		list_of_dfs = [segment_df.iloc[x:x+file_size,:] for x in range(0, len(segment_df),file_size)]
		j = 1
		for k in list_of_dfs:
			output_file = "/nfs/science/tesco_uk/OFFSITE/AudienceTest/YT/DOM_" + campaign_id + "_" + segments[s]['name'] + "_CM_"+str(j)+".csv"
			k.to_csv(output_file, sep=',', index=None, header=True)
			j = j+1
		i = i + 1
	return i

# Helper function to hash a string with SHA256 after making it lowercase
def hash_string(string):
	string = str(string)
	if len(string)>0:
		return hashlib.sha256(string.encode('utf-8').strip().lower()).hexdigest()
	else:
		return ''

# Helper function to add country code to phone numbers, using Google Customer Match format
def phone_string(string):
	string = str(string)
	if len(string)>0:
		if string[0] == '0':
			return '+44'+string[1:]
		else:
			return string

def main():
	parser = argparse.ArgumentParser(description="Split an audience file for use in Facebook, LiveRamp or Customer Match.")
	parser.add_argument("--facebook", dest="facebook_flag", help="create files for Facebook.", action='store_true')
	parser.add_argument("--liveramp", dest="liveramp_flag", help="create files for LiveRamp.", action='store_true')
	parser.add_argument("--customer", dest="customer_flag", help="create files for Customer Match.", action='store_true')
	parser.add_argument("audience_file",  help="input audience file", metavar="audience_file.psv")
	parser.add_argument("campaign_id",  help="dh internal campaign id", metavar="123456")
	parser.add_argument("segments",  help="json with segment names", metavar="'{\"PRIMARY_BUYERS\":{\"name\":\"PR_PB\"},\"PRIMARY_LAPSERS\":{\"name\":\"PR_LA\"},\"COMPETITOR_BUYERS\":{\"name\":\"CO_PB\"}}'")
	args = parser.parse_args()

	#filename = 'x'
	filename = args.audience_file
	df = pd.read_csv(args.audience_file, sep='|', dtype='str', quoting=csv.QUOTE_NONE, keep_default_na=False, error_bad_lines=False, engine='python')
	segments = json.loads(args.segments)


	if args.facebook_flag:
		r = split_facebook(df,segments,filename,args.campaign_id)
		print("\n"+str(r)+" files successfully created for Facebook.")
	if args.liveramp_flag:
		r = split_liveramp(df,segments,filename,args.campaign_id)
		print("\n"+str(r)+" files successfully created for LiveRamp.")
	if args.customer_flag:
		r = split_customer(df,segments,filename,args.campaign_id)
		print("\n"+str(r)+" files successfully created for Customer Match.")
	

if __name__ == "__main__":
	main()
