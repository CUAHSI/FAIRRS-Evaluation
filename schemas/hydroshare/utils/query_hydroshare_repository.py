import os
import re
import json
import requests
from typing import List, Dict

def get_model_instances() -> List[Dict]:
    """
    Queries HydroShare API for metadata from all model instance resources.
    """

    model_instances = []
    page_num = 1
    previous_resources = None

    while True:
        response = requests.get(
            'https://hydroshare.org/discoverapi/?filter={%22type%22:[%22Model%20Instance%22]}',
            params={'pnum': page_num}
        )
        json_response = response.json()
        resources = json.loads(json_response['resources'])

        if resources == previous_resources:
            break

        model_instances.extend(resources)
        previous_resources = resources
        page_num += 1

    return model_instances

def write_to_file(resources,output_folder):
    """
    Writes HydroShare resource metadata to file.
    """

    output_dir = os.path.abspath(os.path.join(os.getcwd(), "..", output_folder))
    os.makedirs(output_dir, exist_ok=True)

    for resource in resources:
        # use resource ID as file name
        filename = os.path.join(output_dir, f"{resource['short_id']}.json")
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(resource, f, indent=2, ensure_ascii=False)
        print(f"Saved to file: {filename}")

def main():

    # fetch model instances and write to file
    model_instances = get_model_instances()
    write_to_file(model_instances,'model_instances_metadata')

if __name__ == "__main__":
    main()