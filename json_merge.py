import json
import os

def merge_json_files(base_file_path, new_file_path, output_file_path):
    """
    Merges the contents of new_file_path into base_file_path and saves the result to output_file_path.
    """
    if not os.path.exists(base_file_path):
        raise FileNotFoundError(f"Base file {base_file_path} does not exist.")

    if not os.path.exists(new_file_path):
        raise FileNotFoundError(f"New file {new_file_path} does not exist.")

    try:
        # Load base JSON file
        with open(base_file_path, 'r') as base_file:
            base_data = json.load(base_file)

        # Load new JSON file
        with open(new_file_path, 'r') as new_file:
            new_data = json.load(new_file)

        # Merge new data into base data
        if isinstance(base_data, dict) and isinstance(new_data, dict):
            base_data.update(new_data)
        elif isinstance(base_data, list) and isinstance(new_data, list):
            base_data.extend(new_data)
        else:
            raise ValueError("Incompatible JSON structures. Merging not performed.")

        # Save merged data to output file
        with open(output_file_path, 'w') as output_file:
            json.dump(base_data, output_file, indent=4)
        print(f"Merged JSON data saved to {output_file_path}")

    except Exception as e:
        raise RuntimeError(f"An error occurred while merging JSON files: {e}")
