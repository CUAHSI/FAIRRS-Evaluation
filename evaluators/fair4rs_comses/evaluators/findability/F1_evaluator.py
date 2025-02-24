# Import abstract base class for evaluation
from evaluators.base_evaluator import BaseEvaluator
# Import defined type hints for inputs and outputs
from evaluators.fair_models import FAIR4RSPrincipleEvaluation
# Import crosswalk loader to map Codemeta fields to FAIR4RS indicators
from utils.crosswalk_loader import CrosswalkLoader  

# Define crosswalk file path
CROSSWALK_FILE = "crosswalks/codemeta2fair4rs.csv"

class F1_evaluator(BaseEvaluator):
    """
    Evaluator for F1: Software is assigned a globally unique and persistent identifier.
    """

    def __init__(self, metadata):
        """
        Initializes the evaluator and extracts relevant metadata based on the crosswalk mapping.
        """

        self.metadata = metadata

        # Load crosswalk mapping
        crosswalk_loader = CrosswalkLoader(CROSSWALK_FILE)
        crosswalk_mapping = crosswalk_loader.get_fair4rs_mapping()

        # Extract relevant fields for F1
        self.indicator = "F1"
        self.FAIR4RS_mapping = crosswalk_mapping.get(self.indicator, [])

    def evaluate(self) -> FAIR4RSPrincipleEvaluation:
        """
        Evaluates F1 based on mapped metadata.
        """

        # Default evaluation result
        not_evaluated_msg = "not_evaluated"

        # Extract only relevant metadata for this FAIR4RS indicator
        relevant_metadata = {
            key: value for key, value in self.metadata.items() if key in self.FAIR4RS_mapping
        }

        # Format evaluation result
        evaluation_result = {
            f"{self.indicator}_evaluation": not_evaluated_msg,
            f"{self.indicator}_evaluation_logs": not_evaluated_msg,
            f"{self.indicator}_metadata": {key: value for key, value in self.metadata.items() if key in self.FAIR4RS_mapping}
        }

        return evaluation_result