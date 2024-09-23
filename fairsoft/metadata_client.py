import requests

def get_repository_metadata(repo_name,owner_name,installation_id):

    endpoint_url = 'https://observatory.openebench.bsc.es/github-metadata-api/metadata'

    payload = {
        'repo': repo_name,
        'owner': owner_name,
        'installationID': installation_id
    }

    try:
        # get the response
        response = requests.post(endpoint_url,data=payload)
        response.raise_for_status()

        if response.status_code == 200:
            # extract the json response
            json_response = response.json()

            # 'data' field is null if the app is not installed with owner's repository
            if json_response['data'] is not None:
                metadata = json_response['data']
                return metadata
            
            else:
                print('Error in retrieving tool metadata.')
                return None

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")

