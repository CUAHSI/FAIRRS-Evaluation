#!/usr/bin/env python3

"""
This utility converts HydroShare model instance metadata to CodeMeta format.
"""

import json
import logging
from glob import glob
from pathlib import Path
from datetime import date, datetime
from typing import Union, List, Optional

import typer
from pydantic.v1 import HttpUrl, AnyUrl # Import AnyUrl to handle its serialization
from pydantic2_schemaorg.Person import Person
from pydantic2_schemaorg.Organization import Organization
from pydantic2_schemaorg.PropertyValue import PropertyValue
from pydantic2_schemaorg.Review import Review

# Assuming codemeticulous.codemeta.models is available and contains CodeMetaV3
# and VersionedLanguage as per your models.py file.
# If not, you'll need to adjust the import path or include the models directly.
try:
    from codemeticulous.codemeta.models import CodeMetaV3, VersionedLanguage
except ImportError:
    # Fallback for local testing if codemeticulous is not installed
    # This requires models.py to be in the same directory or accessible via PYTHONPATH
    import sys
    sys.path.append(str(Path(__file__).parent))
    from models import CodeMetaV3, VersionedLanguage


app = typer.Typer()

# Define the base URL for HydroShare resources
HYDROSHARE_BASE_URL = "https://www.hydroshare.org"

def as_list(obj: Union[str, List[str]]) -> List[str]:
    """
    Utility function to convert a string or list of strings to a list of strings.
    """
    if isinstance(obj, list):
        return obj
    if obj is None:
        return []
    return [obj]

@app.command()
def encode(
    file: Path | None = typer.Option(
        None,
        "--file",
        "-f",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        help="path to a single input file containing mediawiki variables in JSON format",
    ),
    directory: Path | None = typer.Option(
        None,
        "--directory",
        "-d",
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        help="path to a directory containing input files containing mediawiki variables in JSON format",
    ),
    output_directory: Path = typer.Option(
        None,
        "--output_directory",
        "-o",
        exists=True,
        file_okay=False,
        dir_okay=True,
        writable=True,
        help="path to a directory to write the output file(s)",
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="print verbose output"),
) -> None:

    # Check that exactly one of file or directory is provided
    if (file is None and directory is None) or (
        file is not None and directory is not None
    ):
        typer.echo(
            "Error: You must provide exactly one of --file or --directory.", err=True
        )
        raise typer.Exit(code=1)

    if verbose:
        logging.basicConfig(level=logging.INFO, format="%(message)s")
        logging.info("Verbose output enabled")
    else:
        logging.basicConfig(level=logging.ERROR, format="%(message)s")

    codemeta = {}
    if file:
        logging.info(f"Processing file: {file}")
        codemeta = build_codemeta(file)

        if output_directory:
            outfile = f"{output_directory}/{file.stem}.json"

            # this is a hack to pretty print the json since not
            # all pydantic options are implemetned in the codemeiculous
            json_data = json.loads(codemeta.json())

            with open(outfile, "w") as f:
                json.dump(json_data, f, indent=4)

        if verbose:
            logging.info(f"{json.dumps(json.loads(codemeta.json()) , indent=4)}")
    else:
        files = glob(f"{directory}/*.json")
        i = 1
        for f in files:
            logging.info(f"Processing file [{i} of {len(files)}]: {Path(f)}")

            codemeta = build_codemeta(Path(f))
            if output_directory:
                outfile = f"{output_directory}/{Path(f).stem}.json"

                # this is a hack to pretty print the json since not
                # all pydantic options are implemetned in the codemeiculous
                json_data = json.loads(codemeta.json())

                with open(outfile, "w") as f:
                    json.dump(json_data, f, indent=4)
            i += 1

