import json
import os

# saves the given data to a file
def save_recommendations_to_file(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f)

# loads the given data from a file
def load_recommendations_from_file(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}