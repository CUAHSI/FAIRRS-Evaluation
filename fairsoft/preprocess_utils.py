import os
import urllib.parse as urlparse


def get_github_repo_and_owner(url):

    # get path from url
    path = urlparse.urlparse(url).path
    # split the path into head (owner) and tail (repo)
    owner, repo = os.path.split(path)
    # remove leading slash from owner
    owner = owner.lstrip("/")

    return repo,owner


