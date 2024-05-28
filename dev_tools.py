import argparse
import json
import os
import sys
import logging
import subprocess
import shutil
import requests

# Set up basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Determine the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILENAME = os.path.join(script_dir, "config.json")

DEFAULT_CONFIG = {
    "name": "PDL",
    "email": "name@example.com",
    "lib_path": os.path.join("..", "libraries"),
    "github_token": "your_github_token",  # Add your GitHub token here
    "github_org": "Product-Design-Lab"  # Add the organization name here
}

def init_config():
    if os.path.exists(CONFIG_FILENAME):
        logging.info("Config file already exists")
        return

    try:
        with open(CONFIG_FILENAME, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        logging.info("Config file created")
    except IOError as e:
        logging.error(f"Failed to create config file: {e}")

def _set_config(key, val):
    if not os.path.exists(CONFIG_FILENAME):
        logging.error("Config file does not exist, creating default config file")
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

def create_directories(new_library_path):
    try:
        os.makedirs(os.path.join(new_library_path, "src"))
        os.makedirs(os.path.join(new_library_path, "example", "demo"))
    except OSError as e:
        logging.error(f"Failed to create directories: {e}")
        return False
    return True

def create_files(new_library_path, name, config):
    file_structure = {
        os.path.join("src", f"{name}.h"): '#pragma once\n\n',
        os.path.join("src", f"{name}.cpp"): f'#include "{name}.h"\n\n',
        os.path.join("example", "demo", "demo.ino"): 
            '#include <Arduino.h>\n#include <{0}.h>\n\nvoid setup() \n{{\n\n}}\nvoid loop() \n{{\n\n}}\n'.format(name),
        "library.properties": 
            f'name={name}\nversion=0.0.0\nauthor={config["name"]}\nmaintainer={config["name"]} <{config["email"]}>\n'
            'sentence=Short description of the library\nparagraph=Longer description of the library\ncategory=\nurl=http://example.com\n',
        "keywords.txt": f'{name} KEYWORD1\n',
        "README.md": f'# {name}\n\n',
    }

    for file_path, content in file_structure.items():
        try:
            with open(os.path.join(new_library_path, file_path), "w") as f:
                f.write(content)
        except IOError as e:
            logging.error(f"Failed to write file {file_path}: {e}")
            return False

    # Copy the LICENSE file
    try:
        shutil.copyfile(os.path.join(script_dir, "LICENSE"), os.path.join(new_library_path, "LICENSE"))
        logging.info("LICENSE file copied")
    except IOError as e:
        logging.error(f"Failed to copy LICENSE file: {e}")
        return False

    return True

def initialize_git_repo(new_library_path):
    try:
        subprocess.run(["git", "init"], cwd=new_library_path, check=True)
        subprocess.run(["git", "add", "."], cwd=new_library_path, check=True)
        subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=new_library_path, check=True)
        logging.info("Initialized git repository")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to initialize git repository: {e}")
        return False
    return True

def create_remote_repo(name, github_token, github_org):
    url = f"https://api.github.com/orgs/{github_org}/repos"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "name": name,
        "private": False
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        repo_url = response.json()["clone_url"]
        logging.info(f"Created remote repository: {repo_url}")
        return repo_url
    else:
        logging.error(f"Failed to create remote repository: {response.json()}")
        return None

def push_to_remote(new_library_path, repo_url):
    try:
        subprocess.run(["git", "remote", "add", "origin", repo_url], cwd=new_library_path, check=True)
        subprocess.run(["git", "branch", "-M", "main"], cwd=new_library_path, check=True)
        subprocess.run(["git", "push", "-u", "origin", "main"], cwd=new_library_path, check=True)
        logging.info("Pushed to remote repository")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to push to remote repository: {e}")
        return False
    return True

def add_git_submodule(main_repo_path, repo_url, name):
    try:
        subprocess.run(["git", "submodule", "add", repo_url, os.path.join("libraries", name)], cwd=main_repo_path, check=True)
        logging.info("Added as git submodule")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to add as git submodule: {e}")
        return False
    return True

def create_new_library(name):
    if not isinstance(name, str):
        logging.error("Library name must be a string")
        return

    config = load_config()
    if config is None:
        return

    if "lib_path" not in config:
        logging.error("lib_path not set in config")
        return

    if "github_token" not in config:
        logging.error("github_token not set in config")
        return

    if "github_org" not in config:
        logging.error("github_org not set in config")
        return

    lib_path = config["lib_path"]
    if not os.path.isabs(lib_path):
        lib_path = os.path.normpath(os.path.join(script_dir, lib_path))

    new_library_path = os.path.join(lib_path, name)

    if os.path.exists(new_library_path):
        logging.error("Library with the same name already exists")
        return

    if not create_directories(new_library_path):
        return

    if not create_files(new_library_path, name, config):
        return

    if not initialize_git_repo(new_library_path):
        return

    repo_url = create_remote_repo(name, config["github_token"], config["github_org"])
    if repo_url is None:
        return

    if not push_to_remote(new_library_path, repo_url):
        return

    main_repo_path = os.path.normpath(os.path.join(script_dir, ".."))
    if not add_git_submodule(main_repo_path, repo_url, name):
        return

    logging.info(f"Library created at {new_library_path}")

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PDL Development Tools")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("init_config", help="Initialize the config file")
    library_parser = subparsers.add_parser("create_new_library", help="Initialize a new library")
    library_parser.add_argument("name", help="Name of the library")

    config_parser = subparsers.add_parser("config", help="Set a configuration value")
    config_parser.add_argument("key", choices=["name", "email", "lib_path", "github_token", "github_org"])
    config_parser.add_argument("value")

    args = parser.parse_args()

    if args.command == "init_config":
        init_config()
    elif args.command == "create_new_library":
        create_new_library(args.name)
    elif args.command == "config":
        if args.key == "name":
            config_name(args.value)
        elif args.key == "email":
            config_email(args.value)
        elif args.key == "lib_path":
            config_lib_path(args.value)
        elif args.key == "github_token":
            config_github_token(args.value)
        elif args.key == "github_org":
            config_github_org(args.value)
    else:
        parser.print_help()
