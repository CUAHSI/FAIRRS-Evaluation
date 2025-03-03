from abc import ABC, abstractmethod
from typing import Dict, Any
# import defined type hints
from evaluators.fair_models import FAIR4RSPrincipleEvaluation

class BaseEvaluator(ABC):
    """
    Abstract base class for evaluating FAIR4RS principle.
    """

    def __init__(self, metadata: Dict[str, Any]):
        """
        Initializes the evaluator with relevant fields from codemeta for given FAIR4RS principle.
        """

        self.metadata: metadata

    @abstractmethod
    def evaluate(self) -> FAIR4RSPrincipleEvaluation:
        """
        Evaluates FAIR4RS principle with relevant fields from codemeta.
        """
        pass
