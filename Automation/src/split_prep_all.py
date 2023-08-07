import sys
import json
import pandas as pd
import csv
import os
import glob
import configparser
import time
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

# format the log entries
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
handler = TimedRotatingFileHandler('Audience.log',  when='midnight', backupCount=7)
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

#Setting enviromental paths
strConfigPath = "/nfs/science/tesco_uk/OFFSITE/AudienceTest/Config/"
strFacebookPath = "/nfs/science/tesco_uk/OFFSITE/AudienceTest/Facebook"
strLiveRampPath = "/nfs/science/tesco_uk/OFFSITE/AudienceTest/Liveramp"
strYTPath = "/nfs/science/tesco_uk/OFFSITE/AudienceTest/YT"

#Creating list 
configList = glob.glob(strConfigPath + "config_*.ini")

#Preparing the parser and reading the file
config = configparser.ConfigParser(allow_no_value=True)

#Check for an additional parameter in the commandline
if len(sys.argv) == 2:
	strParam = sys.argv[1]
	if strParam == "--facebook":
		strFolderPath = '/nfs/tesco_gb/marketplace_etl_dropzone/FB_Audience_Load/TUK_Test/Facebook/'
	elif strParam == "--liveramp":
		strFolderPath = '/nfs/tesco_gb/marketplace_etl_dropzone/FB_Audience_Load/TUK_Test/Google/'
	elif strParam == "--customer":
		strFolderPath = '/nfs/tesco_gb/marketplace_etl_dropzone/FB_Audience_Load/TUK_Test/Google/'
	elif strParam == "--mapping":
		isMapping = "True"
		strFolderPath = '/nfs/tesco_gb/marketplace_etl_dropzone/FB_Audience_Load/TUK_Test/Google/'

#Run the following block as many times as there are config_ files in the folder
for y in range(len(configList)):

	config.read(configList[y])
	
	print("\n" + CYELLOW + str(y) +CEND + CGREEN + " Config file List: " + CEND + CYELLOW + str(configList) + CEND)
	#Create a variable with DH campaign ID
	dh_campaign_id = config.get('CAMPAIGN', 'DH_CAMPAIGN_ID')
	dh_uuid = config.get('CAMPAIGN', 'UUID')
	print(CGREEN + "DH UUID:" + CEND + CYELLOW + dh_uuid + CEND)
	myFileList = glob.glob((strFolderPath + "*" + "_" + str(dh_campaign_id) + "_" + "*psv"))
	print("My file list: " + CYELLOW + str(myFileList) + CEND)

	if len(myFileList) != 0:
		#Creating a command list needed for upload
		for x in range(len(myFileList)):
			strMyFile = myFileList[x]
			
			print(strMyFile)
			print(CGREEN + "UUID Lenght: " +CEND + CYELLOW + str(strMyFile.find(dh_uuid)) +CEND )
			foovar = strMyFile.find("CV")
			print(CGREEN + "IS CV: " +CEND + CYELLOW + str(foovar) + CEND)

			#Checking if the filename is a conversion file for Liveramp, or is conversion and doesn't have UUID for facebook then start reading file contents 
			if strMyFile.find("CV") == -1 and strParam == "--liveramp" or strMyFile.find("CV") == -1 and len(dh_uuid) == 0 and strParam =="--facebook": #strMyFile.find(dh_uuid) == 0 and 
				#Reading the file selected in argument and parsing it to get audience names from SEGMENT column
				print("Reading file....")

				df = pd.read_csv(strMyFile, sep='|', dtype='str', quoting=csv.QUOTE_NONE, keep_default_na=False, error_bad_lines=False, engine='python' )
				result = df.groupby('SEGMENT')['CUSTOMERID'].nunique()

				print(CYELLOW + "Results: " + CEND)
				print(CBLUE2 + str(result) + CEND)

				#Creating a dictionary parameter list from audience names
				dictRowNames = result.index.values

				#Create a JSON string of parameters from an array of aucdience names (replacing any whitespaces for separate audience filenames)
				strJSON = json.dumps({n:{"name":n.replace(" ","_")} for n in dictRowNames})

				#Printing and running the output command to split the files
				print("\nCommand running for the audience_split script:\n")
				print("python3 " + CGREEN2 + "/nfs/science/tesco_uk/OFFSITE/AudienceTest/Version/audience_split.py " + CEND + CYELLOW +  strParam + CEND + " " + CVIOLET + strMyFile + CEND +  " '" + CGREEN + dh_campaign_id + CEND+ "' '" + CBLUE2 + strJSON.replace(": ",":").replace(", ",",") + "'\n\n" + CEND)
				print("Working.... Standby....")
				os.system("python3 /nfs/science/tesco_uk/OFFSITE/AudienceTest/Version/audience_split.py " + strParam + " " + strMyFile + " '" + dh_campaign_id + "' '" + strJSON.replace(": ",":").replace(", ",",")  + "'\n\n" )
	else:
		print(CRED + "\nAudience file with DhID: " + dh_campaign_id + " was not found. Config file is not moved." + CEND)
		logger.warning("Audience file with DhID: " + dh_campaign_id + " was not found. Config file is not moved.")

# Run uploader script for different platforms depending on parameter used
if len(configList) != 0:
	print(CVIOLET2 + "=======================================================================================================================" + CEND)
	print("Starting Uploads for: " + CYELLOW + strParam + CEND)
	#Starting the uploader
	print("python3 " + CGREEN2 + "upload_prep_new.py " + CEND +  CYELLOW + strParam + CEND)
	os.system("python3 /nfs/science/tesco_uk/OFFSITE/AudienceTest/Version/upload_prep_new.py " + strParam)

else:
	print(CRED + "No config files found and no files were uploaded." + CEND)
	logger.warning("No config files found and no files were uploaded.")


###################################################################################################
		#TODO: Logging
