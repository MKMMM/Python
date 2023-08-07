#! /usr/bin/python

import sys
sys.path.append('/nfs/shared/py_packages/facebook-python') # Replace this with the place you installed facebookads using pip
sys.path.append('/nfs/shared/py_packages/facebook-python') # same as above

from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
import argparse 
import configparser
import logging
from logging.handlers import TimedRotatingFileHandler

import sys
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
config.optionxform = lambda option: option
config.read(args.config_file)

business_manager_id = config.get('DEFAULT', 'BUSINESS_MANAGER_ID')
app_id = config.get('DEFAULT', 'APP_ID')
app_secret = config.get('DEFAULT', 'APP_SECRET')
access_token = config.get('DEFAULT', 'ACCESS_TOKEN')

ad_account_id = config.get('CAMPAIGN', 'AD_ACCOUNT_ID')
campaign_name = config.get('CAMPAIGN', 'CAMPAIGN_NAME')
dh_campaign_id =  config.get('CAMPAIGN', 'DH_CAMPAIGN_ID')
event_source_id = config.get('CAMPAIGN', 'EVENT_SOURCE_ID')

# Start Facebook API and get ad account
FacebookAdsApi.init(app_id, app_secret, access_token)
ad_account = AdAccount('act_'+ad_account_id)

# Create custom conversion for optimization
fields = [
]
params = {
  'name': campaign_name,
  'event_source_id': event_source_id,
  'custom_event_type': 'OTHER',
  'rule':'{"custom_data.dh1":{"eq":"'+dh_campaign_id+'"}}'
}
custom_conversion = ad_account.create_custom_conversion(
  fields=fields,
  params=params,
)
custom_conversion_id = custom_conversion['id']

# Create custom conversion for offline brand sales
fields = [
]
params = {
  'name': campaign_name+'_UsGrt25StE_cyqvM5zTBj',
  'event_source_id': event_source_id,
  'custom_event_type': 'OTHER',
  'rule':'{"and": [{"custom_data.dh1":{"eq":"'+dh_campaign_id+'"}},{"custom_data.dh3":{"eq":"UsGrt25StE"}},{"custom_data.dh2":{"eq":"cyqvM5zTBj"}}]}'
}
custom_conversion = ad_account.create_custom_conversion(
  fields=fields,
  params=params,
)
custom_conversion_id2 = custom_conversion['id']

# Create custom conversion for offline featured product sales
fields = [
]
params = {
  'name': campaign_name+'_UsGrt25StE_JB6WbLPtQu',
  'event_source_id': event_source_id,
  'custom_event_type': 'OTHER',
  'rule':'{"and": [{"custom_data.dh1":{"eq":"'+dh_campaign_id+'"}},{"custom_data.dh3":{"eq":"UsGrt25StE"}},{"custom_data.dh2":{"eq":"JB6WbLPtQu"}}]}'
}
custom_conversion = ad_account.create_custom_conversion(
  fields=fields,
  params=params,
)
custom_conversion_id3 = custom_conversion['id']

# Create custom conversion for online brand sales
fields = [
]
params = {
  'name': campaign_name+'_Nzyp4HHS3Z_cyqvM5zTBj',
  'event_source_id': event_source_id,
  'custom_event_type': 'OTHER',
  'rule':'{"and": [{"custom_data.dh1":{"eq":"'+dh_campaign_id+'"}},{"custom_data.dh3":{"eq":"Nzyp4HHS3Z"}},{"custom_data.dh2":{"eq":"cyqvM5zTBj"}}]}'
}
custom_conversion = ad_account.create_custom_conversion(
  fields=fields,
  params=params,
)
custom_conversion_id4 = custom_conversion['id']

# Create custom conversion for online featured product sales
fields = [
]
params = {
  'name': campaign_name+'_Nzyp4HHS3Z_JB6WbLPtQu',
  'event_source_id': event_source_id,
  'custom_event_type': 'OTHER',
  'rule':'{"and": [{"custom_data.dh1":{"eq":"'+dh_campaign_id+'"}},{"custom_data.dh3":{"eq":"Nzyp4HHS3Z"}},{"custom_data.dh2":{"eq":"JB6WbLPtQu"}}]}'
}
custom_conversion = ad_account.create_custom_conversion(
  fields=fields,
  params=params,
)
custom_conversion_id5 = custom_conversion['id']

print("\nCustom conversion for optimization CUSTOM_CONV_OPTIM: " + custom_conversion_id)
logger.info("\nCustom conversion for optimization CUSTOM_CONV_OPTIM: " + custom_conversion_id + " was created for: " + campaign_name)

print("\nCustom conversion for optimization CUSTOM_CONV_BR_OF_UsGrt25StE_cyqvM5zTBj: " + custom_conversion_id2)
logger.info("\nCustom conversion for optimization CUSTOM_CONV_BR_OF_UsGrt25StE_cyqvM5zTBj: " + custom_conversion_id2 + " was created for: " + campaign_name)

print("\nCustom conversion for optimization CUSTOM_CONV_FP_OF: _UsGrt25StE_JB6WbLPtQu: " + custom_conversion_id3)
logger.info("\nCustom conversion for optimization CUSTOM_CONV_FP_OF_UsGrt25StE_JB6WbLPtQu:  " + custom_conversion_id3 + " was created for: " + campaign_name)

print("\nCustom conversion for optimization: CUSTOM_CONV_BR_ON_Nzyp4HHS3Z_cyqvM5zTBj: " + custom_conversion_id4)
logger.info("\nCustom conversion for optimization CUSTOM_CONV_BR_ON_Nzyp4HHS3Z_cyqvM5zTBj: " + custom_conversion_id4 + " was created for: " + campaign_name)

print("\nCustom conversion for optimization CUSTOM_CONV_FP_ON _Nzyp4HHS3Z_JB6WbLPtQu: " + custom_conversion_id5)
logger.info("\nCustom conversion for optimization _Nzyp4HHS3Z_JB6WbLPtQu: " + custom_conversion_id5 + " was created for: " + campaign_name)

config.add_section('INSIGHTS')
config.set('INSIGHTS', 'CUSTOM_CONV_OPTIM', custom_conversion_id)
config.set('INSIGHTS', 'CUSTOM_CONV_FP_ON', custom_conversion_id5)
config.set('INSIGHTS', 'CUSTOM_CONV_FP_OF', custom_conversion_id3)
config.set('INSIGHTS', 'CUSTOM_CONV_BR_ON', custom_conversion_id4)
config.set('INSIGHTS', 'CUSTOM_CONV_BR_OF', custom_conversion_id2)


with open(args.config_file, 'w') as f:
    config.write(f)

print("Conversion IDs were written to: " + args.config_file)
