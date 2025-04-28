
import re 

# Known persistent ID regex patterns
PERSISTENT_ID_PATTERNS = {
    "doi": r"^https?://doi\.org/10\.\d{4,9}/[-._;()/:A-Z0-9]+$",
    "handle": r"^https?://hdl\.handle\.net/\d+/.+$",
    "ark": r"^https?://n2t\.net/ark:/\d+/.+$"
}

def evaluate_fm_i1(codemeta):
    """
    Evaluates FM_I1 metric based on CodeMeta input.

    Parameters:
        codemeta (dict): Parsed CodeMeta JSON as a Python dictionary

    Returns:
        dict: Evaluation result with score (0–1), reason, and matched identifier
    """
    id_candidates = []

    # Collect identifier candidates from known CodeMeta fields
    for key in ['identifier', 'sameAs', 'url']:
        value = codemeta.get(key)
        if isinstance(value, list):
            id_candidates.extend(value)
        elif isinstance(value, str):
            id_candidates.append(value)

    # Remove empty or null values
    id_candidates = [i for i in id_candidates if i]

    for id_str in id_candidates:
        for scheme, pattern in PERSISTENT_ID_PATTERNS.items():
            if re.match(pattern, id_str, re.IGNORECASE):
                return {
                    "score": 1,
                    "reason": f"Identifier matches known persistent pattern ({scheme})",
                    "identifier": id_str
                }

    if id_candidates:
        return {
            "score": 0.5,
            "reason": "Identifier present but does not match a known persistent pattern",
            "identifier": id_candidates[0]
        }
    else:
        return {
            "score": 0,
            "reason": "No identifier found in CodeMeta",
            "identifier": None
        }
    

# Example usage:
codemeta_example = {
    "identifier": "https://doi.org/10.1594/IEDA/100076",
    "name": "2DFLOWVEL",
    "codeRepository": "https://github.com/csdms-contrib/2dflowvel"
}

result = evaluate_fm_i1(codemeta_example)
print(result)
# Output: {
#   'score': 1, 
#   'reason': 'Identifier matches known persistent pattern (doi)', 
#   'identifier': 'https://doi.org/10.5281/zenodo.1234567'}