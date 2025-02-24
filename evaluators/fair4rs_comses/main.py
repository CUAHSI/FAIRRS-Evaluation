import json
import argparse
from services.evaluation_manager import FAIR4RS_Evaluation_Manager

def load_metadata(file_path: str):
    """
    Loads the Codemeta JSON file.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            metadata = json.load(file)
        print("Loaded Codemeta file.")
        return metadata
    except Exception as e:
        print(f"Error loading Codemeta file: {e}")
        exit(1)

def main(codemeta_file):
    """
    Main function to run the FAIR4RS evaluation.
    """

    # Load metadata
    metadata = load_metadata(codemeta_file)

    # Run evaluation
    print("Running FAIR4RS evaluation...")
    evaluation_manager = FAIR4RS_Evaluation_Manager(metadata)
    results = evaluation_manager.run_evaluation()

    # Print results
    print("FAIR4RS Evaluation Results:")
    print(json.dumps(results, indent=4))

    return results

if __name__ == "__main__":

    codemeta_filepath = 'schemas/examples/HydroTrend_codemeta.json'
    res = main(codemeta_filepath)
