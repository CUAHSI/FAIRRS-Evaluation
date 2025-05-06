#!/usr/bin/env python3

"""
This utility converts CSDMS metadata to CodeMeta format.
"""

import re
import json
import logging
from glob import glob
from pathlib import Path
from datetime import date
from typing import Union, List, Optional


import typer
from pydantic.v1 import HttpUrl
from pydantic2_schemaorg.Person import Person
from pydantic2_schemaorg.DataFeed import DataFeed
from pydantic2_schemaorg.Organization import Organization
from pydantic2_schemaorg.CreativeWork import CreativeWork
from pydantic2_schemaorg.Review import Review
from codemeticulous.codemeta.models import CodeMetaV3, VersionedLanguage


app = typer.Typer()


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


def build_codemeta(json_file: Path) -> CodeMetaV3:
    """
    Reads a CSDMS metadata file in JSON format and converts it to CodeMeta format.

    Arguments:
        json_file (Path): Path to the CSDMS metadata JSON file.

    Returns:
        str: CodeMeta formatted string.
    """

    with open(json_file, "r", encoding="utf-8") as f:
        dat = json.loads(f.read())

    properties = squash_mediawiki_vars(dat)

    ##################
    # ENCODE AUTHORS #
    ##################

    # Lots of handling is needed to account for one or more authors.

    # get the total number of authors by their email addresses
    total_people = len(
        as_list(properties.get("Email_address", []))
        + as_list(properties.get("Additional_email_address", []))
    )
    #    if "Additional_email_address" in properties:
    #        total_people += len(as_list(properties["Additional_email_address"]))

    # collect first names, last names, and emails
    first_names = as_list(properties.get("First_name", [])) + as_list(
        properties.get("Additional_first_name", [])
    )
    first_names = grow_list(first_names, total_people)
    # if "Additional_first_name" in properties:
    #    first_names += as_list(properties["Additional_first_name"])

    last_names = as_list(properties.get("Last_name", [])) + as_list(
        properties.get("Additional_last_name", [])
    )
    last_names = grow_list(last_names, total_people)
    # if "Additional_last_name" in properties:
    #    last_names += as_list(properties["Additional_last_name"])

    emails = as_list(properties.get("Email_address", [])) + as_list(
        properties.get("Additional_email_address", [])
    )
    emails = grow_list(emails, total_people)
    #    if "Additional_email_address" in properties:
    #        emails += as_list(properties["Additional_email_address"])

    # If the length of any of these fields is 1, it will
    # be applied to all additional_fields collect addresses.
    cities = as_list(properties.get("City", [])) + as_list(
        properties.get("Additional_city", [])
    )
    cities = grow_list(cities, total_people)
    #    if "Additional_city" in properties:
    #        additional_cities = as_list(properties["Additional_city"])
    #        if len(additional_cities) < (total_people - 1):
    #            additional_cities *= total_people - 1
    #        cities += additional_cities

    # collect countries
    countries = as_list(properties.get("Country", [])) + as_list(
        properties.get("Additional_country", [])
    )
    countries = grow_list(countries, total_people)
    # if "Additional_country" in properties:
    #     additional_countries = as_list(properties["Additional_country"])
    #     if len(additional_countries) < (total_people - 1):
    #         additional_countries *= total_people - 1
    #     countries += additional_countries

    # collect institutes
    institutes = as_list(properties.get("Institute", [])) + as_list(
        properties.get("Additional_institute", [])
    )
    institutes = grow_list(institutes, total_people)
    # if "Additional_institute" in properties:
    #     additional_institutes = as_list(properties["Additional_institute"])
    #     if len(additional_institutes) < (total_people - 1):
    #         additional_institutes *= total_people - 1
    #     institutes += additional_institutes

    # build list of authors
    authors = []
    for i in range(0, total_people):
        # import pdb
        #
        # pdb.set_trace()
        author = Person(
            givenName=first_names[i],
            familyName=last_names[i],
            email=emails[i],
            affiliation=Organization(
                address=f"{cities[i]}, {countries[i]}", name=institutes[i]
            ),
        )
        authors.append(author)

    ########################
    # ENCODE CORE ELEMENTS #
    ########################
    date_created = properties.get("Start_year_development", None)
    if date_created:
        date_created = date(int(date_created), 1, 1)

    # Keywords combine: ModelDomain, Modelautophrases, and Model_keywords
    keywords = (
        as_list(properties.get("ModelDomain", []))
        + as_list(properties.get("Modelautophrases", []))
        + as_list(properties.get("Model_keywords", []))
    )
    if len(keywords) == 0:
        keywords = None

    web_address = properties.get("Source_web_address", None)

    # downloadUrl and codeRepository
    downloadUrl = None
    codeRepository = None
    source_web_address = properties.get("Source_web_address", None)
    #    import pdb
    #
    #    pdb.set_trace()
    if source_web_address:
        # source address may contain muiltiple lines
        source_web_address = source_web_address.split("\n")

        # items may contain multiple web addresses
        if len(source_web_address) > 1:
            downloadUrl = []
            codeRepository = []
            for web_address in source_web_address:
                downloadUrl.append(
                    HttpUrl(scheme=web_address.split(":")[0], url=web_address)
                )

                codeRepository.append(
                    HttpUrl(scheme=web_address.split(":")[0], url=web_address)
                )
            # this is necessary because currently code-meta only supports a single code repository.
            # However, the CSDMS metadata may contain multiple code repositories.
            codeRepository = codeRepository[0]
        else:
            downloadUrl = HttpUrl(
                scheme=properties["Source_web_address"].split(":")[0],
                url=properties["Source_web_address"],
            )
            codeRepository = HttpUrl(
                scheme=properties["Source_web_address"].split(":")[0],
                url=properties["Source_web_address"],
            )

    plang = as_list(properties.get("Programming_language", [])) + as_list(
        properties.get("Programming_language_other", [])
    )
    programmingLanguage = [VersionedLanguage(name=lang) for lang in plang]

    #    if "Program_language_other" in properties:
    #        plang += as_list(properties["Program_language_other"])

    # applicationCategory
    applicationCategory = properties.get("Model_type", None)

    # memory Requirements
    memoryRequirements = properties.get("Memory_requirements", None)
    if memoryRequirements is not None:
        memoryRequirements = memoryRequirements.replace("-", "").strip()
    if not memoryRequirements:
        memoryRequirements = None

    dateModified = None
    if "End_year_model_development" in properties:
        dateModified = date(properties["End_year_model_development"], 1, 1)

    supported_platforms = as_list(properties.get("Supported_platforms", [])) + as_list(
        properties.get("Supported_platforms_other", [])
    )
    operatingSystem = [platform for platform in supported_platforms]

    model_name = dat["subject"][0:-7]
    record_url = f"https://csdms.colorado.edu/wiki/Model:{model_name}"
    url = HttpUrl(scheme=record_url.split(":")[0], url=record_url)

    # license
    # TODO: The way we extract license needs to be improved.
    license_value = properties.get("Program_license_type", None)
    if license_value is not None:
        if license_value.startswith("https:") or license_value.startswith("http:"):
            license = HttpUrl(scheme=license_value.split(":")[0], url=license_value)
        else:
            license = CreativeWork(name=properties["Program_license_type"])

    # identifier
    doi_identifier = properties.get("DOI_model", None)

    # softwareVersion 
    # modify to retrieve DOI_assigned_to_version instead of version property from CSDMS
    software_version = properties.get("DOI_assigned_to_version", None)

    # softwareHelp
    # modified to encode buildInstructions codemeta term instead of softwareHelp
    buildInstructions = None
    manual_available_string = properties.get("DOI_assigned_to_version", "No")
    helpAvailable = False if manual_available_string == "No" else True
    if helpAvailable:
        model_manual = properties.get("Model_manual", None)
        if model_manual is not None:
            manual_url = f"https://csdms.colorado.edu/csdms_wiki/images/{':'.join(model_manual.split(':')[1:])}"

            buildInstructions = CreativeWork(
                name="Software Manual",
                url=HttpUrl(scheme="https", url=manual_url.replace(" ", "_")),
            )

    # supportingData
    # using test data because this is a URL that's provided. Calibration data is a narrative.
    supportingData = None
    testData = properties.get("Model_test_data", None)
    if testData:
        testData = as_list(testData)
        supportingData = []
        for datafile in testData:
            test_data_url = f"https://csdms.colorado.edu/csdms_wiki/images/{':'.join(datafile.split(':')[1:])}"
            supportingData.append(
                DataFeed(name="Test Data", url=test_data_url.replace(" ", "_"))
            )

    # review
    # check if the model has been code reviewed or not 
    # link to JOSS publication does not appear to be available for all models
    # note this is not in Irene's crosswalk at the moment
    review = None
    codeReviewed = properties.get("CodeReviewed")
    if codeReviewed == "0": # model has been reviewed and accepted in JOSS (value is "1" if not reviewed)
        review = Review(reviewBody="Reviewed and accepted by the Journal of Open Source Software (JOSS).")

    # relatedLink
    # extracting this from Model forum field for now
    relatedLink = None
    related_link_value = properties.get("Model_forum", None)
    if related_link_value:
        related_link_url = extract_url(related_link_value)
        if related_link_url:
            relatedLink = HttpUrl(scheme="https", url=related_link_url)


    ###################
    # ENCODE CODEMETA #
    ###################

    # developmentStatus ### NOTE THIS IS DIFFERENT THAN IRENE'S MAPPING ###
    developmentStatus = properties.get("DevelopmentCode", None)

    #    import pdb
    #
    #    pdb.set_trace()

    ##########################
    # CREATE CODEMETA OBJECT #
    ##########################
    meta = CodeMetaV3(
        name=dat["subject"][0:-7],
        dateCreated=date_created,
        author=authors,
        description=properties["Extended_model_description"],
        keywords=keywords,
        codeRepository=codeRepository,
        programmingLanguage=programmingLanguage,
        applicationCategory=applicationCategory,
        memoryRequirements=memoryRequirements,
        dateModified=dateModified,
        operatingSystem=operatingSystem,
        url=url,
        developmentStatus=developmentStatus,
        downloadUrl=downloadUrl,
        identifier=doi_identifier,
        software_version=software_version,
        supportingData=supportingData,
        review = review,
        relatedLink = relatedLink
    )
    # There appears to be an issue with the validate_creative_work function that
    # I think is related to the "each_item=True" option. To overcome this, we'll
    # add some fields after our class is instantiated to skip validation.
    meta.license = license
    meta.buildInstructions = buildInstructions

    return meta


