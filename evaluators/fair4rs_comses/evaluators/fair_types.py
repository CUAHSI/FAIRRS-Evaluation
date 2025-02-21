from typing import Dict, List, Union

# structure of codemeta file input
codemetaMetadata = Dict[str, Union[str, List[str]]]

# structure of relevant metadata used as input to evaluate one FAIR4RS principle
FAIR4RSMetadataInput = Dict[str, Union[str, List[str]]]

# structure of evaluation result for one FAIR4RS principle
FAIR4RSPrincipleEvaluation = Dict[str, Union[str, FAIR4RSMetadataInput]]

# structure of overall evaluation result across all FAIR4RS principles
FAIR4RSOverallEvaluation = Dict[str, FAIR4RSPrincipleEvaluation]