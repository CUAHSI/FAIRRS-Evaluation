import re
from typing import Dict, List, Union, Optional
from pydantic import AnyUrl


def extract_urls_from_field(value, regex_filter: Optional[Union[str, List[str]]] = None) -> List[str]:
    """
    Extracts URLs from a given CodeMetaV3 field with optional regex filtering.

    Parameters:
    - value: The field value (can be a single URL, list of URLs, or nested object).
    - regex_filter: (Optional) A string or list of regex patterns to filter URLs.

    Returns:
    - A list of extracted URLs (filtered if regex is provided).
    """
    urls = []

    if not value:
        return urls  # Return empty list if value is None or empty

    if isinstance(value, list):  # Handle lists of URLs or objects
        for item in value:
            urls.extend(extract_urls_from_field(item, regex_filter))  # Recursively extract URLs

    elif isinstance(value, dict):  # Handle nested dictionaries (CreativeWork, PropertyValue, etc.)
        if "@id" in value:  # Check if the object has an ID field that might be a URL
            urls.append(value["@id"])
        for key, val in value.items():  # Look for URL-like fields inside objects
            urls.extend(extract_urls_from_field(val, regex_filter))

    elif isinstance(value, AnyUrl) or (isinstance(value, str) and value.startswith("http")):
        urls.append(str(value))  # Convert AnyUrl to string and add to results

    # Apply regex filtering if a pattern is provided
    if regex_filter:
        if isinstance(regex_filter, str):  # If a single regex pattern is given
            urls = [url for url in urls if re.search(regex_filter, url)]
        elif isinstance(regex_filter, list):  # If multiple regex patterns are given
            urls = [url for url in urls if any(re.search(pattern, url) for pattern in regex_filter)]

    return urls