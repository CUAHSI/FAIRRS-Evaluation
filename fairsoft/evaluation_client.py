import requests

def get_fairsoft_results_and_logs(metadata):

    endpoint_url = 'https://observatory.openebench.bsc.es/api/fair/evaluate'

    payload = {
        'tool_metadata': metadata
    }

    try:
        # get the response
        response = requests.post(endpoint_url,data=payload)
        response.raise_for_status()

        if response.status_code == 200:
            # extract the json response
            json_response = response.json()
            print(json_response)
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