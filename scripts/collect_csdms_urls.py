#!/usr/bin/env python3

import json
import pandas
import requests

root_url = "https://csdms.colorado.edu/csdms_wiki/api.php?action=ask&query="
# q = 'query=[[Model:HydroTrend]]&format=json

query = (
    "[[Category:Models]]"
    + "|?ModelDomain"
    + "|?Source+web+address"
    + "|?Source+code+availability"
    + "|?CodeReviewed"
    + "|limit=10000"
)


res = requests.get(root_url + query + "&format=json")
if res.status_code == 200:
    data = res.json()
    cleaned_data = []
    for model, metadata in data["query"]["results"].items():
        meta = {
            "ModelName": model.split(":")[1],
            "ModelDomain": next(iter(metadata["printouts"]["ModelDomain"]), ""),
            "SourceWebAddress": next(
                iter(metadata["printouts"]["Source web address"]), ""
            ),
            "SourceCodeAvailability": next(
                iter(metadata["printouts"]["Source code availability"]), ""
            ),
            "CodeReviewed": next(iter(metadata["printouts"]["CodeReviewed"]), ""),
            "FullUrl": metadata["fullurl"],
        }
        cleaned_data.append(meta)
    df = pandas.DataFrame(cleaned_data)
    df.to_csv("csdms_models.csv")
else:
    print("Failed to fetch data")

print("Output saved to csdms_models.csv")
