import pandas as pd
from typing import Dict, List

class CrosswalkLoader:
    """
    Loads the crosswalk CSV to map Codemeta fields to FAIR4RS indicators.
    """

    def __init__(self, csv_path: str):
        """
        Initializes the loader by reading the crosswalk CSV.
        """
        self.crosswalk_df = pd.read_csv(csv_path)

    def get_fair4rs_mapping(self) -> Dict[str, List[str]]:
        """
        Returns a mapping of FAIR4RS indicators to Codemeta fields.
        """
        mapping = {}
        for _, row in self.crosswalk_df.iterrows():
            fair_indicator = row["FAIR4RS_Indicator"]
            codemeta_field = row["Codemeta_Field"]

            if fair_indicator not in mapping:
                mapping[fair_indicator] = []
            mapping[fair_indicator].append(codemeta_field)

        return mapping

    def get_codemeta_mapping(self) -> Dict[str, List[str]]:
        """
        Returns a mapping of Codemeta fields to FAIR4RS indicators.
        """
        mapping = {}
        for _, row in self.crosswalk_df.iterrows():
            codemeta_field = row["Codemeta_Field"]
            fair_indicator = row["FAIR4RS_Indicator"]

            if codemeta_field not in mapping:
                mapping[codemeta_field] = []
            mapping[codemeta_field].append(fair_indicator)

        return mapping
