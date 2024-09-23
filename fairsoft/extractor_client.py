import requests


def get_installation_id(repo_name,owner_name):

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
                return installation_id
            
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
