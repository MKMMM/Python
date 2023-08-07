
#! /usr/bin/python

import sys
sys.path.append('/lib/python3.6/site-packages/facebook_business') # Replace this with the place you installed facebookads using pip
sys.path.append('/lib/python3.6/site-packages/facebook_business/facebook_business-3.0.0-py2.7.egg-info') # same as above


from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount

import argparse
import configparser
# config = configparser.ConfigParser()
# config.read('config_campaign.ini')

parser = argparse.ArgumentParser(description="Create a skeleton campaign on Facebook and adding a custom audience file with it.")
parser.add_argument("audience_name",  help="audience name in platform", metavar="DOM_12345_PR_PB")
parser.add_argument("custom_audience_id",  help="audience id in platform", metavar="1234567890")
parser.add_argument("config_file",  help="config file", metavar="config.ini")
args = parser.parse_args()

config = configparser.ConfigParser()
config.read(args.config_file)

business_manager_id = config.get('DEFAULT', 'BUSINESS_MANAGER_ID')
app_id = config.get('DEFAULT', 'APP_ID')
app_secret = config.get('DEFAULT', 'APP_SECRET')
access_token = config.get('DEFAULT', 'ACCESS_TOKEN')


if(len(args.audience_name) > 128):
    strCustomAudienceName = args.audience_name.split('_')[6]
    strCustomAudienceName = strCustomAudienceName[32:-32]
else:
    strCustomAudienceName = args.audience_name


ad_account_id = config.get('CAMPAIGN', 'AD_ACCOUNT_ID')
fb_page_id = config.get('CAMPAIGN', 'FB_PAGE_ID')
campaign_name = config.get('CAMPAIGN', 'CAMPAIGN_NAME') + strCustomAudienceName
dh_campaign_id =  config.get('CAMPAIGN', 'DH_CAMPAIGN_ID')
campaign_objective =  config.get('CAMPAIGN', 'CAMPAIGN_OBJECTIVE').upper()
#campaign_objective = REACH
start_time =  config.get('CAMPAIGN', 'START_DATE')
end_time =  config.get('CAMPAIGN', 'END_DATE')
budget =  float("1.00") * 100
ad_set_name =  config.get('CAMPAIGN', 'CAMPAIGN_NAME') + strCustomAudienceName
max_frequency =  config.get('CAMPAIGN', 'FREQUENCY_CAP')
max_frequency = str(max_frequency).split(".")[0]
# audience_id =  config.get('CAMPAIGN', 'AUDIENCE_ID')
audience_id =  args.custom_audience_id

custom_conversion_id =  config.get('INSIGHTS', 'CUSTOM_CONV_OPTIM')

if campaign_objective == "CONVERSIONS":
  adset_objective = "OFFSITE_CONVERSIONS"
elif campaign_objective == "VIDEO_VIEWS":
  adset_objective = "THRUPLAY"
else:
  adset_objective = campaign_objective

# Start Facebook API and get ad account
FacebookAdsApi.init(app_id, app_secret, access_token)
ad_account = AdAccount('act_'+ad_account_id)

# Create campaign
fields = [
]
params = {
  'name': campaign_name,
  'objective': campaign_objective,
  'lifetime_budget': budget,
  'bid_strategy': 'LOWEST_COST_WITHOUT_CAP',
  'status': 'PAUSED',
  'special_ad_categories': ['NONE']
}
campaign = ad_account.create_campaign(
  fields=fields,
  params=params,
)
campaign_id = campaign['id']

# Create adsets
fields = [
]
params = {
  'campaign_id': campaign_id,
  'name': ad_set_name,
  'start_time': start_time,
  'end_time': end_time,
  'billing_event': 'IMPRESSIONS',
  'optimization_goal': adset_objective,
  'targeting': {"custom_audiences": [{"id":audience_id}], "geo_locations":{"countries":["GB"]}, "publisher_platforms":["facebook", "instagram"], "facebook_positions":["feed", "right_hand_column", "instant_article", "instream_video"], "instagram_positions":["stream"], "brand_safety_content_filter_levels":["FACEBOOK_STANDARD", "AN_STRICT"]},
  'status': 'PAUSED',
  
}
if campaign_objective == "CONVERSIONS":
  params['promoted_object'] = {"custom_conversion_id":custom_conversion_id}
  params['attribution_spec'] = [{'event_type':'CLICK_THROUGH','window_days':7},{'event_type':'VIEW_THROUGH','window_days':1}]
elif campaign_objective == "REACH":
  params['frequency_control_specs'] = [{"event": "IMPRESSIONS", "interval_days":7, "max_frequency":max_frequency}]
else:
  params['promoted_object'] = {"page_id":fb_page_id}

ad_set = ad_account.create_ad_set(
  fields=fields,
  params=params,
)
ad_set_id = ad_set['id']

print("campaign created with id "+campaign_id+" \n")
print("adset created with id "+ad_set_id+" \n")

