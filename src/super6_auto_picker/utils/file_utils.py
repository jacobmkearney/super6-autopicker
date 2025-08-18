import os
import json
from typing import Optional


def save_json(data, filename):
    # Ensure the data directory exists
    data_dir = os.path.join(os.path.dirname(__file__), '../../../data')
    os.makedirs(data_dir, exist_ok=True)
    
    # Construct the full path
    file_path = os.path.join(data_dir, filename)
    
    # Save the JSON data
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)


def read_predictions(file_path):
    """Read predictions from a JSON file."""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: The file {file_path} could not be decoded.")
        return None