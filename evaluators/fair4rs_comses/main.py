import argparse
import json
import os
from evaluators import MyEvaluator
from utils.crosswalk_loader import CrosswalkLoader

def main(codemeta_file):

    # load evaluator and load/validate codemeta file
    evaluator = MyEvaluator(codemeta_file)
    codemeta_json = evaluator.validate_codemeta_file()
    
    # load evaluator methods crosswalk (calling crosswalk for now, may change)
    crosswalk = CrosswalkLoader(codemeta_json)
    eval_methods = crosswalk.map_evaluators_to_codemeta()

    # initialize dictionary of results  
    results = {}

    # get the evaluator method names from MyEvaluator class
    eval_method_names = [
    name for name in dir(evaluator)
    if "eval" in name and callable(getattr(evaluator, name))
]

    # run evalutions for each evaluator in MyEvaluator
    for method_name in eval_method_names:
        method = getattr(evaluator, method_name, None)
        # run evaluation and store/print result
        try:
            result = method(**eval_methods[method_name])
        # some evaluation methods need codemeta properties in crosswalk
        except KeyError:
            result = "Need codemeta property in crosswalk."
        # store and print result (logs are printed in evaluator methods)
        results[method_name] = result
        print(f"{method_name} result: {result}")

    return results


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Evaluate a Codemeta JSON file using FAIR4RS criteria.")
    parser.add_argument("codemeta_file", type=str, help="Path to the Codemeta JSON file.")
    args = parser.parse_args()
    
    main(args.codemeta_file)

