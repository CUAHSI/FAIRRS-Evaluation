import requests

def get_jsonld_metadata(metadata):
    """
    
    Returns JSON-LD file from metadata input for updating metadata in the GitHub repository.
    
    """

    # remove the 'version' field -- not sure why but this field is not recognized
    if 'version' in metadata:
        del metadata['version']

    endpoint_url = 'https://observatory.openebench.bsc.es/api/tools/jsonld'

    # define payload and content type headers
    payload = {
        'data': metadata
    }
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        # get the response
        response = requests.post(endpoint_url,data=payload,headers=headers)
        response.raise_for_status()

        if response.status_code == 200:
            # extract the json response
            json_response = response.json()

            if json_response is not None:
                # retrieve the json-ld
                return json_response
            
            else:
                print('Error in obtaining JSON-LD.')
                return None

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")      