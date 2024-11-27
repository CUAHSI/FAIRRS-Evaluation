import requests

def get_fairsoft_scores_and_evaluation(metadata):
    """
    
    Retrieves FAIRsoft results and evaluation through metadata input into the Software Observatory API.
    
    """


    # remove the 'version' field -- not sure why but this field is not recognized in payload,
    # even though value is empty list
    if 'version' in metadata:
        del metadata['version']
        # add version control field (R.4.1) and set to True
        metadata['version_control'] = True


    endpoint_url = 'https://observatory.openebench.bsc.es/api/fair/evaluate'

    # define payload and content type headers
    payload = {
        'tool_metadata': metadata
    }
    headers = {
        'Content-Type': 'application/json'
    }
    
    try:
        # get the response
        response = requests.post(endpoint_url,json=payload,headers=headers)
        response.raise_for_status()

        if response.status_code == 200:
            # extract the json response
            json_response = response.json()

            if json_response['result'] is not None:
                # retrieve the results and logs
                results = json_response['result']
                logs = json_response['logs']
                return results,logs
            
            else:
                print('Error in obtaining FAIRsoft evaluation results.')
                return None

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")        