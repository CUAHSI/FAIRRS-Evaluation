# Import evaluators
from evaluators.findability.F1_evaluator import F1_evaluator # FAIR evaluator
# Import type hints
from typing import Dict, Any
import sys
# Import crosswalk loader to map Codemeta fields to FAIR4RS indicators
from utils.crosswalk_loader import CrosswalkLoader
# Import codemeticulous validator
from utils.codemeta_validator import run_codemeticulous_validation


class FAIR4RS_Evaluation_Manager:
    """
    Manages and runs FAIR4RS evaluations.
    """

    def __init__(self, codemeta_file: str):
        """
        Initializes the evaluation manager and loads/validates metadata and loads/maps crosswalk before running evaluations.
        """

        # load metadata run codemeticulous validation to validate codemeta file
        codemeta_metadata = run_codemeticulous_validation(codemeta_file)

        # Load crosswalk mapping for FAIR4RS to codemeta
        crosswalk_loader = CrosswalkLoader()
        crosswalk_mapping = crosswalk_loader.map_codemeta_to_fair4rs(codemeta_metadata)

        # Load evaluators with mapped metadata for input indicator
        self.evaluators = [
            F1_evaluator(crosswalk_mapping['F1']) 
        ]

    def run_evaluation(self) -> Dict[str, Any]:
        """
        Runs all defined FAIR4RS evaluators and collects results.
        """

        results = {}
        for evaluator in self.evaluators:
            results.update(evaluator.evaluate())
        return results