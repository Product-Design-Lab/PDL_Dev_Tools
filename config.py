import os
import json
import logging
import shutil

script_dir = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILENAME = os.path.join(script_dir, "config.json")

DEFAULT_CONFIG = {
    "name": "PDL",
    "email": "name@example.com",
    "lib_path": os.path.join("..", "libraries"),
    "github_token": "your_github_token",
    "github_org": "Product-Design-Lab"
}


def init_config():
    _init_vscode_config()
    _init_file_structure()

    if os.path.exists(CONFIG_FILENAME):
        logging.info("Config file already exists")
        return

    try:
        with open(CONFIG_FILENAME, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        logging.info("Config file created")
    except IOError as e:
        logging.error(f"Failed to create config file: {e}")


def load_config():
    try:
        with open(CONFIG_FILENAME, "r") as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        logging.error("Config file does not exist")
        return None
    except json.JSONDecodeError:
        logging.error("Config file is not valid JSON")
        return None


def config_name(name):
    _set_config("name", name)


def config_email(email):
    _set_config("email", email)


def config_lib_path(path):
    _set_config("lib_path", path)


def config_github_token(token):
    _set_config("github_token", token)


def config_github_org(org):
    _set_config("github_org", org)


def _merge_json_files(dest_file, src_file, output_file):
    """
    Merges two JSON files, with src_file overwriting values in dest_file,
    and writes the result to output_file.
    """
    try:
        with open(dest_file, 'r') as f:
            dest_data = json.load(f)
    except (IOError, json.JSONDecodeError):
        dest_data = {}

    try:
        with open(src_file, 'r') as f:
            src_data = json.load(f)
    except (IOError, json.JSONDecodeError):
        src_data = {}

    merged_data = {**dest_data, **src_data}

    with open(output_file, 'w') as f:
        json.dump(merged_data, f, indent=4)


def _init_vscode_config():
    # Define paths relative to the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    vscode_dir = os.path.join(script_dir, '..',
                              '.vscode')  # .vscode at the same level as main
    tasks_src = os.path.join(script_dir, 'vscode_config_template',
                             'tasks.json')
    cpp_properties_src = os.path.join(script_dir, 'vscode_config_template',
                                      'c_cpp_properties.json')

    # Ensure the .vscode directory exists
    if not os.path.exists(vscode_dir):
        os.makedirs(vscode_dir)
        logging.info(f"Created .vscode directory at {vscode_dir}")

    # Copy tasks.json if it does not exist
    tasks_dest = os.path.join(vscode_dir, 'tasks.json')
    try:
        if not os.path.exists(tasks_dest) and os.path.exists(tasks_src):
            shutil.copy(tasks_src, tasks_dest)
            logging.info(f"Copied tasks.json to {tasks_dest}")
        elif os.path.exists(tasks_dest):
            _merge_json_files(tasks_dest, tasks_src, tasks_dest)
            logging.info(f"Merged tasks.json into {tasks_dest}")
        else:
            logging.error("tasks.json does not exist in the source directory.")
    except Exception as e:
        logging.error(f"Failed to handle tasks.json: {e}")

    # Copy c_cpp_properties.json if it does not exist
    cpp_properties_dest = os.path.join(vscode_dir, 'c_cpp_properties.json')
    try:
        if not os.path.exists(cpp_properties_dest) and os.path.exists(
                cpp_properties_src):
            shutil.copy(cpp_properties_src, cpp_properties_dest)
            logging.info(
                f"Copied c_cpp_properties.json to {cpp_properties_dest}")
        elif os.path.exists(cpp_properties_dest):
            _merge_json_files(cpp_properties_dest, cpp_properties_src,
                              cpp_properties_dest)
            logging.info(
                f"Merged c_cpp_properties.json into {cpp_properties_dest}")
        else:
            logging.error(
                "c_cpp_properties.json does not exist in the source directory."
            )
    except Exception as e:
        logging.error(f"Failed to handle c_cpp_properties.json: {e}")

    # Optionally, check if both files were handled successfully
    copied_tasks = os.path.exists(tasks_dest)
    copied_cpp_properties = os.path.exists(cpp_properties_dest)

    if copied_tasks and copied_cpp_properties:
        logging.info(
            "Both VS Code configuration files were handled successfully.")
    else:
        logging.error(
            "One or both VS Code configuration files could not be handled.")


def _init_file_structure():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    main_dir = os.path.join(script_dir, "../", 'main')
    library_dir = os.path.join(script_dir, "../", 'libraries')

    # Create 'main' directory if it doesn't exist
    if not os.path.exists(main_dir):
        os.makedirs(main_dir)
        logging.info(f"Created directory: {main_dir}")

    # Create 'libraries' directory if it doesn't exist
    if not os.path.exists(library_dir):
        os.makedirs(library_dir)
        logging.info(f"Created directory: {library_dir}")


def _set_config(key, val):
    if not os.path.exists(CONFIG_FILENAME):
        logging.error(
            "Config file does not exist, creating default config file")
        init_config()
        return

    try:
        with open(CONFIG_FILENAME, "r") as f:
            config = json.load(f)
    except (IOError, json.JSONDecodeError) as e:
        logging.error(f"Failed to read the config file: {e}")
        return

    config[key] = val

    try:
        with open(CONFIG_FILENAME, "w") as f:
            json.dump(config, f, indent=4)
        logging.info(f"Config updated: {key} = {val}")
    except IOError as e:
        logging.error(f"Failed to write to the config file: {e}")
