import requests
from typing import Dict, Any


def check_for_operational_url(url: str, timeout_val = 10) -> Dict[str, Any]:
    """
    Checks if a URL resolves successfully using an HTTP HEAD request.
    """

    try: 
        # perform a head request to see if url is operational
        response = requests.head(url, allow_redirects=True, timeout=timeout_val)
        status_code = response.status_code

        log = f'Status code for {url} = {status_code}'

        # Check if the response status code is in the range of 200-299
        if status_code >= 200 and status_code < 300:
            return True,log + ' -- URL is operational'  # URL is operational
        else:
            return False,log + ' -- URL is not operational'  # URL is NOT operational
    
    except requests.RequestException as e:
        return False,e + ' -- URL is NOT operational'  # URL is not operational


