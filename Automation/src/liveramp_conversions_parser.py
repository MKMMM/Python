#! /usr/bin/python
# coding: utf-8

import sys
import csv 
import time
import datetime
import re
import configparser
from io import StringIO

def process_file(filename,floodlight,flabel,campaign_id):

	today = datetime.datetime.utcnow().strftime("%m%d%Y")
	output_fp_on = "/nfs/science/tesco_uk/OFFSITE/AudienceTest/Liveramp/LiveRamp_UK_Conversions_" + floodlight + "_" + today + ".psv"

	# Create the output files
	f1 = open(output_fp_on,"w+")
	header = "CustomerID|FIRSTNAME|LASTNAME|ADDRESS1|ADDRESS2|ADDRESS3|ADDRESS4|TOWN|COUNTY|POSTCODE|EMAIL1|MOBILE1|Product Group/Channel|Timestamp|Conversion_Amount|Conversion_Quantity|Ordinal|U1|U2|U3"
	f1.write(header)

	err = 0
	i = 0
	with open(filename, 'rU') as f:
		data = f.read()
		data = data.replace('\x00','')
		r = csv.DictReader(StringIO(data), delimiter='|', fieldnames = ( "TIMESTAMP","TRANSACTION_ID","VALUE","PROD_FLAG","CHANNEL","CUSTOMERID","FIRSTNAME","LASTNAME","ADDRESS1","ADDRESS2","ADDRESS3","ADDRESS4","ADDRESS5","TOWN","COUNTY","POSTCODE","EMAIL1","PHONENUMBER"))
		for row in r:
			if i > 0:
				include = True
				# Obfuscate data for LiveRamp
				fn = re.sub('[^A-Za-z0-9_\-\s]+', '', row['FIRSTNAME']).lower() if len(row['FIRSTNAME'])>0 else ''
				ln = re.sub('[^A-Za-z0-9_\-\s]+', '', row['LASTNAME']).lower() if len(row['LASTNAME'])>0 else ''
				post = re.sub('[^A-Za-z0-9\s]+','',row['POSTCODE']) if len(row['POSTCODE'])>0 else ''
				email = re.sub('[^A-Za-z0-9_.+-@]+', '', row['EMAIL1']).strip().lower() if len(row['EMAIL1'])>0 else ''
				phone = re.sub(r'[\D]', '', row['PHONENUMBER']) if len(row['PHONENUMBER'])>0 else ''
				add1 = re.sub('[^A-Za-z0-9_\-\s]+', '', row['ADDRESS1']).lower() if len(row['ADDRESS1'])>0 else ''
				add2 = re.sub('[^A-Za-z0-9_\-\s]+', '', row['ADDRESS2']).lower() if len(row['ADDRESS2'])>0 else ''
				add3 = re.sub('[^A-Za-z0-9_\-\s]+', '', row['ADDRESS3']).lower() if len(row['ADDRESS3'])>0 else ''
				add4 = re.sub('[^A-Za-z0-9_\-\s]+', '', row['ADDRESS4']).lower() if len(row['ADDRESS4'])>0 else ''
				ct = re.sub('[^A-Za-z0-9\-\s]+', '', row['ADDRESS5']).lower() if len(row['ADDRESS5'])>0 else ''
				st = re.sub('[^A-Za-z0-9\-\s]+', '', row['COUNTY']).lower() if len(row['COUNTY'])>0 else ''
				tr = str(int(row['TRANSACTION_ID']) * 3) if len(row['TRANSACTION_ID'])>0 else ''
				val = str(float(row['VALUE']) * 2.71828) if len(row['VALUE'])>0 else ''
				if row['PROD_FLAG'] == "Product":
					pr = "JB6WbLPtQu"
				elif row['PROD_FLAG'] == "Brand":
					pr = "cyqvM5zTBj"
				else: 
					pr = ''
					include = False
				if row['CHANNEL'] == "ONL":
					ch = "Nzyp4HHS3Z"
				elif row['CHANNEL'] == "STO":
					ch = "UsGrt25StE"
				else: 
					ch=''
					include = False
					
				rowstr = '\n' + row['CUSTOMERID'] + '|' + fn + '|' + ln + '|' + add1 + '|' + add2 + '|' + add3 + '|' + add4 + '|' + ct + '|' + st + '|' + post + '|' + email + '|' + phone + '|' + flabel + '|' + row['TIMESTAMP'] + '|' + val + '|1|' + tr + '|' + campaign_id + '|' + pr + '|' + ch

				if include:
					f1.write(rowstr)
				else:
					err = err+1
			i = i+1

	recs = i-1

	f.close() 
	f1.close() 
	return [recs,err]


def main():

	if len(sys.argv) < 3:
		print("\nPlease provide the conversions file and config file as arguments.\nUsage: python liveramp_conversions.py conversions_file.psv config_file.ini\n")
		sys.exit()

	conversions_file = sys.argv[1]
	config_file = sys.argv[2]

	config = configparser.ConfigParser()
	config.read(config_file)

	floodlight = config.get('DEFAULT', 'FLOODLIGHT')
	flabel = config.get('DEFAULT', 'FLOODLIGHT_LABEL')
	campaign_id = config.get('CAMPAIGN', 'DH_CAMPAIGN_ID')

	[rows,err] = process_file(conversions_file,floodlight,flabel,campaign_id)
	print("\nConversions file processed with "+str(rows)+" records and "+str(err)+" errors.\n")

if __name__ == "__main__":
	main()