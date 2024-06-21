import requests


#get github repository information 
def get_repo_info(repo_name):
    url = 'https://api.github.com/repos/' + repo_name
    response = requests.get(url)
    return response.json()