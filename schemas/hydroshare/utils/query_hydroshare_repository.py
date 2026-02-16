import os
import json
import requests
from typing import List, Dict
from hsclient import HydroShare
from pydantic import ValidationError
from datetime import datetime, date
from pydantic import AnyUrl


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

def custom_json_encoder(obj):
    """
    Handles non-standard types like date, datetime, Url, and Enums for JSON serialization.
    """
    # Handle datetime.date and datetime.datetime objects
    if isinstance(obj, (date, datetime)):
        # Convert date and datetime objects to ISO format strings
        return str(obj)
    
    # Handle Pydantic's Url/AnyUrl objects
    elif isinstance(obj, AnyUrl):
        # Convert Url objects to strings
        return str(obj)
        
    # Handle Enums (like AggregationType.ModelProgramAggregation)
    elif hasattr(obj, 'value'): 
        return obj.value
        
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

def log_failed_resource(resource_id, error_type, output_dir):
    """
    Appends the failed resource ID and error type to a specified log file.
    """

    log_filename = os.path.join(output_dir,"failed_extraction_logs.txt")
    log_entry = f"https://hydroshare.org/resource/{resource_id}, error code = {error_type}\n"
    
    # Use 'a' for append mode. 'w' would overwrite the file.
    with open(log_filename, 'a') as f:
        f.write(log_entry)

def write_to_file(hs_instance,resources,output_folder):
    """
    Writes HydroShare resource metadata to file.
    """

    output_dir = os.path.abspath(os.path.join(os.getcwd(), "..", output_folder))
    os.makedirs(output_dir, exist_ok=True)

    for resource in resources:
        # use the resource id as input to hsclient and for output file naming
        resource_id = resource['short_id']
        print(f'Analyzing https://hydroshare.org/resource/{resource_id}')

        try: 
            hs_res = hs_instance.resource(resource_id)
            extract_hs_res_metadata = True

            try:
                for agg in hs_res.aggregations(type='ModelProgram'):

                    # extract aggregation level metadata per iteration
                    agg_metadata = agg._retrieved_metadata.model_dump()
                    # extract resource level metadata once per resource
                    if extract_hs_res_metadata:
                        hs_res_metadata = hs_res._retrieved_metadata.model_dump()
                        extract_hs_res_metadata = False

                    # add creators and published status directly from resource level metadata
                    agg_metadata['resource_id'] = resource_id
                    agg_metadata['creators'] = hs_res_metadata['creators']
                    agg_metadata['published'] = hs_res_metadata['published'] if 'published' in hs_res_metadata else None

                    # add resource level metadata where revelevant aggregation level metadata fields are empty or non-existant
                    agg_metadata['subjects'] = agg_metadata['subjects'] if 'subjects' in agg_metadata else hs_res_metadata['subjects']
                    if 'spatial_coverage' not in agg_metadata:
                        if 'spatial_coverage' in hs_res_metadata:
                            agg_metadata['spatial_coverage'] = hs_res_metadata['spatial_coverage']
                        else:
                            agg_metadata['spatial_coverage'] = None
                    if 'period_coverage' not in agg_metadata:
                        if 'period_coverage' in hs_res_metadata:
                            agg_metadata['period_coverage'] = hs_res_metadata['period_coverage']
                        else:
                            agg_metadata['period_coverage'] = None
                    
                    # use aggreagation title as file name
                    filename = os.path.join(output_dir, f"{resource_id}-{agg_metadata['title']}.json")
                    with open(filename, "w", encoding="utf-8") as f:
                        json.dump(agg_metadata, f, indent=2, ensure_ascii=False,default=custom_json_encoder)
                    print(f"Saved to file: {filename}")

            except Exception as e:
                    error_type = "AGG_METADATA_EXTRACTION_ERROR"
                    log_failed_resource(resource_id, error_type, output_dir)
                    print(f"Full Error: {error_message}")            

        except Exception as e:
            error_message = str(e)
            # 1. Targeted Handling for the 401 Unauthorized Error
            if "Failed GET" in error_message and "status_code 401" in error_message:
                error_type = "401_UNAUTHORIZED"
                log_failed_resource(resource_id, error_type,output_dir)
            # 2. Handling for a 404 Not Found or other specific status codes
            elif "status_code 404" in error_message:
                error_type = "404_NOT_FOUND"
                log_failed_resource(resource_id, error_type, output_dir)
            # 3. Handling all other exceptions (Network errors, internal library issues, etc.)
            else:
                error_type = "UNKNOWN_RES_METADATA_EXTRACTION_ERROR"
                log_failed_resource(resource_id, error_type, output_dir)
                print(f"Full Error: {error_message}")

def main():

    hs = HydroShare()
    hs.sign_in()

    # fetch model program resources and write to file
    model_programs_ids = get_model_programs()
    # extract metadata from model programs resource ids and write to file
    write_to_file(hs,model_programs_ids ,'model_program_metadata')

if __name__ == "__main__":
    main()