from abc import ABC, abstractmethod
from typing import Dict, List, Union
# import defined type hints
from evaluators.fair_types import FAIR4RSMetadataInput, FAIR4RSPrincipleEvaluation

class BaseEvaluator(ABC):
    """Abstract base class for evaluating FAIR principles."""

    def __init__(self, metadata: FAIR4RSMetadataInput):
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
