import argparse
import os
import logging
import tempfile

import config
import git_tools

# Set up basic configuration for logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

script_dir = os.path.dirname(os.path.abspath(__file__))

def create_new_library(name):
    if not isinstance(name, str):
        logging.error("Library name must be a string")
        return

    config_data = config.load_config()
    if config_data is None:
        return

    required_keys = ["lib_path", "github_token", "github_org"]
    for key in required_keys:
        if key not in config_data:
            logging.error(f"{key} not set in config")
            return

    # Create a temporary directory to avoid conflict with existing structure
    with tempfile.TemporaryDirectory() as temp_dir:
        logging.info(f"Using temporary directory {temp_dir} for library creation")

        new_library_path = os.path.join(temp_dir, name)

        # Create the necessary directories inside the temp folder
        if not git_tools.create_directories(new_library_path):
            return

        # Create files for the new library
        if not git_tools.create_files(new_library_path, name, config_data, script_dir):
            return

        # Initialize a Git repository inside the temporary directory
        if not git_tools.initialize_git_repo(new_library_path):
            return

        # Create a remote GitHub repository and get its URL
        repo_url = git_tools.create_remote_repo(name, config_data["github_token"], config_data["github_org"])
        if repo_url is None:
            return

        # Push the repository from the temp directory to the remote
        if not git_tools.push_to_remote(new_library_path, repo_url):
            return

        # Add the repository as a submodule to the main repository
        main_repo_path = os.path.normpath(os.path.join(script_dir, ".."))
        if not git_tools.add_git_submodule(main_repo_path, repo_url, name):
            return

        logging.info(f"Library created and pushed to {repo_url}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PDL Development Tools")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("init_config", help="Initialize the config file")
    library_parser = subparsers.add_parser("create_new_library",
                                           help="Initialize a new library")
    library_parser.add_argument("name", help="Name of the library")

    config_parser = subparsers.add_parser("config",
                                          help="Set a configuration value")
    config_parser.add_argument(
        "key",
        choices=["name", "email", "lib_path", "github_token", "github_org"])
    config_parser.add_argument("value")

    args = parser.parse_args()

    if args.command == "init_config":
        config.init_config()
    elif args.command == "create_new_library":
        create_new_library(args.name)
    elif args.command == "config":
        if args.key == "name":
            config.config_name(args.value)
        elif args.key == "email":
            config.config_email(args.value)
        elif args.key == "lib_path":
            config.config_lib_path(args.value)
        elif args.key == "github_token":
            config.config_github_token(args.value)
        elif args.key == "github_org":
            config.config_github_org(args.value)
    else:
        parser.print_help()
