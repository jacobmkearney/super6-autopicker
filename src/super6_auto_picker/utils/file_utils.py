import os
import json
import logging
from typing import Optional

logger = logging.getLogger(__name__)


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
        logger.error("The file %s was not found.", file_path)
        return None
    except json.JSONDecodeError:
        logger.error("The file %s could not be decoded.", file_path)
        return None