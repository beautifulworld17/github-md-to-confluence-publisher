import requests

from urllib3.exceptions import InsecureRequestWarning
from requests.auth import HTTPBasicAuth
from config.getconfig import get_config

CONFIG = get_config()

confluence_parent_page_id = str(CONFIG["confluence_parent_page_id"])

# Suppress only the single warning from urllib3.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

def get_child_pages_info(user_id, user_token, page_id=confluence_parent_page_id):
    '''
    Fetches the child page ID and Title
    '''
    # Set the Confluence REST API endpoint for getting child pages
    child_pages_url = str(CONFIG["confluence_url"]) + "/wiki/rest/api/content/" + page_id + "/child/page"

    # Authenticate with Confluence using HTTP Basic Authentication
    auth = HTTPBasicAuth(user_id, user_token)

    try:
        # Get the list of child pages
        response = requests.get(child_pages_url, auth=auth, verify=False)
        response.raise_for_status()
        child_pages = response.json().get("results", [])

        # Extract child page ID and title
        child_pages_info = [{"id": child_page["id"], "title": child_page["title"]} for child_page in child_pages]

        return child_pages_info

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None