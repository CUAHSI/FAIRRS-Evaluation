# Import evaluators
from evaluators.findability.F1_evaluator import F1_evaluator # FAIR evaluator
# Import libraries for loading codemeta file and running codemeticulous validator
from codemeticulous.cli import load_and_create_model
from codemeticulous.convert import STANDARDS
# Import type hints
from typing import Dict, Any
import sys


class FAIR4RS_Evaluation_Manager:
    """
    Manages and runs FAIR4RS evaluations.
    """

    def __init__(self, codemeta_file: str, validate: bool = True):
        """
        Initializes the evaluation manager and loads/validates metadata before running evaluations.
        """

        self.validate = validate
        self.codemeta_file = codemeta_file

        # run codemeticulous validation and return metadata
        self.codemeta_metadata = self.run_codemeticulous_validation()

        # Use validated metadata for evaluation
        # Start with F1 for now
        self.evaluators = [
            F1_evaluator(self.codemeta_metadata) 
        ]

    def run_codemeticulous_validation(self):
        """
        Validates the Codemeta JSON file using `codemeticulous` directly in Python.
        """

        try:
            model = STANDARDS['codemeta']["model"]  # Get Pydantic model for codemeta V3
            codemeta_metadata = load_and_create_model(self.codemeta_file, model)  # Run validation
            print(f"✅ {self.codemeta_file} is a valid codemeta file.")
            # convert pydantic object to dict and return
            return(codemeta_metadata.dict())
        except ValueError as e:
            # if invalid codemeta file show errors and break
            print(f"❌ Codemeta validation failed:\n{e}")
            sys.exit(1)

    def run_evaluation(self) -> Dict[str, Any]:
        """
        Runs all defined FAIR4RS evaluators and collects results.
        """
        results = {}
        for evaluator in self.evaluators:
            results.update(evaluator.evaluate())
        return results