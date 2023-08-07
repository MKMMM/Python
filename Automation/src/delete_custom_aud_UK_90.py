# Delete all custom audiences from the FB business manager greater tha 90 days 

access_token = 'EAADwubHpNPoBAJyUwGzciZBjsha3pZAvjpJmUwoqcfLQnjI56CxGykci7ziyjCi8408FTz3D1jvIFG0Um4IMguNE7dxeZAnozX9sNm8SGh0oxdfGLaPhdVqBzYRYMmrqcvb8cILBdfyXpJBZCAHzxVGJRlxRd4RqNGfcyAeZAqRbAUUZBfOBH8S6Sp617qwknceob7T43s3wZDZD'
app_secret = '1d9a17e56a843e59a18f873032b48a3f'
app_id = '264680344466682'

import sys
sys.path.append(r'Users\damodarr\AppData\Local\Programs\Python\Python37\Lib\site-packages') # Replace this with the place you installed facebookads using pip
sys.path.append(r'Users\damodarr\AppData\Local\Programs\Python\Python37\Lib\site-packages\facebook_business-6.0.2.dist-info') # same as above
import datetime
import dateutil.parser
import pytz
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adaccountactivity import AdAccountActivity
from facebook_business.adobjects.customaudience import CustomAudience
from facebook_business.adobjects.abstractobject import AbstractObject
from facebook_business.api import FacebookAdsApi
from facebook_business import FacebookSession
from facebook_business.adobjects.adaccountuser import AdAccountUser as AdUser
import json
import os

### Setup session ###
session = FacebookSession(app_id,app_secret,access_token)
api = FacebookAdsApi(session)

if __name__ == '__main__':
    FacebookAdsApi.set_default_api(api)

    ### Pull the ad accounts and custom audiences ###
    me = AdUser(fbid='me')
    fields = [
        'currency',
        'name']
    params = {}
    my_accounts_iterator = me.get_ad_accounts(fields=fields,params=params,)
    print('Generating the list of accounts')
    for account in my_accounts_iterator:
        if account["currency"] == "GBP":
            id = account["id"]
            ad_account_name = account["name"]
            FacebookAdsApi.init(access_token=access_token)
            account = AdAccount(id)
            fields = [
            'time_created',
            'name']
            params = {}
            custom_audiences = account.get_custom_audiences(fields=fields,params=params,)
            length = len(custom_audiences)
            # Remove the custom audience greater than 90 days
            for i in range(length):

                time_created = custom_audiences[i]['time_created']
                cust_aud_name = custom_audiences[i]['name']
                convert_iso = datetime.datetime.fromtimestamp(time_created).isoformat()
                diffretiation = pytz.utc.localize(datetime.datetime.utcnow()) - dateutil.parser.parse(f'{convert_iso}.065Z')
                if diffretiation.days>90:
                    cust_aud = custom_audiences[i]['id']
                    #custom_audience_delete = CustomAudience(cust_aud).api_delete()
                    print(f'The custom Audience ID {cust_aud} from the ad account {ad_account_name} has been deleted')
                else:
            	    pass
