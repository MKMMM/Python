#! /usr/bin/python3
import yaml
import os
from pathlib import Path
from jira import JIRA
from methods.jiraExportMethods import DhJiraClient

if __name__ == "__main__":

    app_root_folder = Path(__file__).parent
    app_config_file_path = Path(f'{app_root_folder}/config/config.yaml')
    
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
    
    # Search campaigns with label 'ready_for_config' and not with label 'config_generated'
    jql = f"Project = {search_parameters.get('project')} AND Type in ({search_parameters.get('issue_types')})" \
          f"AND Labels in (\"ready_for_config\") AND Labels not in(\"config_generated\") "
    
    campaigns = jira_client.search_issues(jql=jql, fields=','.join([
        v for k, v in search_parameters.get("fields").items()]))
    
    file_config = app_config["file-config"]
    fields = search_parameters.get("fields")

    # Per campaign:
    for campaign in campaigns:
        # Most of the time campaign name is entered in Jira card summary and not campaign name
        campaign_name = getattr(campaign.fields, fields.get("campaign_name").replace(" ","_").replace("'","").replace("&","").replace("%",""))
        if not campaign_name:
            campaign.update(notify=False, fields={str(fields.get("campaign_name")): str(campaign.fields.summary)})
    
        # Init campaign filename and file content
        campaign_file_name, campaign_file_content = file_config["name"], file_config["content"]

        # Update placeholders by campaign field values e.g. [campaign_name] should be replaced by
        # campaign.fields.customfield_14682
        for k, v in fields.items():
            place_holder = f"[{k}]"
            field_value = getattr(campaign.fields, v) if getattr(campaign.fields, v) is not None else ''
            field_value = ','.join(field_value) if type(field_value) == list else field_value
            campaign_file_content = campaign_file_content.replace(place_holder, str(field_value))
            campaign_file_name = campaign_file_name.replace(place_holder, str(field_value)).replace(" ","").replace("'","").replace("&","").replace("%","")
    
        # Create file and add content
        Path(f"{file_config['destination-path']}{campaign_file_name}").write_text(campaign_file_content)

        # Add new label
        campaign.fields.labels.append("config_generated")
        campaign.update(fields={"labels": campaign.fields.labels})
