import os
import sys
import json
import requests
from typing import Dict, Any
# Import libraries for loading codemeta file and running codemeticulous validator
import pydantic
from codemeticulous.cli import load_and_create_model
from codemeticulous.convert import STANDARDS

def check_for_operational_url(url: str, timeout_val = 10) -> bool:
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
            return True  # URL is operational
        else:
            return False  # URL is NOT operational
    
    except requests.RequestException as e:
        return False  # URL is not operational

def load_codemeta_file(codemeta_file):
    try:
        with open(codemeta_file, "r") as file:
            return json.load(file)
    except:
        print(f'Codemeta file could not load: {codemeta_file}')
        sys.exit(1) 

def run_codemeticulous_validation(codemeta_file):
    """
    Validates the Codemeta JSON file using `codemeticulous` directly in Python.
    """

    codemeta_json = load_codemeta_file(codemeta_file)

    # see if codemeta is valid
    try:
        model = STANDARDS['codemeta']["model"]  # Get Pydantic model for codemeta V3
        model(**codemeta_json)
        print(f"{codemeta_file} is a valid codemeta file.")

        return codemeta_json

    # if invalid print validation errors and break
    except pydantic.v1.error_wrappers.ValidationError as e:
        print(f"{codemeta_file} is not a valid codemeta file. {e}")
        sys.exit(1)

def validate_and_log_urls(extracted_values,eval_method,log):

    result = False

    for key, value in extracted_values.items():
        
        for url in value:
            res = check_for_operational_url(url)

            if res == True:
                result = True
                print(f"{eval_method} logs: {url} in codemeta property '{key}' {log}")

    return result

def validate_and_log_version(extracted_values,eval_method,log):

    result = False

    for key, value in extracted_values.items():

        parts = value.split('.')  # Split the version string

        # Check if version is in the format X.Y.Z where X, Y, and Z are integers (semanatic versioning)
        is_valid = len(parts) == 3 and all(part.isdigit() for part in parts)

        if is_valid:
            print(f"{eval_method} logs: {value} in codemeta property '{key}' {log}")
            result = True

    return result


