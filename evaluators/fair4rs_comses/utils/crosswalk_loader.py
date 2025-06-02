import pandas as pd
from typing import Dict, List, Any

# Define crosswalk file path
CROSSWALK_FILE = "crosswalks/fair4rs_to_codemeta.csv"

class CrosswalkLoader:
    """
    Loads a crosswalk CSV that maps FAIR4RS indicators to Codemeta fields.
    Uses Pandas for efficient processing and metadata extraction.
    """

    def __init__(self,codemeta_json):
        """
        Initializes the CrosswalkLoader and loads the FAIR4RS-to-Codemeta mapping.

        :param crosswalk_file: Path to the crosswalk CSV file.
        """

        self.crosswalk_file = CROSSWALK_FILE
        self.crosswalk_mapping = self._load_crosswalk()
        self.codemeta_json = codemeta_json

    def _load_crosswalk(self) -> Dict:
        """
        Loads the crosswalk CSV into a dictionary mapping FAIR4RS indicators to Codemeta fields.

        :param crosswalk_file: Path to the crosswalk CSV.
        :return: Dictionary {FAIR4RS Indicator → List of Codemeta Fields}
        """
        try:
            df = pd.read_csv(self.crosswalk_file).rename(columns=str.strip)

            # Ensure no NaN values exist
            df = df.dropna(subset=["evaluation_method", "codemeta"])

            # Convert Codemeta properties from a single string into a list
            df["codemeta"] = df["codemeta"].apply(
                lambda x: [field.strip() for field in x.split(" / ")] if isinstance(x, str) else [x]
            )
            # df["codemeta"] = df["codemeta"].apply(lambda x: [field.strip() for field in x.split(" / ")])

            # Create dictionary mapping FAIR4RS indicators to lists of Codemeta fields
            return df.set_index("evaluation_method")["codemeta"].to_dict()

        except Exception as e:
            print(f"Error loading crosswalk file: {e}")
            return {}

    def map_evaluators_to_codemeta(self) -> Dict:
        """
        Maps Codemeta metadata to all FAIR4RS indicators and returns a dictionary.

        :param codemeta_data: Parsed Codemeta JSON as a dictionary.
        :return: Dictionary where each FAIR4RS indicator maps to its relevant metadata.
        """

        fair4rs_metadata_mapping = {}

        for indicator, fields in self.crosswalk_mapping.items():
            # Extract only the fields that exist in Codemeta data
            relevant_metadata = {field: self.codemeta_json.get(field) for field in fields if field in self.codemeta_json}

            # Store only if there's relevant metadata
            if relevant_metadata:
                fair4rs_metadata_mapping[indicator] = relevant_metadata

        return fair4rs_metadata_mapping