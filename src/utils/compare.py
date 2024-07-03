import requests
from packaging.version import parse
import re

#example repositories 
# repo_name ='ICHydro/topmodel'
# repo_name ='NOAA-OWP/topmodel'

#TODO make class structure for the functions - this is currently in draft state
#TODO add doc strings to the functions
#TODO complete the functions based on scorecard principles 


def get_repo_info(repo_name, section='readme'):
    """
    Description: Get the repository information from the github api based on the section that is passed in the function

    params:
    repo_name(str): the repository name that is being searched for. Note - this is not the url . Format : owner/repo_name
    section(str): the section of the repository that is being searched for. The options are 'readme','releases','contents'

    returns:
    data(str): the data that is returned from the github api based on the section that is passed in the function - either json or text string 

    """
    if section == 'readme':
    #get the repository information

        url = f"https://api.github.com/repos/{repo_name}/readme"
        headers = {"Accept": "application/vnd.github.v3.raw"}
        response = requests.get(url, headers=headers)

        #response 
        data= response.text

    if section == 'releases':

        url = f"https://api.github.com/repos/{repo_name}/releases"

        response = requests.get(url)
        data = response.json()

    if section == 'contents':
        url = f"https://api.github.com/repos/{repo_name}/contents"
        response = requests.get(url)
        data = response.json()

    return data

def f1_unique_identifier(data):
    """
    Description:
    Principle F1: (meta)data are assigned a globally unique identifier - software uses identifier either(Digital Object Identifier)DOI or (SofWare Heritage persistent Identifier) SWHID via archiving software tools ( Zenodo, Software Heritage, Figshare) or domain specific repositories that specialize in FAIR open source model repositories 

    params:
    data(str): the data from the repository readme file - this is the data that is returned from the get_repo_info function. section 'readme'

    returns:
    len_found(int): the number of search words that are found in the data
    len_search_words(int): the number of search words that are listed in the search_words list
    
    """
    #check if the repository has a unique identifier based on the search words listed below.
    search_words =['unique identifier','DOI','zenodo','badge']
    found =[]
    for word in search_words:
        if word in data:
            found.append(word)

    len_found = len(found)
    len_search_words = len(search_words)
    
    return len_found, len_search_words

#TODO fill in function f1_1 - currently is in draft state (empty)
def f1_1_components_unique_identifier(data, code_source_path):

    """
    Description:    
    Principle F1.1. Components of the software representing levels of granularity are assigned distinct identifiers.

    This specific function checks if different classes or function names are unique 

    """

def f1_2_versions_unique_identifier(data):
    """
    Description:
    F1.2. Different versions of the software are assigned distinct identifiers.

    params:
    data(json): the data from the repository readme file - this is the data that is returned from the get_repo_info function by passing in the 'releases' section

    returns:
    len_formatted_versions(int): the number of formatted via semantic versioning that are found in the data
    len_found(int): the number of versions that are found in the data
    len_duplicates(int): the number of duplicates that are found in the data
    """

    found =[]
    not_format_versions=[]
    formatted_versions =[]
    duplicates =[]
    for release in data:
        found.append(release['tag_name'])

    #check for semantic versioning
    for version in found:
        # Remove leading 'v' if present
        version = version.lstrip('v')
    
        # matching semantic versioning
        pattern = r'^(\d+)\.(\d+)\.(\d+)$'
        if re.match(pattern, version):
            formatted_versions.append(version)
        else:
            not_format_versions.append(version)

        if len(found) != len(set(found)):
            duplicates.append(version)

    len_formatted_versions = len(formatted_versions)
    len_found = len(found)
    len_duplicates = len(duplicates)

    return len_formatted_versions, len_found, len_duplicates
    
def f_2_plus_readme_contents(data):
    """
    Description
    F2+. README file is includes descriptive documentation
    software includes a  README file [markdown, plain text].  The file includes the following sections :[Description, Install, Documentation Link, How to Contribute [if applicable], License, Usage example]

    params:
    data(str): the data from the repository readme file - this is the data that is returned from the get_repo_info function by passing in the 'readme' section

    returns:
    len_found_readme(int): the number of search words that are found in the readme
    len_search_words_readme(int): the number of search words that are listed in the search_words list
    """
    #search the contents of the readme file
    search_words =['Description','Install','How to Contribute','License','Documentation']

    found = []
    for word in search_words:
        if word in data:
            found.append(word)

    len_found_readme = len(found)
    len_search_words_readme = len(search_words)


    return len_found_readme, len_search_words_readme ,found

