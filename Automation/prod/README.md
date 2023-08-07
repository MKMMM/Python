# Audience config file & Jira

## Prerequisites

### Jira api credentials

Once you have your jira api credentials, create the following environment variables:
*  JIRA_OAUTH_CONSUMER_KEY: Jira Oauth Consumer Key
*  JIRA_OAUTH_TOKEN: Jira Oauth access token
*  JIRA_OAUTH_SECRET: Jira Oauth access token secret
*  JIRA_OAUTH_KEY_PATH (private SSH key, should be the same than the one used during the creation of jira API credentials)

Update environment variable names in app.py if you used different names

### Config file
Create `config.yaml` file and add it to the `./config` folder
Update the `config.yaml` file content with the template below

#### Config file template
```
jira:
  search_parameters:
    project: TDT
    issue_types: Campaign,Story
    fields:
      summary: summary
      campaign_name: customfield_14682
      campaign_id: customfield_14683
      event_source_id: customfield_15890
      ad_account_id: customfield_15891

file-config:
  destination-path: /nfs/science/...
  name: config_[campaign_id].ini
  content: |
    [DEFAULT]
    BUSINESS_MANAGER_ID = 580032172157635
    APP_ID =
    APP_SECRET =
    ACCESS_TOKEN =

    [CAMPAIGN]

    # Add campaign details in this section.
    # Possible values for CAMPAIGN_OBJECTIVE: REACH - CONVERSIONS - LINK_CLICKS - POST_ENGAGEMENT - VIDEO_VIEWS

    AD_ACCOUNT_ID = [ad_account_id]
    DH_CAMPAIGN_ID = [campaign_id]
    EVENT_SOURCE_ID = [event_source_id]
    CAMPAIGN_NAME = [campaign_name]

    ...
```

## Usage

### Run script
Run `python3 ./app.py`

### Add more placeholders to the file config content
#### Update the `config.yaml` file
##### Update jira -> search_parameters -> fields
*  Add the place holder name as key and the custom field ID from Jira (e.g. campaign_name:customfield_14682)

##### Update file-config -> content
* Add the place holder to the config file content (e.g. [campaign_name])
