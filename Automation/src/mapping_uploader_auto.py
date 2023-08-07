import glob
import sys
import configparser
import os
import time
import datetime
import logging
import pandas as pd
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
handler = TimedRotatingFileHandler('Mapping.log',  when='midnight', backupCount=7)
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

if len(sys.argv) == 1:
	strToday = datetime.datetime.utcnow().strftime('%d%m%Y')
else:
	strToday = sys.argv[1]

#strFileNameWithPath = sys.argv[1]
#Select file name with path for the splitter script
strFiles = glob.glob('/nfs/tesco_gb/marketplace_etl_dropzone/FB_Audience_Load/TUK_Test/Google/LiveRamp_UK_Dunnhumby_mapping_map_*' + strToday + "*.psv")

if len(strFiles) != 0:
	print(CVIOLET2 + "=======================================================================================================================" + CEND)

	strFileNameWithPath = strFiles[0]
	print(CGREEN + "Filename used: " + CEND + CBLUE + strFileNameWithPath + CEND)

	df = pd.read_csv(strFileNameWithPath, sep='|', usecols = ['SEGMENT'], nrows=1)
	strSegmentName = str(df.SEGMENT[0])
	print("Segments name: " + strSegmentName)

	#File has to be parsed by the splitter to be compliant with Liveramp
	print(CGREEN + "Splitting the mapping file for liveramp..." + CEND)
	print("python3 audience_split.py --liveramp "  +  CBLUE + strFileNameWithPath + CEND +  " \'ALL\' \'{\"" + strSegmentName + "\":{\"name\":\"ALL\"}}\'" )
	print(CGREEN + "Running...." + CEND)
	os.system("python3 audience_split.py --liveramp " + strFileNameWithPath +  " \'ALL\' \'{\"" + strSegmentName + "\":{\"name\":\"ALL\"}}\'" )

	#Instantiate the temp folder as the next step's source, and grab the filename list from the newly split file:
	strSourceFolder = '/nfs/science/tesco_uk/OFFSITE/AudienceTest/Liveramp/'
	myFileList = glob.glob(strSourceFolder + "LiveRamp_UK_Dunnhumby_DOM_ALL_ALL_" + "*.psv")

	print(CGREEN + "File to be processed:" + CEND + CBLUE + myFileList[0] + CEND)
	print(CGREEN + "Gziping the mapping file for Liveramp..." + CEND)
	print("gzip "+ CBLUE + strSourceFolder + CEND + CBLUE2 + myFileList[0].split("/")[-1] + CEND)
	os.system("gzip "+ strSourceFolder + myFileList[0].split("/")[-1])
	print(CYELLOW + "Done" + CEND)

	#Encrypt the files after GZIP
	print("Encrypting the following file: " + CBLUE2 + myFileList[0].split("/")[-1] + ".gz" + CEND)
	print("gpg --encrypt --trust-model always --recipient LiveRamp " + CBLUE + strSourceFolder + CEND + CBLUE + myFileList[0].split("/")[-1] +".gz" + CEND)
	os.system("gpg --encrypt --trust-model always --recipient LiveRamp " +strSourceFolder + myFileList[0].split("/")[-1] +".gz")
	print("Done encrypting " + CBLUE + myFileList[0].split("/")[-1] +".gz" + CEND)

	#Check if mapping file, then send over to a LiveRamp Bucket
	print("Sending the following file to AWS: " + CBLUE + myFileList[0].split("/")[-1] +".gz.gpg" + CEND)

	os.system("aws s3 cp " + strSourceFolder + myFileList[0].split("/")[-1] + ".gz.gpg" + " s3://com-liveramp-eu-customer-uploads/1273/3/")
	print("Mapping file: "+ CBLUE +  myFileList[0].split("/")[-1].split(".")[0] +".gz.gpg" + CEND + " was sent.")

	print(CRED + "Removing temp files..." + CEND)
	print("rm " + strSourceFolder + CRED + "LiveRamp_UK_Dunnhumby_DOM_ALL_ALL_" + "*gpg" + CEND)
	print("rm " + strSourceFolder+ CRED + "LiveRamp_UK_Dunnhumby_DOM_ALL_ALL_" + "*gz" + CEND)

	os.system("rm " + strSourceFolder + "LiveRamp_UK_Dunnhumby_DOM_ALL_ALL_" + "*gpg")
	os.system("rm " + strSourceFolder+ "LiveRamp_UK_Dunnhumby_DOM_ALL_ALL_" + "*gz")
	print(CGREEN + "Temp files removed." + CEND)
else:
	print(CRED + "No new files found!" + CEND )
	logger.info("No new files found!")
