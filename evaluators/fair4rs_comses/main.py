import json
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

    codemeta_filepath = 'schemas/examples/HydroTrend_codemeta.json'
    # codemeta_filepath = 'schemas/examples/chime.json'
    res = main(codemeta_filepath)
