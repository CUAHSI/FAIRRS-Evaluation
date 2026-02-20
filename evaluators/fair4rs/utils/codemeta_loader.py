import sys
import json

def load_codemeta_file(codemeta_file):
    try:
        with open(codemeta_file, "r") as file:
            return json.load(file)
    except:
        print(f'Codemeta file could not load: {codemeta_file}')
        sys.exit(1)