# Import validators & evaluators
from schemas.codemeta_models import CodemetaMetadata  # Codemeta validation
from evaluators.findability.F1_evaluator import F1_evaluator # FAIR evaluator
# Import type hints
from typing import Dict, Any

class FAIR4RS_Evaluation_Manager:
    """
    Manages and runs FAIR4RS evaluations.
    """

    def __init__(self, metadata: Dict[str, Any]):
        """
        Initializes the evaluation manager and validates metadata before running evaluations.
        """

        # # skipping this for now
        # # Validate Codemeta metadata (raises an error if invalid)
        # self.validated_metadata = CodemetaMetadata(**metadata) 
        
        self.metadata = metadata
        
        # Use validated metadata for evaluation
        # Start with F1 for now
        self.evaluators = [
            F1_evaluator(self.metadata)  # Ensure metadata is passed in correct format
        ]
    
    def run_evaluation(self) -> Dict[str, Any]:
        """
        Runs all defined FAIR4RS evaluators and collects results.
        """
        results = {}
        for evaluator in self.evaluators:
            results.update(evaluator.evaluate())
        return results