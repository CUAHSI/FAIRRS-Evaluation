import json
import os
from evaluators import MyEvaluator
from utils.crosswalk_loader import CrosswalkLoader

def main(codemeta_file):

    # load evaluator and load/validate codemeta file
    evaluator = MyEvaluator(codemeta_file)
    codemeta_json = evaluator.validate_codemeta_file()
    
    # load evaluator methods crosswalk
    crosswalk = CrosswalkLoader(codemeta_json)
    eval_methods = crosswalk.map_evaluators_to_codemeta()

    # initialize dictionary of results  
    results = {}

    # Get only method names that contain 'eval'
    eval_method_names = [
    name for name in dir(evaluator)
    if "eval" in name and callable(getattr(evaluator, name))
]

    # run evalutions for each evaluator
    for method_name in eval_method_names:
        # extract evaluation method from evaluator class
        method = getattr(evaluator, method_name, None)
        # run evaluation and store/print result
        try:
            result = method(**eval_methods[method_name])
        # some evaluation methods need codemeta properties in crosswalk
        except KeyError:
            result = "Need codemeta property in crosswalk."

        results[method_name] = result
        print(f"{method_name} result: {result}")

    return results


if __name__ == "__main__":

    # Input codemeta file (JSON) under schema/examples
    codemeta_filename = 'HydroTrend_codemeta.json'

    # Get the directory where main.py is located
    main_script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to the example JSON file (may change location of schema folder later)
    codemeta_filepath = os.path.normpath(os.path.join(main_script_dir, "..", "..", "schemas", "examples", codemeta_filename))

    res = main(codemeta_filepath)
