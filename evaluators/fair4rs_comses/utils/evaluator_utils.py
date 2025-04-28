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

def validate_presence_of_fields(fields, eval_method):
    """
    Validates that required fields are present and not None or empty.
    """

    result = True

    for key, value in fields.items():
        if value is None or (isinstance(value, str) and value.strip() == ''):
            print(f"{eval_method} logs: Field '{key}' is missing or empty.")
            result = False
        else:
            print(f"{eval_method} logs: Field '{key}' is present.")
    
    return result

def extract_extensions_from_supporting_data(supporting_data_list):
    """
    Extracts file extensions from supportingData entries (URLs or paths).
    """
    extensions = []
    if supporting_data_list:
        for entry in supporting_data_list:
            if isinstance(entry, str):
                ext = os.path.splitext(entry)[-1].lower().strip(".")
                if ext:  # skip empty extensions
                    extensions.append(ext)
    return extensions


def validate_data_interoperability(supporting_data, accepted_data_formats, eval_method):
    """
    Validates that the software interoperates using community-accepted standards for data exchange or API documentation.
    """

    result = True
    all_formats = extract_extensions_from_supporting_data(supporting_data)

    recognized_formats = [fmt for fmt in all_formats if fmt.lower() in accepted_data_formats]

    if recognized_formats:
        print(f"{eval_method} logs: Recognized formats used: {recognized_formats}")
    else:
        print(f"{eval_method} logs: No recognized formats found in input, output, or supportingData.")
        result = False

    return result

def check_for_api_documentation(build_instructions, api_keywords, eval_method):
    """
    Checks if the buildInstructions field points to API-related documentation based on keywords.

    """

    result = False

    if not build_instructions:
        print(f"{eval_method} logs: No buildInstructions field provided.")
        return result

    # Make sure api_documentation is iterable
    if isinstance(build_instructions, str):
        build_instructions = [build_instructions]

    for entry in build_instructions:
        if not isinstance(entry, str):
            continue
        lowered_entry = entry.lower()
        if any(keyword in lowered_entry for keyword in api_keywords):
            print(f"{eval_method} logs: found API documentation link in buildInstructions: {entry}.")
            result = True
        else:
            print(f"{eval_method} logs: buildInstructions link'{entry}' does not appear to be API documentation.")

    return result
