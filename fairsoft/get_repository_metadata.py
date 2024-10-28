import os
import requests
from gql import gql, Client
import urllib.parse as urlparse
from gql.transport.requests import RequestsHTTPTransport # also need to install requests_toolbelt
from dotenv import load_dotenv

def get_github_repo_and_owner(url):

    # get path from url
    path = urlparse.urlparse(url).path
    # split the path into head (owner) and tail (repo)
    owner_name, repo_name = os.path.split(path)
    # remove leading slash from owner
    owner_name = owner_name.lstrip("/")

    return repo_name, owner_name

def get_access_token():

    # load variables from .env file
    load_dotenv()

    # retrieve client id and client secret
    access_token = os.getenv('ACCESS_TOKEN')

    return access_token

def query_repository_object(token, owner, repo, commit_limit=100):
    """
    
    Adaptation of queryRepositoryObject function from https://github.com/inab/github-metadata-api/blob/main/src/metadataExtractor/helpers/metadata.js

    """

    # define transport to communicate with the GitHub GraphQL API
    transport = RequestsHTTPTransport(
        url="https://api.github.com/graphql",
        headers={"Authorization": f"Bearer {token}"}
    )

    # create GraphQL client using the transport
    client = Client(transport=transport, fetch_schema_from_transport=True)
    
    # define query
    query = gql("""
        query ($owner: String!, $repo: String!, $commitLimit: Int!) {    
            repository(owner: $owner, name: $repo) {
                description
                descriptionHTML
                homepageUrl
                isDisabled
                isEmpty
                isFork
                isInOrganization
                isLocked
                isMirror
                isPrivate
                isTemplate
                latestRelease {
                    name
                    tagName
                }
                licenseInfo {
                    id
                    name
                    spdxId
                    url
                }
                name
                mirrorUrl
                packages(first: $commitLimit) {
                    nodes {
                        id
                        name
                        packageType
                        version(version: "") {
                            version
                            summary
                        }
                    }
                }
                releases(last: $commitLimit) {
                    nodes {
                        id
                        tagName
                        name
                        url
                    }
                }
                url
                defaultBranchRef {
                    target {
                        ... on Commit {
                            history(first: $commitLimit) {
                                edges {
                                    node {
                                        author {
                                            name
                                            email
                                            user {
                                                login
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
                repositoryTopics(first: $commitLimit) {
                    nodes {
                        url
                        topic {
                            id
                            name
                        }
                    }
                }
            }
        }
    """)

    # execute query with the provided variables
    variables = {
        "owner": owner,
        "repo": repo,
        "commitLimit": commit_limit
    }

    ghObject = client.execute(query, variable_values=variables)["repository"]

    return ghObject


def build_license(githubObject):
    """
    
    Adaptation of buildLicense function from https://github.com/inab/github-metadata-api/blob/main/src/metadataExtractor/helpers/metadata.js

    """

    if githubObject["licenseInfo"]:

        licenses = [
            {
            'name': githubObject["licenseInfo"]["name"],
            'url': githubObject["licenseInfo"]["url"]
        }
        ]

    else:
        licenses = []

    return licenses

def remove_null(array):
    """
    
    Adaptation of removeNull function from https://github.com/inab/github-metadata-api/blob/main/src/metadataExtractor/helpers/metadata.js

    """

    array_filtered = [val for val in array if val is not None]

    return array_filtered

def build_topics(githubObject):
    """
    
    Adaptation of buildTopics function from https://github.com/inab/github-metadata-api/blob/main/src/metadataExtractor/helpers/metadata.js

    """

    topics = []

    if len(githubObject["repositoryTopics"]["nodes"]) > 0:
        # iterate over each node in the list
        for node in githubObject["repositoryTopics"]["nodes"]:
            # create dictionary for each topic
            item = {
                "uri": node["url"],
                "term": node["topic"]["name"],
                "vocabulary": ""
            }
            # append to the topics list
            topics.append(item)

    return topics

def build_authors(githubObject):
    """
    
    Adaptation of buildAuthors function from https://github.com/inab/github-metadata-api/blob/main/src/metadataExtractor/helpers/metadata.js

    """

    authors = []

    # extract contributors the commit history
    contributors = [
        edge["node"]["author"]
        for edge in githubObject["defaultBranchRef"]["target"]["history"]["edges"]
    ]

    # generate an author dictionary for each contributor
    for contributor in contributors:
        author = {
            "name": contributor["name"],
            "type": "person",  # GitHub contributor type is always 'person'
            "email": contributor["email"],  # Use an empty string if no email is provided
            "maintainer": False
        }

        # avoid duplicates based on email
        if not any(existing_author["email"] == author["email"] for existing_author in authors):
            authors.append(author)

    return authors

def prepare_lists_ids(metadata):
    """
    
    Adaptation of function from https://github.com/inab/github-metadata-api/blob/main/src/metadataExtractor/helpers/metadata.js

    """

    fields = [
        'edam_topics', 'edam_operations', 'documentation', 'description', 'webpage', 
        'license', 'src', 'links', 'topics', 'operations', 'input', 'output', 
        'repository', 'dependencies', 'os', 'authors', 'publication'
    ]
    
    for field in fields:
        # check if field is present in metadata and is a list
        if field in metadata and isinstance(metadata[field], list):
            # transform each item in list to a dictionary with 'term' and 'id'
            metadata[field] = [{"term": item, "id": idx} for idx, item in enumerate(metadata[field])]

    return metadata

def github_metadata(ghObject):
    """
    
    Adaptation of githubMetadata function from https://github.com/inab/github-metadata-api/blob/main/src/metadataExtractor/helpers/metadata.js

    """

    # observatory metadata schema
    metadata = {
        'name': ghObject["name"],
        'label': [
            ghObject["name"]
        ],
        'description': remove_null([ 
            ghObject["description"] 
        ]),
        'links': remove_null([
            ghObject["mirrorUrl"] 
        ]),
        'webpage': remove_null([
            ghObject["homepageUrl"]
        ]),
        'isDisabled': ghObject["isDisabled"],
        'isEmpty': ghObject["isEmpty"],
        'isLocked': ghObject["isLocked"],
        'isPrivate': ghObject["isPrivate"],
        'isTemplate': ghObject["isTemplate"],
        'license': build_license(ghObject),
        'repository': remove_null([ 
            ghObject["url"]
        ]),
        
        'topics': build_topics(ghObject),
        'operations': [],
        'authors': build_authors(ghObject),
        'bioschemas': False,
        'contribPolicy': [],
        'dependencies': [],
        'documentation': [],
        'download': [], #// This could be package or come from repository contents
        'edam_operations': [],
        'edam_topics': [],
        'https': True,
        'input': [],
        'inst_instr': False,
        'operational': False,
        'os': [],
        'output': [],
        'publication': [],
        'semantics': {
            'inputs': [],
            'outputs': [],
            'topics': [],
            'operations': [],
        },
        'source': ['github'],
        'src': [],
        'ssl': True,
        'tags': [],
        'test': [],
        'type': "",   
    }

    return metadata

def main(github_url):

    # get github access token
    token = get_access_token()

    # extract owner and repo name from github url
    repo,owner = get_github_repo_and_owner(github_url)

    # make query through github graphql api
    github_object = query_repository_object(token, owner, repo)

    # get github metadata and transform to observatory metadata schema
    metadata = github_metadata(github_object)

    # add terms to dictionary
    metadata = prepare_lists_ids(metadata)

    return metadata

    

