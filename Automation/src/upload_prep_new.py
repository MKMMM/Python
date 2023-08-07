import glob
import sys
import configparser
import os
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

#Format the log entries
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
handler = TimedRotatingFileHandler('Audience.log',  when='midnight', backupCount=7)
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

#Getting the config filename list - this is where the path goes
configList = glob.glob("/nfs/science/tesco_uk/OFFSITE/AudienceTest/Config/config_*.ini")

#Preparing the parser and reading the file
config = configparser.ConfigParser()

#Run the following block as many times as there are config_ files in the folder
for y in range(len(configList)):
	config.read(configList[y])
	print(CVIOLET2 + "=======================================================================================================================" + CEND)
	strParam = sys.argv[1]
	#Create a variable with DH campaign ID
	dh_campaign_id = config.get('CAMPAIGN', 'DH_CAMPAIGN_ID')
	UUID = config.get('CAMPAIGN', 'UUID')
	floodlight_id = config.get('DEFAULT', 'FLOODLIGHT')
	adacct_id = config.get('CAMPAIGN', 'AD_ACCOUNT_ID')

	print(CGREEN + "UUID: " + CEND + CYELLOW + UUID + CEND + CGREEN + " Len:"+ CEND + CYELLOW + str(len(UUID)) +CEND)
	isMapping = "False"
	strDoneFolder = '/nfs/science/tesco_uk/OFFSITE/AudienceTest/Config/Done/'
	strLvrmpCVFolder = '/nfs/science/tesco_uk/OFFSITE/AudienceTest/Liveramp/Conversion_configs/'

	if len(UUID) > 0 and strParam == '--facebook':
		strSourceFolder = '/nfs/tesco_gb/marketplace_etl_dropzone/FB_Audience_Load/TUK_Test/Facebook/'
	elif len(UUID) < 1 and strParam == '--facebook':
		strSourceFolder = '/nfs/science/tesco_uk/OFFSITE/AudienceTest/Facebook/'

	if len(UUID) > 0 and strParam == '--liveramp':
		strSourceFolder = '/nfs/science/tesco_uk/OFFSITE/AudienceTest/Liveramp/'
	elif len(UUID) < 1 and strParam =='--liveramp':
		strSourceFolder = '/nfs/science/tesco_uk/OFFSITE/AudienceTest/Liveramp/'

	if strParam == '--mapping':
		isMapping = "True"
		strSourceFolder = '/nfs/science/tesco_uk/OFFSITE/AudienceTest/Liveramp/'

	print(CYELLOW + str(y) +CEND + CGREEN + " Config file List: " + CEND + CYELLOW + str(configList) + CEND)
	print(CYELLOW + "Reading config: " + CEND + CGREEN + configList[y] + CEND + CYELLOW + " for DH ID: " + CEND + CGREEN + dh_campaign_id + CEND)
	print(strSourceFolder + "*" + "_" + CGREEN + str(dh_campaign_id) + CEND + "_" + "*.psv")
	myFileList = glob.glob(strSourceFolder + "*" + "_" + str(dh_campaign_id) + "_" + "*.psv")
	print(CYELLOW + "My File list: " + CEND + CGREEN +  str(myFileList) + "\n\n" + CEND)

	#Run the audience creator script for Facebook
	if len(myFileList) != 0:
		if strParam == '--facebook':
			#Printing the output command
			print(CVIOLET2 + "=======================================================================================================================" + CEND)
			print("\nThe following commands will run for:  " + CGREEN +  configList[y] + CEND)
			logger.info("The following commands will run for:  "+ configList[y])

			sleep_time = 2
			num_retries = 5
			for z in range(0, num_retries):  
				try:
					for x in range(len(myFileList)):
						print("python3 " + CYELLOW + "create_audience_science.py " + CEND + CBLUE2 + myFileList[x] + CEND + " " + CBLUE + myFileList[x].split(".")[0].split("/")[-1] + CEND + " " + CGREEN + configList[y] + CEND)
						logger.info("python3 create_audience_science.py " + myFileList[x] + " " + myFileList[x].split(".")[0].split("/")[-1] + " " + configList[y])
						os.system( "python3 /nfs/science/tesco_uk/OFFSITE/AudienceTest/Version/create_audience_science.py " + myFileList[x] + " " + myFileList[x].split(".")[0].split("/")[-1] + " " + configList[y] + " &")
					str_error = None
				except Exception as str_error:
					pass

				if str_error:
					sleep(sleep_time)  # Wait before the next try
					logger.warning("Audience push failed. Retrying...")
					sleep_time *= 2  # Implemented an exponential backoff to wait a bit longer after each try
				else:
					break
					logger.warning("Audience push failed " + num_retries + " times. Please retry manually")

			print(CYELLOW + "Creating custom conversions for: " + CEND + CGREEN + configList[y] + CEND)
			os.system("python3 /nfs/science/tesco_uk/OFFSITE/AudienceTest/Version/create_conversions_science.py " + configList[y])

	
		#Check if LiveRamp, doesn't have "CV", and no UUID in filename if so, gzip all files with dh_campaign_id
		if strParam == "--liveramp" :
			for x in range(len(myFileList)):
				print("Reading: " + CGREEN + configList[y] + CEND)
				if myFileList[x].find("CV") == -1 and len(UUID) == 0:	
					#Gziping, encrypting, and sending split audience files to Liveramp - since no UUID we should be in a Local folder
					print(CVIOLET2 + "=======================================================================================================================" + CEND)
					print(CRED + "Found NO UUID" + CEND)
					print("Gziping the audience file for Liveramp...")
					print("gzip "+ CBLUE + strSourceFolder + CEND + CBLUE2 + myFileList[x].split("/")[-1] + CEND)
					os.system("gzip "+ strSourceFolder + myFileList[x].split("/")[-1])
					print(CYELLOW + "Done" + CEND)
					
					#Encrypt the files after GZIP
					print("Encrypting the following file: " + CBLUE2 + myFileList[x].split("/")[-1] + ".gz" + CEND)
					print("gpg --encrypt --trust-model always --recipient LiveRamp " + CBLUE + strSourceFolder + CEND + CBLUE + myFileList[x].split("/")[-1] +".gz" + CEND)
					os.system("gpg --encrypt --trust-model always --recipient LiveRamp " +strSourceFolder + myFileList[x].split("/")[-1] +".gz")
					print("Done encrypting " + CBLUE + myFileList[x].split("/")[-1] +".gz" + CEND)
					
					#Check if mapping file, then send over to a LiveRamp Bucket
					print("Sending the following file to AWS: " + CBLUE + myFileList[x].split("/")[-1] +".gz.gpg" + CEND)
					if isMapping == "False":
						os.system("aws s3 cp " + strSourceFolder + myFileList[x].split("/")[-1] + ".gz.gpg" + " s3://com-liveramp-eu-customer-uploads/1273/1/")
						print("File: "+ CBLUE + myFileList[x].split("/")[-1] +".gpg" + CEND + " was sent.")
					else:
						os.system("aws s3 cp " + strSourceFolder + myFileList[x].split("/")[-1] + ".gz.gpg" + " s3://com-liveramp-eu-customer-uploads/1273/3/")
						print("Mapping file: "+ CBLUE +  myFileList[x].split("/")[-1].split(".")[0] +".gz.gpg" + CEND + " was sent.")
				
					print(CRED + "Removing temp files..." + CEND)
					os.system("rm " + strSourceFolder + "*" + dh_campaign_id + "*gpg")
					os.system("rm " + strSourceFolder+ "*" + dh_campaign_id + "*gz")
					print(CGREEN + "Temp files removed." + CEND)

					#If UUID is present and upload directly from the Audience FOLDER
				elif myFileList[x].find("CV") == -1 and len(UUID) > 0:
					#Gziping, encrypting, and sending split audience files to Liveramp TEMP
					print(CVIOLET2 + "=======================================================================================================================" + CEND)
					print(CYELLOW + "Found UUID: " + CGREEN + UUID + CEND)
					print("Copying file into temp folder...")
					print("cp "+ CBLUE + myFileList[x] + CEND + " /nfs/science/tesco_uk/OFFSITE/AudienceTest/Liveramp/")
					os.system("cp "+ myFileList[x] + " /nfs/science/tesco_uk/OFFSITE/AudienceTest/Liveramp/")
					strSourceFolder =  '/nfs/science/tesco_uk/OFFSITE/AudienceTest/Liveramp/'
					
					print("Gziping the audience file for Liveramp...")
					print("gzip "+ CBLUE + strSourceFolder + CEND + CBLUE2 + myFileList[x].split("/")[-1] + CEND)
					os.system("gzip "+ strSourceFolder + myFileList[x].split("/")[-1])
					print(CGREEN + "Done" + CEND)
					
					print("Encrypting the following file: " + CBLUE + myFileList[x].split("/")[-1] + ".gz" + CEND)
					print("gpg --encrypt --trust-model always --recipient LiveRamp " + CBLUE2 + strSourceFolder + CEND + CBLUE + myFileList[x].split("/")[-1] + ".gz" + CEND)
					os.system("gpg --encrypt --trust-model always --recipient LiveRamp " + strSourceFolder + myFileList[x].split("/")[-1] + ".gz")
					print("Done encrypting " + CBLUE + myFileList[x].split("/")[-1] + ".gz" + CEND)
							
					#Change the Folder since a file with UUID is in a folder without permission
					print("Changing the folder to: " + CBLUE2 + strSourceFolder + CEND + "and starting encrypt files...")
					strSourceFolder =  '/nfs/science/tesco_uk/OFFSITE/AudienceTest/Liveramp/'
					#Check if mapping file, then send over to a LiveRamp Bucket		

					print("Sending the following file to AWS: " + CBLUE + myFileList[x].split("/")[-1] +".gz.gpg" + CEND)
					if isMapping == "False":
						os.system("aws s3 cp " + strSourceFolder + myFileList[x].split("/")[-1] + ".gz.gpg" + " s3://com-liveramp-eu-customer-uploads/1273/1/")
						print("File: "+ CBLUE + myFileList[x].split("/")[-1] +".gpg" + CEND + " was sent.")
					else:
						os.system("aws s3 cp " + strSourceFolder + myFileList[x].split("/")[-1] + ".gz.gpg" + " s3://com-liveramp-eu-customer-uploads/1273/3/")
						print("Mapping file: "+ CBLUE + myFileList[x].split("/")[-1].split(".")[0] +".gz.gpg" + CEND + " was sent.")
				
					print(CRED + "Removing temp files..." + CEND)
					os.system("rm " + strSourceFolder + "*" + dh_campaign_id + "*gpg")
					os.system("rm " + strSourceFolder+ "*" + dh_campaign_id + "*gz")
					print(CGREEN + "Temp files removed." + CEND)

				#If UUID is present and "CV" is found and UUID is not present
				elif myFileList[x].find("CV") != -1 and len(UUID) == 0:
					print("No soup for conversions!!!!!!")

	else:
		print("\nAudience file with DhID: " + dh_campaign_id + " was not found. Config file is not moved.")
		logger.warning("Audience file with DhID: " + dh_campaign_id + " was not found. Config file is not moved.")

	print("DH ID: "+ dh_campaign_id)
	print("Floodlight: " + floodlight_id)

	if len(floodlight_id) < 1 and strParam == '--facebook':
		print("Floodlight: " + floodlight_id)
		logger.info("Floodlight: " + floodlight_id)
		print("Facebook campaign only, moving config to the \'Done\' folder..." )
		logger.info("Facebook campaign only, moving config to the \'Done\' folder..." )
		os.system("mv "+ configList[y] + " " + strDoneFolder)
		logger.info("mv "+ configList[y] + " " + strDoneFolder)
	elif strParam == '--liveramp':
		print(CGREEN + "Copying the config to the \'Liveramp_conversions\' folder..." + CEND)
		os.system("cp "+ configList[y] + " " + strLvrmpCVFolder)
		print(CGREEN + "Done!" + CEND)

		print("Moving config to the \'Done\' folder..." )
		os.system("mv "+ configList[y] + " " + strDoneFolder)
		print(CGREEN + "Done!" + CEND)
