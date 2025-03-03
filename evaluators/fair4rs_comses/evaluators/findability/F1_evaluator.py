# Import abstract base class for evaluation
from evaluators.base_evaluator import BaseEvaluator
# Import defined type hints for inputs and outputs
from evaluators.fair_models import FAIR4RSPrincipleEvaluation
# Import evaluator utility functions
from utils.evaluator_utils import check_for_operational_url
# Import codemeta parser
from utils.codemeta_parser import get_persistent_identifier_urls


class F1_evaluator(BaseEvaluator):
    """
    Evaluator for F1: Software is assigned a globally unique and persistent identifier.
    """

    def __init__(self, mapped_metadata):
        """
        Initializes the F1_evaluator and extracts relevant metadata based on the crosswalk mapping.
        """

        self.indicator = "F1"
        self.mapped_metadata = mapped_metadata

    def evaluate(self) -> FAIR4RSPrincipleEvaluation:
        """
        Evaluates F1.
        """

        results = [] 
        logs = []

        doi_urls = get_persistent_identifier_urls(self.mapped_metadata)

        for doi_url in doi_urls:

            result,log = check_for_operational_url(doi_url)

            results.append(result)
            logs.append(log)

        # Format evaluation result
        evaluation_result = {
            f"{self.indicator}_evaluation": 'PASS' if True in results else 'FAIL',
            f"{self.indicator}_evaluation_logs": logs,
            f"{self.indicator}_metadata": self.mapped_metadata
        }

        return evaluation_result