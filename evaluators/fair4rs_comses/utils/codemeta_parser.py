from typing import Dict, Any, List

def get_persistent_identifier_urls(metadata: Dict[str, Any]) -> List[str]:
    """
    Recursively searches for persistent identifier (DOI) URLs in a nested dictionary.

    :param metadata: Dictionary containing metadata (can include nested dictionaries/lists).
    :return: List of DOI URLs found in the metadata.
    """
    doi_urls = []

    def search_dict(data: Any):
        """Recursive helper function to traverse nested dictionaries and lists."""
        if isinstance(data, dict):
            for value in data.values():
                search_dict(value)  # Recursively check values
        elif isinstance(data, list):
            for item in data:
                search_dict(item)  # Recursively check list elements
        elif isinstance(data, str) and data.startswith("https://doi.org"):
            doi_urls.append(data)  # Store valid DOI URL

    search_dict(metadata)  # Start the recursive search
    return doi_urls