def squash_mediawiki_vars(mediawiki_json: dict) -> dict:
    """
    Squashes the mediawiki variables in the JSON string to something more
    useable by the encoding function.

    Arguments:
        mediawiki_json_str (str): JSON string containing mediawiki variables.

    Returns:
        dict: Dictionary with the mediawiki variables squashed.
    """

    properties = {}
    for prop in mediawiki_json["data"]:
        items = [p["item"].strip() for p in prop["dataitem"]]
        if len(items) == 1:
            items = items[0]
        properties[prop["property"]] = items

    return properties


def as_list(obj: Union[str, List[str]]) -> List[str]:
    """
    Utility function to convert a string or list of strings to a list of strings.

    Arguments:
        str | List[str]: String or list of strings to convert.
    Returns:
        List[str]: List of strings.
    """

    if isinstance(obj, list):
        return obj
    return [obj]


def grow_list(
    original_list: list[str] | list[str | None], new_size: int
) -> list[str | None]:
    """
    Resizes a list to a new size by duplicating the last element

    Arguments:
        original_list (List[str]): Original list to resize.
        new_size (int): New size of the list.
    Returns:
        List[str]: Resized list.
    """

    if new_size <= len(original_list):
        return [item for item in original_list]

    resized_list = list(original_list)
    last_element = resized_list[-1] if resized_list else None

    while len(resized_list) < new_size:
        resized_list.append(last_element)

    return resized_list

def extract_url(property_value: str) -> Optional[str]:
    """
    Utility function to retrieve URLs from property containing free text.
    """

    # pattern to find URLs starting with https://
    pattern = r'https://\S+'

    match = re.search(pattern,property_value)

    if match:
        url = match.group()
    else:
        url = None

    return url






if __name__ == "__main__":
    app()
