from typing import Dict, List, Union, Optional
from pydantic import BaseModel

class FAIR4RSPrincipleEvaluation(BaseModel):
    """
    Model representing the evaluation of a single FAIR4RS principle.
    """
    evaluation: str  # Expected values: "pass", "fail", "not_evaluated"
    evaluation_logs: Optional[str] = None  # Log reasons for the result
    metadata: Optional[Dict[str, Union[str, List[str]]]] = None  # Store metadata directly as a dictionary