# Import abstract base class for evaluation
from evaluators.base_evaluator import BaseEvaluator
# Import defined type hints for inputs and outputs
from evaluators.fair_models import FAIR4RSPrincipleEvaluation
# Import evaluator utility functions
from utils.evaluator_utils import check_for_operational_url, run_codemeticulous_validation


class F2_evaluator(BaseEvaluator):
    """
    Evaluator for F2: Software is described with rich metadata.
    """

    def __init__(self, codemeta_file, codemeta_metadata):
        """
        Initializes the F2_evaluator.
        """

        self.indicator = "F2"
        self.codemeta_metadata = codemeta_metadata
        self.codemeta_file = codemeta_file

    def evaluate(self) -> FAIR4RSPrincipleEvaluation:
        """
        Evaluates F2.
        """

        result,logs = run_codemeticulous_validation(self.codemeta_file,self.codemeta_metadata)

        # Format evaluation result
        evaluation_result = {
            f"{self.indicator}_evaluation": 'PASS' if result == True else 'FAIL',
            f"{self.indicator}_evaluation_logs": logs,
            f"{self.indicator}_metadata": 'N/A'
        }

        return evaluation_result