# Publish Markdown files from GitHub to Confluence

This directory contains the scripts that allows you to publish Markdown files from GitHub to Confluence. The script automates the process of converting Markdown files to Confluence markup and uploading them to your Confluence space.

## Pre-requsiste
Confluence API expects mail ID as an username and an API Key.  
New API key can be created here https://id.atlassian.com/manage-profile/security/api-tokens

## Setup
### Configure the publisher in ./config/config.yaml

Example config file. Replace with your values.

``` yaml

confluence_url: https://mysample.atlassian.net
confluence_space: SA
confluence_parent_page_id: 4209312081
github_folder_with_md_files: ../../
git_repo_name: node-app/

```
`confluence_url` :   
Domain name of the confluence  

`confluence_space` :   
Create a new Space or if Space already exists, copy it's ID from the URL.  
For the URL: https://mysample.atlassian.net/wiki/spaces/SA/overview?homepageId=691700225  
Space ID would be `SA`

`confluence_parent_page_id` :   
Create a new page in the required Space and copy it's ID from the URL.  
For the URL: https://mysample.atlassian.net/wiki/spaces/SA/pages/4209312081/Salt-States+Documentations+Source+GitHub
Page ID would be `4209312081`

`github_folder_with_md_files` :   
Relative path to the parent directory, where all *.md files are available under it.

`git_repo_name` :   
Name of the GitHub repository or parent directory name.

## How to Run

``` bash
python3 ./main.py [-h] --user USER --token TOKEN [--upload-all UPLOAD_ALL] [--added-files ADDED_FILES][--deleted-files DELETED_FILES] [--modified-files MODIFIED_FILES]  

options:
  -h, --help                      show this help message and exit
  --user USER, -u USER            user ID is mandatory
  --token TOKEN, -t TOKEN         API token is mandatory
  --upload-all UPLOAD_ALL         takes either true or false
  --added-files ADDED_FILES       comma separated list of newly added files
  --deleted-files DELETED_FILES   comma separated list of deleted files
  --modified-files MODIFIED_FILES comma separated list of modified files
```

### Example usage
There are 2 ways to run:  
1. Using **--upload-all** argument: It will delete all the currently uploaded pages under the specified parent in config file (`confluence_parent_page_id`) and re-uploads all *.md files from the directory (`github_folder_with_md_files`)
``` bash
python3 ./main.py \
--user user@email.com \
--token ATATT3xFfGF00 \
--upload-all true

```
2. By providing list of files to newly add or delete or update the content. This can be used to implement pipeline using the GitHub action workflow.  
   Sample workflow: https://github.com/beautifulworld17/github-md-to-confluence-publisher/blob/main/sample-workflow.yml

```bash
python3 ./main.py \
--user user@email.com \
--token ATATT3xFfGF00 \
--modified-files _runners/README.md,bind/master/README.md \
--added-files sct/readme-sct.md \
--deleted-files ans/README.md
```