#! /usr/bin/python

import sys
#sys.path.append('/nfs/shared/py_packages/facebook-python') # Replace this with the place you installed facebookads using pip
#sys.path.append('/nfs/shared/py_packages/facebook-python') # same as above

#sys.path.append('/nfs/science/tesco_uk/OFFSITE/AudienceTest/myenv/lib/python3.6/site-packages')
#sys.path.append('/nfs/science/tesco_uk/OFFSITE/AudienceTest/facebook_business/')

from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
import argparse 
import configparser
import logging
from logging.handlers import TimedRotatingFileHandler
import csv 
import hashlib
import re
import time
import datetime
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.business import Business
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.adsinsights import AdsInsights

# format the log entries
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
handler = TimedRotatingFileHandler('Audience.log',  when='midnight', backupCount=1)
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

parser = argparse.ArgumentParser(description="Create an audience on Facebook and add users from an audience file.")
parser.add_argument("config_file",  help="config file", metavar="config.ini")
args = parser.parse_args()
  
config = configparser.ConfigParser()
config.read(args.config_file)

business_manager_id = config.get('DEFAULT', 'BUSINESS_MANAGER_ID')
app_id = config.get('DEFAULT', 'APP_ID')
app_secret = config.get('DEFAULT', 'APP_SECRET')
access_token = config.get('DEFAULT', 'ACCESS_TOKEN')

ad_account_id = config.get('CAMPAIGN', 'AD_ACCOUNT_ID')
start_time =  config.get('CAMPAIGN', 'START_DATE')
end_time =  config.get('CAMPAIGN', 'END_DATE')

dh_campaign_id = config.get('CAMPAIGN', 'DH_CAMPAIGN_ID')
brand = config.get("CAMPAIGN", "BRAND")
strToday = datetime.datetime.utcnow().strftime('%d%m%Y')

custom_conv_optim = config.get('INSIGHTS', 'CUSTOM_CONV_OPTIM')
custom_conv_fp_on = config.get('INSIGHTS', 'CUSTOM_CONV_FP_ON')
custom_conv_fp_of = config.get('INSIGHTS', 'CUSTOM_CONV_FP_OF')
custom_conv_br_on = config.get('INSIGHTS', 'CUSTOM_CONV_BR_ON')
custom_conv_br_of = config.get('INSIGHTS', 'CUSTOM_CONV_BR_OF')

f = FacebookAdsApi.init(app_id, app_secret, access_token)
print(f.API_VERSION)

start_time = start_time[0:10]
end_time = (datetime.datetime.strptime(end_time[0:10], "%Y-%m-%d") + datetime.timedelta(days=28)).strftime("%Y-%m-%d")

dict_data = {}

# Make request to get insights
fields = [
	'adset_id',
	'adset_name',
	'impressions',
	'reach',
	'frequency',
	'clicks',
	'cpm',
	'cpc',
	'ctr',
	'spend'
]
params = {
	'level': 'adset',
	'action_report_time': 'conversion',
	'time_increment': 1,
	'time_range': {"since":start_time,"until":end_time},
	'action_attribution_windows':['28d_click','28d_view']
}
response = AdAccount('act_'+ad_account_id).get_insights(
  fields=fields,
  params=params
)

for row in response:
	actions = {}
	row_key = row['adset_id']+"_"+row['date_start']
	row_key = str(row_key).encode('utf-8')
	row_key = hashlib.sha256(row_key).hexdigest()
	actions['adset_id'] = row['adset_id']
	actions['adset_name'] = row['adset_name'].replace(',',' ')
	actions['date_start'] = row['date_start']
	actions['date_stop'] = row['date_stop']
	actions['impressions'] = row['impressions'] if 'impressions' in row else 0
	actions['frequency'] = row['frequency'] if 'frequency' in row else 0
	actions['clicks'] = row['clicks'] if 'clicks' in row else 0
	actions['cpm'] = row['cpm'] if 'cpm' in row else 0
	actions['cpc'] = row['cpc'] if 'cpc' in row else 0
	actions['ctr'] = row['ctr'] if 'ctr' in row else 0
	actions['spend'] = row['spend'] if 'spend' in row else 0
	if row_key in dict_data:
		dict_data[row_key].update(actions)
	else:
		dict_data[row_key]=actions

csv_columns = ['date_start', 'date_stop']
csv_columns.extend(fields)


