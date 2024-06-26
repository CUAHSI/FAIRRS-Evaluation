import requests


# repo_name ='ICHydro/topmodel'

# repo_name ='NOAA-OWP/topmodel'

#TODO make class structure for the functions - this is currently in draft state

#get github repository information 
def get_repo_info(repo_name):
    #get the repository information

    url = f"https://api.github.com/repos/{repo_name}/readme"
    headers = {"Accept": "application/vnd.github.v3.raw"}
    response = requests.get(url, headers=headers)

    #response 
    data= response.text

    return data

def search_contents_readme(data):
    #search the contents of the readme file
    search_words =['Description','Install','How to Contribute','License','Documentation']

    found = []
    for word in search_words:
        if word in data:
            found.append(word)
    print("the following sections were found in the readme file: ",found)
    return len(found), len(search_words)

