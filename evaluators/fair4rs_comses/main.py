import json
import os
from services.evaluation_manager import FAIR4RS_Evaluation_Manager

def main(codemeta_file):
    """
    Main function to run the FAIR4RS evaluation.
    """

    # Run evaluation
    print("Running FAIR4RS evaluation...")
    evaluation_manager = FAIR4RS_Evaluation_Manager(codemeta_file)
    results = evaluation_manager.run_evaluation()

    # Print results
    print("FAIR4RS Evaluation Results:")
    print(json.dumps(results, indent=4))

    return results

if __name__ == "__main__":

    # Input codemeta file (JSON) under schema/examples
    codemeta_filename = 'chime.json'

    # Get the directory where main.py is located
    main_script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to the example JSON file (may change location of schema folder later)
    codemeta_filepath = os.path.normpath(os.path.join(main_script_dir, "..", "..", "schemas", "examples", codemeta_filename))

    res = main(codemeta_filepath)
