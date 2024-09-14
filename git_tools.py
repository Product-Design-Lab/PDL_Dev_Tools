import os
import git
import logging
import shutil
from git.exc import GitCommandError
import requests
import json

def is_directory_safe(directory):
    """
    Checks if the directory is already in Git's safe.directory globally.
    """
    try:
        # Use git command directly to check the global config
        logging.info("Checking if directory is in Git's safe.directory")
        repo = git.cmd.Git()  # Create a Git command interface without needing a specific repo
        git_config = repo.config('--global', '--get-all', 'safe.directory')
        safe_dirs = [d.replace("\\", "/") for d in git_config.strip().split('\n') if d]
        normalized_dir = os.path.abspath(directory).replace("\\", "/")

        # Check if the directory is in the safe list
        return normalized_dir in safe_dirs
    except GitCommandError as e:
        logging.error(f"Git command error while checking safe.directory: {e}")
        return False
    except Exception as e:
        logging.error(f"Error checking safe.directory: {e}")
        return False

def add_safe_directory(directory):
    """
    Adds the directory to Git's safe.directory globally.
    """
    try:
        # Normalize the directory path
        normalized_dir = os.path.abspath(directory).replace("\\", "/")
        logging.info(f"Adding {normalized_dir} to Git safe.directory")

        # Use Git command interface without loading a specific repository
        git_cmd = git.cmd.Git()

        # Add the directory to the global safe.directory configuration
        git_cmd.config('--global', '--add', 'safe.directory', normalized_dir)
        logging.info(f"Successfully added {normalized_dir} to Git safe.directory")

    except GitCommandError as e:
        logging.error(f"Failed to add {directory} to Git safe.directory: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred while adding safe.directory: {e}")

def initialize_git_repo(new_library_path):
    """
    Initializes a Git repository, configures safe.directory, adds files, and makes an initial commit.
    """
    try:
        # Normalize the path
        new_library_path = os.path.abspath(new_library_path).replace("\\", "/")
        logging.info(f"Normalized library path: {new_library_path}")

        # Initialize Git repository using GitPython
        repo = git.Repo.init(new_library_path)
        logging.info(f"Initialized Git repository in {new_library_path}")

        # Stage all files
        repo.git.add(all=True)
        logging.info("Added files to Git staging area.")

        # Commit changes
        repo.index.commit("Initial commit")
        logging.info("Performed initial commit.")

    except GitCommandError as e:
        logging.error(f"Failed to initialize git repository: {e}")
        return False
    except Exception as e:
        logging.error(f"An unexpected error occurred during Git initialization: {e}")
        return False

    return True

def create_remote_repo(name, github_token, github_org):
    # Ensure only the organization name is used
    github_org = github_org.split('/')[-1] if github_org.startswith("http") else github_org

    url = f"https://api.github.com/orgs/{github_org}/repos"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {"name": name, "private": False}

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
        repo = git.Repo(new_library_path)

        # Add remote 'origin'
        origin = repo.create_remote('origin', repo_url)
        logging.info(f"Added remote 'origin' with URL {repo_url}")

        # Rename current branch to 'main'
        if repo.active_branch.name != 'main':
            repo.git.branch('-M', 'main')
            logging.info("Renamed current branch to 'main'")

        # Push to remote and set upstream
        origin.push(refspec='main:main', set_upstream=True)
        logging.info("Pushed to remote repository")

    except GitCommandError as e:
        logging.error(f"Failed to push to remote repository: {e}")
        return False
    except Exception as e:
        logging.error(f"An unexpected error occurred while pushing to remote: {e}")
        return False
    return True

def add_git_submodule(main_repo_path, repo_url, name):
    try:
        logging.info(f"Main repository path: {main_repo_path}")
        logging.info(f"Repo URL: {repo_url}")
        logging.info(f"Name: {name}")
        # Open the main repository
        main_repo = git.Repo(main_repo_path, search_parent_directories=True)

        # Construct the submodule path within the 'libraries' folder
        libraries_dir = os.path.join(main_repo_path, "libraries")
        submodule_path = os.path.join(libraries_dir, name)

        # Normalize the path to avoid issues with different OS (Windows vs Unix)
        submodule_path = os.path.normpath(submodule_path)
        libraries_dir = os.path.normpath(libraries_dir)

        # Ensure the 'libraries' directory exists
        os.makedirs(libraries_dir, exist_ok=True)

        # Check if the submodule path already exists and is not empty
        if os.path.exists(submodule_path) and os.listdir(submodule_path):
            logging.error(f"Submodule path {submodule_path} already exists and is not empty.")
            return False

        # Check and add to safe.directory if not already present
        if not is_directory_safe(submodule_path):
            add_safe_directory(submodule_path)
        else:
            logging.info(f"{submodule_path} is already in Git safe.directory")

        # Add the submodule
        submodule = main_repo.create_submodule(name=name, path=submodule_path, url=repo_url)
        logging.info(f"Added submodule {name} at {submodule_path} pointing to {repo_url}")

    except GitCommandError as e:
        logging.error(f"Git command error while adding submodule: {e}")
        return False
    except Exception as e:
        logging.error(f"An unexpected error occurred while adding submodule: {e}")
        return False

    return True

def create_directories(new_library_path):
    try:
        os.makedirs(os.path.join(new_library_path, "src"))
        os.makedirs(os.path.join(new_library_path, "example", "demo"))
        logging.info(f"Created directories in {new_library_path}")
    except OSError as e:
        logging.error(f"Failed to create directories: {e}")
        return False
    return True

def delete_directories(new_library_path):
    try:
        shutil.rmtree(new_library_path)
        logging.info(f"Deleted directory: {new_library_path}")
    except OSError as e:
        logging.error(f"Failed to delete directories: {e}")
        return False
    return True

def create_files(new_library_path, name, config, script_dir):
    file_structure = {
        os.path.join("src", f"{name}.h"):
        '#pragma once\n\n',
        os.path.join("src", f"{name}.cpp"):
        f'#include "{name}.h"\n\n',
        os.path.join("example", "demo", "demo.ino"):
        '#include <Arduino.h>\n#include <{0}.h>\n\nvoid setup() \n{{\n\n}}\nvoid loop() \n{{\n\n}}\n'.format(name),
        "library.properties":
        f'name={name}\nversion=0.0.0\nauthor={config["name"]}\nmaintainer={config["name"]} <{config["email"]}>\n' \
        'sentence=Short description of the library\nparagraph=Longer description of the library\ncategory=\nurl=http://example.com\n',
        "keywords.txt":
        f'{name} KEYWORD1\n',
        "README.md":
        f'# {name}\n\n',
    }

    for file_path, content in file_structure.items():
        try:
            full_path = os.path.join(new_library_path, file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "w") as f:
                f.write(content)
            logging.info(f"Created file: {full_path}")
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
