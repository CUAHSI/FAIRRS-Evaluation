import argparse
import json
import os
from evaluators import MyEvaluator
from utils.crosswalk_loader import CrosswalkLoader
import scoring
from weights import WEIGHTS

def main(codemeta_file):

    # load evaluator and load/validate codemeta file
    evaluator = MyEvaluator(codemeta_file)
    codemeta_json = evaluator.validate_codemeta_file()
    
    # load evaluator methods crosswalk (calling crosswalk for now, may change)
    crosswalk = CrosswalkLoader(codemeta_json)
    eval_mapping = crosswalk.map_evaluators_to_codemeta()

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
            result = method(**eval_mapping[method_name])
        # some evaluation methods need codemeta properties in crosswalk
        except KeyError as e:
            print(f"{method_name} logs: relevant field(s) not in codemeta file.")
            result = False
        # store and print result (logs are printed in evaluator methods)
        indicator = method_name[4:]
        results[indicator] = result
        print(f"{indicator} result: {result}")
        
    # Compute FAIR scores
    scores = scoring.compute_indicator_scores(results, WEIGHTS)
    print("\nWeighed FAIR Scores (unnormalized):")
    print(scores)
    # print("\n🎯 FAIR Scores (0 to 1 scale):")
    # for principle, score in scores.items():
    #     print(f"  {principle}: {score}")

    return results,scores


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Evaluate a Codemeta JSON file using FAIR4RS criteria.")
    parser.add_argument("codemeta_file", type=str, help="Path to the Codemeta JSON file.")
    args = parser.parse_args()
    
    main(args.codemeta_file)

