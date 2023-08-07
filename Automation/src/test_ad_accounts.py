access_token = 'EAADwubHpNPoBAJyUwGzciZBjsha3pZAvjpJmUwoqcfLQnjI56CxGykci7ziyjCi8408FTz3D1jvIFG0Um4IMguNE7dxeZAnozX9sNm8SGh0oxdfGLaPhdVqBzYRYMmrqcvb8cILBdfyXpJBZCAHzxVGJRlxRd4RqNGfcyAeZAqRbAUUZBfOBH8S6Sp617qwknceob7T43s3wZDZD'
app_secret = '1d9a17e56a843e59a18f873032b48a3f'
app_id = '264680344466682'

import sys
sys.path.append(r'Users\damodarr\AppData\Local\Programs\Python\Python37\Lib\site-packages') # Replace this with the place you installed facebookads using pip
sys.path.append(r'Users\damodarr\AppData\Local\Programs\Python\Python37\Lib\site-packages\facebook_business-6.0.2.dist-info') # same as above

from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.api import FacebookAdsApi
from facebook_business import FacebookSession
from facebook_business.adobjects.adaccountuser import AdAccountUser as AdUser

### Setup session ###
session = FacebookSession(app_id,app_secret,access_token)
api = FacebookAdsApi(session)

if __name__ == '__main__':
	FacebookAdsApi.set_default_api(api)

    ### Setup user and pull the ad accounts ###
	me = AdUser(fbid='me')
	fields = []
	params = {}
	ad_accounts = []
	my_accounts_iterator = me.get_ad_accounts()
	print('Generating the list of accounts')
	
	for account in my_accounts_iterator:
		print(account["id"] + ",")
		ad_accounts.append(account["id"])
	
	print(ad_accounts)



