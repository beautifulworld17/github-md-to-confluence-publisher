import argparse
import logging
from atlassian import Confluence

from config.getconfig import get_config
from pagesController import get_child_pages_info 
from pagesPublisher import publish_folder, publish_page, update_pages, publish_parent_page

logging.basicConfig(level=logging.INFO)

CONFIG = get_config()

confluence_url = str(CONFIG["confluence_url"])
confluence_space_id = str(CONFIG["confluence_space"])
md_files_path = str(CONFIG["github_folder_with_md_files"])
confluence_parent_page_id = str(CONFIG["confluence_parent_page_id"])
git_repo_name = str(CONFIG["git_repo_name"])


logging.info(CONFIG)

# Parse arguments with user_id and user_token for Confluence
parser = argparse.ArgumentParser()
parser.add_argument('--user', '-u', help='user ID is mandatory', required=True)
parser.add_argument('--token', '-t', help='API token is mandatory',  required=True)
parser.add_argument('--upload-all', help='takes either true or false, deletes all the current pages if any and Uploads all *.md files from the folder', default=False)
parser.add_argument('--added-files')
parser.add_argument('--deleted-files')
parser.add_argument('--modified-files')

args = parser.parse_args()
input_arguments = vars(args)

user_id = input_arguments['user']
user_token = input_arguments['token']
added_pages_list = str(input_arguments['added_files']).split(',') if input_arguments['added_files'] else None
deleted_pages_list = str(input_arguments['deleted_files']).split(',') if input_arguments['deleted_files'] else None
modified_pages_list = str(input_arguments['modified_files']).split(',') if input_arguments['modified_files'] else None


confluence = Confluence(url=confluence_url, username=user_id, password=user_token, verify_ssl=False)


if str(args.upload_all).lower() == "true":
    child_pages_info = get_child_pages_info(user_id=user_id, user_token=user_token)
    logging.info("Found these pages in the Space: " + str(child_pages_info))
    if child_pages_info:
        for page_info in child_pages_info:
            logging.info("Deleting page along with it's child pages ID: "+ str(page_info["id"]) + "   Title: " + str(page_info["title"]))
            confluence.remove_page(page_info["id"], status=None, recursive=True)

    publish_folder(folder=md_files_path, confluence=confluence)
    exit(0)


if added_pages_list:
    for page in added_pages_list:
        if not page.__contains__('/'): # check if page is in the repo directory
            publish_page(filepath=md_files_path+'/'+page, confluence=confluence, 
                         parent_page_id=confluence_parent_page_id, repo_name=git_repo_name)
        else:
            parent_page, page_title = page.split('/', 1)
            parent_id = confluence.get_page_id(confluence_space_id, parent_page)

            if parent_id: # If parent page is available, then publish under it
                logging.info("creating new page with the Parent ID: " + parent_page +"  Page Title: " +  page_title)
                publish_page(filepath=md_files_path+page, confluence=confluence, 
                             parent_page_id=parent_id)
            else: # If parent page is not available, then create parent page first and then create child page under it
                logging.info("creating new parent page: " +  parent_page)
                new_parent_id = publish_parent_page(confluence=confluence, page_title=parent_page)
                publish_page(filepath=md_files_path+page, confluence=confluence, parent_page_id=new_parent_id)


if modified_pages_list:
    for page in modified_pages_list:
        if page.__contains__('/'):
            logging.info("Updating page: " +  page)
            update_pages(modified_page=page, confluence=confluence)
        else:
            logging.info("Updating page in repo directory: " +  git_repo_name+page)
            update_pages(modified_page=page, confluence=confluence, repo_name=git_repo_name)


if deleted_pages_list:
    for page in deleted_pages_list:
        if page.__contains__('/'):
            logging.info("Deleting page: " + page)
            page_id = confluence.get_page_id(confluence_space_id, page)
            confluence.remove_page(page_id)
        else: # delete page in the repo directory
            logging.info("Deleting page: " + git_repo_name+page)
            page_id = confluence.get_page_id(confluence_space_id, git_repo_name+page)
            confluence.remove_page(page_id)