# Make request to get Actions
fields = [
	'adset_id',
	'adset_name',
	'actions',
	'action_values',
	'video_p100_watched_actions',
	'video_play_actions',
	'video_thruplay_watched_actions'
]
response = AdAccount('act_'+ad_account_id).get_insights(
  fields=fields,
  params=params
)
csv_columns.extend(['post_engagement_count','post_comment_count','post_reaction_count','post_share_count','sales_total_value','sales_total_count','sales_fp_on_value','sales_fp_on_count','sales_fp_of_value','sales_fp_of_count','sales_br_on_value','sales_br_on_count','sales_br_of_value','sales_br_of_count'])
for row in response:
	actions = {}
	row_key = row['adset_id']+"_"+row['date_start']
	row_key = str(row_key).encode('utf-8')
	row_key = hashlib.sha256(row_key).hexdigest()
	actions['adset_id'] = row['adset_id']
	actions['adset_name'] = row['adset_name'].replace(',',' ')
	actions['date_start'] = row['date_start']
	actions['date_stop'] = row['date_stop']
	if 'action_values' in row:
		for action in row['action_values']:
			if action['action_type'] == 'offline_conversion.custom.'+custom_conv_optim:
				column = 'sales_total_value'
			elif action['action_type'] == 'offline_conversion.custom.'+custom_conv_fp_on:
				column = 'sales_fp_on_value'
			elif action['action_type'] == 'offline_conversion.custom.'+custom_conv_fp_of:
				column = 'sales_fp_of_value'
			elif action['action_type'] == 'offline_conversion.custom.'+custom_conv_br_on:
				column = 'sales_br_on_value'
			elif action['action_type'] == 'offline_conversion.custom.'+custom_conv_br_of:
				column = 'sales_br_of_value'
			else:
				column = action['action_type'] + '_value'
			actions[column] = float(action['28d_view']) if '28d_view' in action else 0
			actions[column] = actions[column] + float(action['28d_click']) if '28d_click' in action else actions[column]
			actions[column] = action['value'] if actions[column] == 0 else actions[column]
	if 'actions' in row:
		for action in row['actions']:
			if action['action_type'] == 'offline_conversion.custom.'+custom_conv_optim:
				column = 'sales_total_count'
			elif action['action_type'] == 'offline_conversion.custom.'+custom_conv_fp_on:
				column = 'sales_fp_on_count'
			elif action['action_type'] == 'offline_conversion.custom.'+custom_conv_fp_of:
				column = 'sales_fp_of_count'
			elif action['action_type'] == 'offline_conversion.custom.'+custom_conv_br_on:
				column = 'sales_br_on_count'
			elif action['action_type'] == 'offline_conversion.custom.'+custom_conv_br_of:
				column = 'sales_br_of_count'
			else:
				column = action['action_type'] + '_count'
			actions[column] = float(action['28d_view']) if '28d_view' in action else 0
			actions[column] = actions[column] + float(action['28d_click']) if '28d_click' in action else actions[column]
			actions[column] = action['value'] if actions[column] == 0 else actions[column]
	if 'video_p100_watched_actions' in row:
		for action in row['video_p100_watched_actions']:
			column = 'video_complete_view_count'
			actions[column] = action['value']
	if 'video_play_actions' in row:
		for action in row['video_play_actions']:
			column = 'video_play_count'
			actions[column] = action['value']
	if 'video_thruplay_watched_actions' in row:
		for action in row['video_thruplay_watched_actions']:
			column = 'video_thruplay_watched_count'
			actions[column] = action['value']
	if row_key in dict_data:
		dict_data[row_key].update(actions)
	else:
		dict_data[row_key]=actions
	csv_columns.extend(x for x in actions.keys() if x not in csv_columns)


# Make request to get reach
fields = [
	'adset_id',
	'adset_name',
	'reach'
]
params = {
	'level': 'adset',
	'action_report_time': 'conversion',
	'time_increment': 'all_days',
	'time_range': {"since":start_time,"until":end_time}
}
response = AdAccount('act_'+ad_account_id).get_insights(
  fields=fields,
  params=params
)

for row in response:
	actions = {}
	row_key = row['adset_id']+"_"+row['date_start']
	row_key = str(row_key).encode('utf-8')
	row_key = hashlib.sha256(row_key).hexdigest()
	actions['adset_id'] = row['adset_id']
	actions['adset_name'] = row['adset_name'].replace(',',' ')
	actions['date_start'] = row['date_start']
	actions['reach'] = row['reach'] if 'reach' in row else 0
	if row_key in dict_data:
		dict_data[row_key].update(actions)
	else:
		dict_data[row_key]=actions

csv_columns.extend(x for x in actions.keys() if x not in csv_columns)


strFolder = '/nfs/science/tesco_uk/offsite/FB_raw_insights/'
sep = ','
header = sep.join(csv_columns)
f1 = open(strFolder + "insights_" + brand + "_" + dh_campaign_id + "_" + strToday + ".csv", "w+")
f1.write(header)
for row in dict_data:
	rowstr = '\n'
	for column in csv_columns:
		if column in dict_data[row]:
			rowstr = rowstr + str(dict_data[row][column]) + ','
		else:
			rowstr = rowstr + ','
	f1.write(rowstr[:-1])
f1.close() 

