import glob
import sys
import configparser
import os
import time
import datetime
import logging
from logging.handlers import TimedRotatingFileHandler
from time import sleep

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

#Format the log entries
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
handler = TimedRotatingFileHandler('Liveramp_conversions.log',  when='midnight', backupCount=7)
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

if len(sys.argv) == 1:
	strToday = datetime.datetime.utcnow().strftime('%d%m%Y')
else:
	strToday = sys.argv[1]

print("Parameter: " + strToday)
#Getting the config filename list - this is where the path goes
configList = glob.glob("/nfs/science/tesco_uk/OFFSITE/AudienceTest/Liveramp/Conversion_configs/config_*.ini")
strSourceFolder = '/nfs/tesco_gb/marketplace_etl_dropzone/FB_Audience_Load/TUK_Test/Google/'

#Preparing the parser and reading the file
config = configparser.ConfigParser()

#Run the following block as many times as there are config_ files in the folder
for y in range(len(configList)):
	config.read(configList[y])
	dh_campaign_id = config.get('CAMPAIGN', 'DH_CAMPAIGN_ID')
	floodlight_id = config.get('DEFAULT', 'FLOODLIGHT')

	print(CYELLOW + str(y) +CEND + CGREEN + " Config file List: " + CEND + CYELLOW + str(configList) + CEND)
	print(CYELLOW + "Reading config: " + CEND + CGREEN + configList[y] + CEND + CYELLOW + " for DH ID: " + CEND + CGREEN + dh_campaign_id + CEND)
	
	print(strSourceFolder + "LiveRamp_UK_Dunnhumby_CV" + "*" + str(dh_campaign_id) + "_" + strToday+ "*.psv")
	myFileList = glob.glob(strSourceFolder + "LiveRamp_UK_Dunnhumby_CV" + "*" + str(dh_campaign_id) + "_" + strToday + "*.psv")

	print(CYELLOW + "My File list: " + CEND + CGREEN +  str(myFileList) + "\n\n" + CEND)


	#Run the audience creator script for Facebook
	if len(myFileList) != 0:
		#Check if LiveRamp, doesn't have "CV", and no UUID in filename if so, gzip all files with dh_campaign_id
		for x in range(len(myFileList)):
			print("Reading: " + CGREEN + configList[y] + CEND)
			#Gziping, encrypting, and sending split audience files to Liveramp - since no UUID we should be in a Local folder
			print(CVIOLET2 + "=======================================================================================================================" + CEND)
			
			#Gziping, encrypting, and sending split audience files to Liveramp TEMP
			print(CGREEN2 + "Conversion files found for Liveramp. Runnning the conversion parser..." + CEND)
			os.system("python3 liveramp_conversions_parser.py " + myFileList[x] + " " + configList[y]) 

			#Change folder to Liveramp's temp one:
			myTempFileFolder = '/nfs/science/tesco_uk/OFFSITE/AudienceTest/Liveramp/'
			print("Gziping the Conversion files for Liveramp...")
			os.system("gzip "+ myTempFileFolder + "*" + floodlight_id + "*.psv" )
			print("Done")

			myNewZippedFileList = glob.glob(myTempFileFolder + "*" + floodlight_id + "*gz")
			#Encrypt the files after GZIP
			print(CYELLOW + "Encrypting the following files: " +CEND + CBLUE2 + myNewZippedFileList[x].split("/")[-1]  + CEND)
			print("gpg --encrypt --trust-model always --recipient LiveRamp " + CBLUE + myTempFileFolder + CEND + CBLUE + myNewZippedFileList[x].split("/")[-1]  + CEND)
			os.system("gpg --encrypt --trust-model always --recipient LiveRamp " +myTempFileFolder + myNewZippedFileList[x].split("/")[-1] )
			print(CGREEN2 + "Done encrypting "+ CEND + CBLUE + myNewZippedFileList[x].split("/")[-1] +".gz" + CEND)
			
			#Check if mapping file, then send over to a LiveRamp Bucket		
			myEncryptedFileList = glob.glob(myTempFileFolder + "*" + floodlight_id + "*gpg")
			print("Sending the following conversion file to AWS: " + CBLUE + myEncryptedFileList[x] +CEND)
			os.system("aws s3 cp " + myEncryptedFileList[x] + " s3://com-liveramp-eu-customer-uploads/1273/2/")
			print("File: "+ CBLUE + myEncryptedFileList[x] + CEND + " was sent.")


			#Removing any temp files
			print("Removing any temporary files..")
			os.system("rm " + myTempFileFolder + "*.psv.*")
			print(CGREEN + "Done." + CEND)

			print(CVIOLET2 + "=======================================================================================================================" + CEND)
	else:
		print("\nNo conversion files with DhID: " + dh_campaign_id + " were not found. Config file is not moved.")
		logger.warning("\nNo conversion files with DhID: "  + dh_campaign_id + " were not found. Config file is not moved.")
	