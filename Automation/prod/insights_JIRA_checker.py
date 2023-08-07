#! /usr/bin/python3
import yaml
import os
from pathlib import Path
from jira import JIRA
from methods.jiraExportMethods import DhJiraClient

if __name__ == "__main__":

    app_root_folder = Path(__file__).parent
    app_config_file_path = Path(f'{app_root_folder}/config/config.yaml')
    configFolder = '/nfs/science/tesco_uk/OFFSITE/AudienceTest/Config/Done/'
    myScriptFolder = '/nfs/science/tesco_uk/OFFSITE/jiraScripts/audience/prod/'
   
   # INIT CONFIG FILE
    with app_config_file_path.open(mode="r") as config_file:
        app_config = yaml.load(config_file, Loader=yaml.FullLoader)
    
    # JIRA API CREDENTIALS
    jira_api_credentials = {
        "consumer_key": os.environ.get("JIRA_OAUTH_CONSUMER_KEY"),
        "access_token": os.environ.get("JIRA_OAUTH_TOKEN"),
        "access_token_secret": os.environ.get("JIRA_OAUTH_SECRET"),
        "key_cert": Path(os.environ.get("JIRA_OAUTH_KEY_PATH")).read_text()
    }
    
    # INIT JIRA CLIENT
    jira_client = DhJiraClient(jira_api_credentials)
    search_parameters = app_config.get("jira", {}).get("search_parameters")
    
    assert search_parameters, "Please add search parameters to config file"
    
    # Search campaigns with label 'ready_for_insights' and not with label 'insights_generated'
    jql = f"Project = {search_parameters.get('project')} AND Type in ({search_parameters.get('issue_types')})" \
          f"AND Labels in (\"ready_for_insights\") AND Labels not in(\"insights_generated\") "
    
    campaigns = jira_client.search_issues(jql=jql, fields=','.join([
        v for k, v in search_parameters.get("fields").items()]))
    
    fields = search_parameters.get("fields")
    # Per campaign:
    for campaign in campaigns:
        # Most of the time campaign name is entered in Jira card summary and not campaign name
        campaign_id = getattr(campaign.fields, fields.get("campaign_id"))
        if not campaign_id:
            campaign.update(notify=False, fields={str(fields.get("campaign_id")): str(campaign.fields.summary)})
        
        brand = getattr(campaign.fields, fields.get("brand"))
        if not brand:
            campaign.update(notify=False, fields={str(fields.get("brand")): str(campaign.fields.summary)})
        
        #Run the following command
        print("Brand: " + brand)
        print("Campaign ID: " + str(campaign_id))

        print("python3 get_insights.py "+ configFolder + "config_" + "*" + str(campaign_id) + ".ini")
        os.system("python3 "+ myScriptFolder + "get_insights.py "+ configFolder + "config_" + "*" + str(campaign_id) + ".ini")

        # Add new label
        campaign.fields.labels.append("insights_generated")
        campaign.update(fields={"labels": campaign.fields.labels})
