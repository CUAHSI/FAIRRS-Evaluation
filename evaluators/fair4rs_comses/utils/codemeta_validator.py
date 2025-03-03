
import sys
# Import libraries for loading codemeta file and running codemeticulous validator
from codemeticulous.cli import load_and_create_model
from codemeticulous.convert import STANDARDS

def run_codemeticulous_validation(codemeta_file):
    """
    Validates the Codemeta JSON file using `codemeticulous` directly in Python.
    """

    try:
        model = STANDARDS['codemeta']["model"]  # Get Pydantic model for codemeta V3
        codemeta_metadata = load_and_create_model(codemeta_file, model)  # Run validation
        print(f"{codemeta_file} is a valid codemeta file.")
        # convert pydantic object to dict and return
        return(codemeta_metadata.dict())
    except ValueError as e:
        # if invalid codemeta file show errors and break
        print(f"Codemeta validation failed:\n{e}")
        sys.exit(1)