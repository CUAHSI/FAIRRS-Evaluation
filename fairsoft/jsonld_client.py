import requests

def get_jsonld_metadata(metadata):

    endpoint_url = 'https://observatory.openebench.bsc.es/api/tools/jsonld'

    payload = {
        'tool_metadata': metadata
    }

    response = requests.post(endpoint_url,data=payload)

    try:
        # get the response
        response = requests.get(endpoint_url)
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