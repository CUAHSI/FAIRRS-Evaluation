import os
import requests
import urllib.parse as urlparse


def get_github_repo_and_owner(url):
    """
    
    Parses github url input (string) into repository and owner name.
    
    """

    # get path from url
    path = urlparse.urlparse(url).path
    # split the path into head (owner) and tail (repo)
    owner_name, repo_name = os.path.split(path)
    # remove leading slash from owner
    owner_name = owner_name.lstrip("/")

    return owner_name, repo_name


def get_installation_id(url):
    """
    
    Retrieves installation ID of GitHub for Metadata Extractor App; this must be installed in user workspace
    with read access to input repository.
    
    """
    
    # parse repository and owner names for feeding into the GitHub Metadata Extractor API
    owner_name, repo_name = get_github_repo_and_owner(url)

    # api endpoint to retrieve Metadata Extractor installation id
    endpoint_url = f'https://observatory.openebench.bsc.es/github-metadata-api/metadata-extractor-for-fairsoft/installation/id?owner={owner_name}&repo={repo_name}'

    try:
        # get the response
        response = requests.get(endpoint_url)
        response.raise_for_status()

        if response.status_code == 200:
            # extract the json reponse
            json_response = response.json()

            # 'data' field is null if the app is not installed with owner's repository
            if json_response['data'] is not None:
                installation_id = json_response['data']['data']['id']
                return installation_id,owner_name,repo_name
            
            else:
                print('Need to install Metadata Extractor for FairSoft GitHub app.')
                return None

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")
