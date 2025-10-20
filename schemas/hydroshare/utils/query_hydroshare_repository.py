import os
import json
import requests
from typing import List, Dict
from hsclient import HydroShare
from hsmodels.schemas.aggregations import ModelProgramMetadata

def get_model_programs() -> List[Dict]:
    """
    Queries HydroShare API for metadata from all resources tagged as model programs.
    """

    model_programs = []
    page_num = 1
    previous_resources = None

    while True:
        response = requests.get(
            'https://hydroshare.org/discoverapi/?filter={%22type%22:[%22Model%20Program%22]}',
            params={'pnum': page_num}
        )
        json_response = response.json()
        resources = json.loads(json_response['resources'])

        if resources == previous_resources:
            break

        model_programs.extend(resources)
        previous_resources = resources
        page_num += 1

    return model_programs

def get_model_program_metadata(hs_instance,resource):
    """
    Get model program metadata through hsclient package.
    """
    
    hs_res_id = resource['short_id']
    hs_res = hs_instance.resource(hs_res_id)

    # initialize metadata fields
    resource['version'] = []
    resource['programming_languages'] = []
    resource['operating_systems'] = []
    resource['code_repository'] = []
    resource['rights'] = []

    for agg in hs_res.aggregations():
        metadata = agg._retrieved_metadata
        if isinstance(metadata, ModelProgramMetadata):
            resource['version'] += metadata.version
            resource['programming_languages'] += metadata.programming_languages
            resource['operating_systems'] += metadata.operating_systems
            resource['code_repository'] += metadata.code_repository
            resource['rights'] += metadata.rights.url

    return resource     

def write_to_file(hs_instance,resources,output_folder):
    """
    Writes HydroShare resource metadata to file.
    """

    output_dir = os.path.abspath(os.path.join(os.getcwd(), "..", output_folder))
    os.makedirs(output_dir, exist_ok=True)

    for resource in resources:

        # add file level metadata
        resource = get_model_program_metadata(hs_instance,resource)

        # use resource ID as file name
        filename = os.path.join(output_dir, f"{resource['short_id']}.json")
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(resource, f, indent=2, ensure_ascii=False)
        print(f"Saved to file: {filename}")

def main():

    hs = HydroShare()
    hs.sign_in()

    # fetch model program resources and write to file
    model_programs_ids = get_model_programs()
    # extract metadata from model programs resource ids and write to file
    write_to_file(hs,model_programs_ids ,'model_program_metadata')

if __name__ == "__main__":
    main()