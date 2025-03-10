import os
import requests
from typing import Dict, Any
# Import libraries for loading codemeta file and running codemeticulous validator
import pydantic
from codemeticulous.cli import load_and_create_model
from codemeticulous.convert import STANDARDS

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

def run_codemeticulous_validation(codemeta_file,codemeta_metadata):
    """
    Validates the Codemeta JSON file using `codemeticulous` directly in Python.
    """

    codemeta_filename = os.path.basename(codemeta_file)

    # see if codemeta is valid
    try:
        model = STANDARDS['codemeta']["model"]  # Get Pydantic model for codemeta V3
        model(**codemeta_metadata)

        log_msg = f"{codemeta_filename} is a valid codemeta file."

        return True, log_msg

    except pydantic.v1.error_wrappers.ValidationError as e:

        log_msg = f"{codemeta_filename} is not a valid codemeta file. {e}"
        # if invalid codemeta file show errors in logs
        return False, log_msg


