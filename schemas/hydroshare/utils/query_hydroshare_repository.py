import os
import json
import requests
from typing import List, Dict
from hsclient import HydroShare
from hsmodels.schemas.aggregations import ModelProgramMetadata
from pydantic import ValidationError

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

def get_model_program_metadata(hs_instance,resource_id):
    """
    Get model program metadata through hsclient package.
    """



    # initialize metadata fields
    metadata = {}

    while True:
        try: 
            hs_res = hs_instance.resource(resource_id)
        except Exception as e:  
            # Check if the error message contains the specific 401 Unauthorized text
            error_message = str(e)
            if "status_code 401" in error_message:
                print(f"Resource https://hydroshare.org/resource/{resource_id} is discoverable or private.")             
            break
        
        try:
            for agg in hs_res.aggregations():
                agg_metadata = agg._retrieved_metadata
                if isinstance(agg_metadata, ModelProgramMetadata):
                    metadata['version'] = agg_metadata.version
                    metadata['programming_languages'] = agg_metadata.programming_languages
                    metadata['operating_systems'] = agg_metadata.operating_systems
                    metadata['code_repository'] = str(agg_metadata.code_repository)
                    metadata['rights'] = str(agg_metadata.rights.url)
                    metadata['software_type'] = agg_metadata.title
                    break #TODO: add handling if there are multiple model programs in a resource
        except ValidationError as e:
            print(f"Error accessing resource https://hydroshare.org/resource/{resource_id}: {e}")

        break

    return metadata    

def write_to_file(hs_instance,resources,output_folder):
    """
    Writes HydroShare resource metadata to file.
    """

    output_dir = os.path.abspath(os.path.join(os.getcwd(), "..", output_folder))
    os.makedirs(output_dir, exist_ok=True)

    for resource in resources:
        # use the resource id as input to hsclient and for output file naming
        resource_id = resource['short_id']

        # add file level metadata
        metadata = get_model_program_metadata(hs_instance,resource_id)

        # write metadata to file if resource contains model program
        if metadata: 
            # add resource level metadata 
            metadata['title'] = resource['title']
            metadata['availability'] = resource['availability']
            metadata['authors'] = resource['authors']
            metadata['subject'] = resource['subject']
            metadata['created'] = resource['created']
            metadata['modified'] = resource['modified']

            # use resource ID as file name
            filename = os.path.join(output_dir, f"{resource_id}.json")
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
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