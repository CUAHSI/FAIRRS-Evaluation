import re
import os
import sys
import json
import requests
from typing import Dict, Any, List
from pathlib import Path
from urllib.parse import urlparse
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
    
def get_urls_by_name(codemeta_property_val, target_name) -> list:
    """

    """
    return [
        entry["url"]
        for entry in codemeta_property_val
        if entry.get("name") == target_name and "url" in entry
    ]

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

def validate_and_log_urls(extracted_values,msg,log=None):

    if log is None:
        log = []

    result = False

    for key, value in extracted_values.items():
        
        for url in value:
            res = check_for_operational_url(url)

            if res == True:
                result = True
                log.append(f"{url} in codemeta property '{key}' is {msg}")
                # print(f"{eval_method} logs: {url} in codemeta property '{key}' {log}")
            else:
                log.append(f"{url} in codemeta property '{key}' is NOT {msg}")

    return result, log

def validate_and_log_version(extracted_values,msg,log=None):

    if log is None:
        log = []

    result = False

    if not extracted_values:

        log.append('No version provided.')

        return result, log

    for key, value in extracted_values.items():

        # parts = value.split('.')  # Split the version string

        # Check if version is in the format X.Y.Z where X, Y, and Z are integers (semanatic versioning)
        pattern = r'\b(\d)\.(\d)\.(\d)\b'
        is_valid = re.search(pattern, value)
        # is_valid = (
        #     len(parts) == 3 and
        #     all(part.isdigit() and len(part) == 1 for part in parts)
        # )

        if is_valid:
            log.append(f"{value} in codemeta property '{key}' {msg}")
            # print(f"{eval_method} logs: {value} in codemeta property '{key}' does NOT {log}")
            result = True
        else:
            log.append(f"{value} in codemeta property '{key}' does NOT {msg}")

    return result, log

def validate_presence_of_fields(fields, log=None):
    """
    Validates that required fields are present and not None or empty.
    """

    if log is None:
        log = []

    result = True

    for key, value in fields.items():
        if value is None or (isinstance(value, str) and value.strip() == ''):
            log.append(f"Field '{key}' is missing or empty.")
            # print(f"{eval_method} logs: Field '{key}' is missing or empty.")
            result = False
        else:
            log.append(f"Field '{key}' is present.")
            # print(f"{eval_method} logs: Field '{key}' is present.")
    
    return result, log

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

def check_substring_regex(full_string, substring, msg, log=None):
    """
    """

    if log is None:
        log = []

    if isinstance(substring,str):
        substring = [substring]

    pattern = re.compile('|'.join(re.escape(base) for base in substring), re.IGNORECASE)

    if pattern:
        result = True
        log.append(f"{full_string} does {msg}.")
    else:
        result = False
        log.append(f"{full_string} does NOT {msg}.")

    return result, log


def validate_data_interoperability(supporting_data, accepted_data_formats, target_name, log=None):
    """
    Validates that the software interoperates using community-accepted standards for data exchange/
    """

    if log is None:
        log = []

    result = False

    if not supporting_data:
        log.append('No supportingData field provided.')
        result = False

        return result, log

    urls = get_urls_by_name(supporting_data, target_name) 

    for url in urls:
        ext = Path(urlparse(url).path).suffix.lstrip('.').lower()
        if ext in accepted_data_formats:
            log.append(f"{url} links test data in an accepted file format.")
            result = True
        else:
            log.append(f"{url} links test data in an UNACCEPTED file format.")
            if result:
                pass
            else:
                result = False

    # all_formats = extract_extensions_from_supporting_data(supporting_data)
    # print(all_formats)
    # recognized_formats = [fmt for fmt in all_formats if fmt.lower() in accepted_data_formats]

    # if recognized_formats:
    #     log.append(f"Recognized data format used: {recognized_formats}")
    #     # print(f"{eval_method} logs: Recognized formats used: {recognized_formats}")
    # else:
    #     log.append(f"No recognized data formats used.")
    #     # print(f"{eval_method} logs: No recognized formats found in input, output, or supportingData.")
    #     result = False

    return result, log

def check_for_api_documentation(build_instructions, api_keywords, log=None):
    """
    Checks if the buildInstructions field points to API-related documentation based on keywords.

    """
    if log is None:
        log = []

    result = False

    if not build_instructions:
        log.append('No buildInstructions field provided.')
        # print(f"{eval_method} logs: No buildInstructions field provided.")
        return result

    # Make sure api_documentation is iterable
    if isinstance(build_instructions, str):
        build_instructions = [build_instructions]

    for entry in build_instructions:
        if not isinstance(entry, str):
            continue
        lowered_entry = entry.lower()
        if any(keyword in lowered_entry for keyword in api_keywords):
            log.append(f"Found API documentation link in buildInstructions: {entry}.")
            # print(f"{eval_method} logs: found API documentation link in buildInstructions: {entry}.")
            result = True
        else:
            log.append(f"buildInstructions link '{entry}' does not appear to be API documentation.")
            # print(f"{eval_method} logs: buildInstructions link'{entry}' does not appear to be API documentation.")

    return result, log

def check_if_field_in_keywords(field, kw_list, msg, log=None):
    """
    Checks if any permissive license keywords appear in the input string using case-insensitive regex.

    Args:
        text (str): The input string to check.
        license_list (List[str]): List of license strings to search for (default = PERMISSIVE_LICENSES)

    Returns:
        bool: True if any license is found, False otherwise.
        
    """

    if log is None:
        log = []

    result = any(re.search(rf'\b{re.escape(kw)}\b', field, re.IGNORECASE) for kw in kw_list)

    if result:
        log.append(f"{field} is {msg}")

    else:
        log.append(f"{field} is NOT {msg}")

    return result,log
