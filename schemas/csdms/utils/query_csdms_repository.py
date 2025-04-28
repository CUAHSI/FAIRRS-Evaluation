import os
import json
import requests
from urllib.parse import quote

def get_all_model_names():
    """
    Query all model page names from the CSDMS Semantic MediaWiki.
    """

    ask_query = "[[Category:Models]]|limit=5000"
    url = "https://csdms.colorado.edu/csdms_wiki/api.php"
    params = {
        "action": "ask",
        "query": ask_query,
        "format": "json"
    }

    print("Fetching model list...")
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise RuntimeError("Failed to get model list.")

    results = response.json()["query"]["results"]
    model_names = [key.split(":", 1)[1] for key in results if ":" in key]
    print(f"Found {len(model_names)} models.")
    return model_names

def fetch_model_properties(model_name):
    """
    Fetch all semantic properties for a given model from Special:Browse endpoint.
    """

    encoded_name = quote(model_name)
    url = f"https://csdms.colorado.edu/csdms_wiki/index.php?title=Special:Browse&offset=0&dir=out&article=Model%3A{encoded_name}&group=hide&format=json"

    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error fetching {model_name}: status code {response.status_code}")
        return None

    try:
        return response.json()
    except json.JSONDecodeError:
        print(f"JSON decoding error for {model_name}")
        return None

def save_model_json(model_name, model_data, output_dir="csdms_model_properties"):
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"{model_name.replace('/', '_')}.json")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(model_data, f, indent=2, ensure_ascii=False)
    print(f"Saved {model_name} to {filename}")

def main():
    """
    Main function to get all CSDMS models and then fetch/export all model properties.
    """
    model_names = get_all_model_names()
    for model in model_names:
        data = fetch_model_properties(model)
        if data:
            save_model_json(model, data)

if __name__ == "__main__":
    main()