def build_codemeta(json_file: Path) -> Optional[CodeMetaV3]:
    """
    Reads a HydroShare metadata file in JSON format and converts it to CodeMeta format.

    Arguments:
        json_file (Path): Path to the HydroShare metadata JSON file.

    Returns:
        Optional[CodeMetaV3]: CodeMetaV3 object or None if conversion fails.
    """
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            dat = json.loads(f.read())
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON from {json_file}: {e}")
        return None
    except FileNotFoundError:
        logging.error(f"File not found: {json_file}")
        return None

    # Mapping HydroShare fields to CodeMetaV3 properties based on the crosswalk
    # and the CodeMetaV3 class definition.

    # Basic fields
    name = dat.get("title")
    description = dat.get("abstract")
    keywords = as_list(dat.get("subject", [])) if dat.get("subject") else None
    if keywords == []: # Ensure empty list becomes None
        keywords = None

    # Dates - keep as datetime objects for now, json_serial will handle conversion to string
    date_created_str = dat.get("created")
    date_modified_str = dat.get("modified")
    date_created = None
    date_modified = None

    if date_created_str:
        try:
            # HydroShare dates are typically ISO format (e.g., "2018-07-11T15:42:26")
            # We will keep them as datetime objects here, and json_serial will convert them
            date_created = datetime.fromisoformat(date_created_str.replace('Z', '+00:00'))
        except ValueError:
            logging.warning(f"Could not parse dateCreated: {date_created_str}")
    if date_modified_str:
        try:
            date_modified = datetime.fromisoformat(date_modified_str.replace('Z', '+00:00'))
        except ValueError:
            logging.warning(f"Could not parse dateModified: {date_modified_str}")

    # Authors and Contributors
    authors = []
    # HydroShare's 'author' field is the primary author
    primary_author_name = dat.get("author")
    if primary_author_name:
        authors.append(Person(name=primary_author_name))

    # HydroShare's 'authors' field is a list of all contributing authors
    # Assuming 'authors' is a list of strings (names)
    contributing_authors = as_list(dat.get("authors", []))
    for auth_name in contributing_authors:
        if auth_name and auth_name != primary_author_name: # Avoid duplicating primary author if listed in 'authors'
            authors.append(Person(name=auth_name))

    # HydroShare's 'contributor' field for additional contributors
    additional_contributors = as_list(dat.get("contributor", []))
    contributors = []
    for contrib_name in additional_contributors:
        if contrib_name:
            contributors.append(Person(name=contrib_name))

    # Links and Identifiers
    # Construct the full URL for the 'link' field
    code_repository_relative_url = dat.get("link")
    code_repository_url = None
    if code_repository_relative_url:
        # Ensure it's not just an empty string after stripping
        full_url = f"{HYDROSHARE_BASE_URL}{code_repository_relative_url}".strip()
        if full_url: # Only assign if not empty
            code_repository_url = full_url

    identifier_short_id = dat.get("short_id")
    author_link = dat.get("author_link")
    availability_url = dat.get("availabilityurl")
    # license_status is typically a list, e.g., ["public"]
    hydroshare_availability = dat.get("availability")
    
    identifier = None 
    if hydroshare_availability == ["published"]:
        identifier = '10.4211/hs.' + identifier_short_id 

    # Type/Category
    application_category = as_list(dat.get("type", [])) if dat.get("type") else None
    if application_category == []:
        application_category = None

    # Maintainer (owner)
    maintainer_name = dat.get("owner")
    maintainer = Person(name=maintainer_name) if maintainer_name else None

    # review
    # check if the model has been code reviewed or not 
    review = None
    if hydroshare_availability == ["published"]:
        review = Review(reviewBody="Reviewed and accepted for publication in HydroShare.")

    # License
    license_obj = None
    # # for now just comment this out
    # # If HydroShare availability indicates "public", assume a common open license
    # if hydroshare_availability and "public" in [s.lower() for s in as_list(hydroshare_availability)]:
    #     # This is a common default for publicly available data/models that don't specify a license.
    #     # You might need to confirm the actual default license for HydroShare public resources.
    #     license_obj = "https://creativecommons.org/licenses/by/4.0/" # Creative Commons Attribution 4.0 International

    # Geo (geographic coverage) - CodeMetaV3 doesn't have a direct 'geo' property.
    # This information would typically be part of a CreativeWork that the software relates to,
    # or could be added as a custom PropertyValue if needed. For now, we'll skip direct mapping.
    # geo_coverage = dat.get("geo")

    try:
        codemeta_obj = CodeMetaV3(
            name=name,
            description=description,
            author=authors if authors else None,
            contributor=contributors if contributors else None,
            keywords=keywords,
            applicationCategory=application_category,
            # Pass the string directly for Pydantic to validate as HttpUrl
            codeRepository=HYDROSHARE_BASE_URL,
            identifier=identifier,
            dateCreated=date_created,
            dateModified=date_modified,
            license=license_obj, # Use the refined license_obj
            maintainer=maintainer,
            # Pass the string directly for Pydantic to validate as HttpUrl
            url=code_repository_url,
            review=review
            # Add other fields as needed based on the CodeMetaV3 model and HydroShare metadata
            # For example, if 'availabilityurl' is a status image, it might not directly map
            # to a CodeMeta property, or could be a relatedLink.
            # If 'availabilityurl' is a link to a status image, it doesn't directly fit CodeMetaV3.
            # You might consider adding it to 'relatedLink' if it's a general link.
            # relatedLink=as_list(availability_url) if availability_url else None,
        )
        return codemeta_obj
    except Exception as e:
        logging.error(f"Error creating CodeMetaV3 object for {json_file}: {e}")
        return None

if __name__ == "__main__":
    app()
