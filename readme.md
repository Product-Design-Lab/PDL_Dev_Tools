# PDL - Dev Tools

The `dev_tools.py` script helps you create template Arduino libraries.

## Project Setup

Place the `PDL_Dev_Tools` folder under the root directory of your project. Your project directory should look like the following example:

```sh
$ tree -a ..
..
├── .git/
├── .gitignore
├── .gitmodules
├── .vscode/
├── doc/
├── libraries/
├── main/
├── PDL_Dev_Tools/
│   ├── config.json
│   ├── dev_tools.py
│   ├── LICENSE
│   ├── readme.md
│   ├── requirements.txt
│   ├── tasks.json
├── README.md
└── Tests/
```

## Creating a GitHub Token

1. **Log into GitHub**: Go to [GitHub](https://github.com/) and log in with your account.
2. **Navigate to Settings**: Click on your profile picture in the upper-right corner and select "Settings" from the dropdown menu.
3. **Developer Settings**: Scroll down to the bottom of the left sidebar and click on "Developer settings".
4. **Personal Access Tokens**: In the Developer settings menu, click on "Personal access tokens".
5. **Generate New Token**: Click the "Generate new token" button.
6. **Select Scopes**: Give your token a descriptive name and select the scopes or permissions you want to grant this token. For creating repositories and pushing code, you will need at least the `repo` scope. Select `repo` and any other permissions you might need.
7. **Generate Token**: Click the "Generate token" button at the bottom of the page.
8. **Copy Token**: Your token will be displayed only once. Make sure to copy it and store it securely.

**Warning**: Do not commit and push your GitHub token to any repository. Ensure that your `config.json` file, which contains your GitHub token, is added to your `.gitignore` file to prevent it from being tracked by git. This will help keep your token secure and prevent unauthorized access to your GitHub account.

## Requirements

Before using the script, ensure you have the required Python package installed. You can install it using:

```bash
pip install -r requirements.txt
```

## What the Script Will Do to Create a New Library

When you run the command to create a new library using `dev_tools.py`, the script will perform the following steps:

1. **Create Directory Structure**: The script will create a new directory for the library with the specified name. Inside this directory, it will create subdirectories and template files commonly used in Arduino libraries (e.g., `src`, `example`, `library.properties`, `README.md`, `LICENSE`, etc.).

2. **Initialize a Local Git Repository**: The script will initialize a new git repository in the newly created library directory. It will then add all the template files to the git repository and commit them.

3. **Create a Remote Repository on GitHub**: The script will use the GitHub API to create a new remote repository under the specified GitHub organization. This requires a GitHub token with appropriate permissions to create repositories in the organization.

4. **Push the Local Repository to GitHub**: After creating the remote repository on GitHub, the script will add the remote URL to the local git repository, set the default branch to `main`, and push the initial commit to the remote repository.

5. **Add the Library as a Git Submodule**: Finally, the script will add the newly created library repository as a git submodule to the main project. This involves adding a reference to the library repository in the main project's `.gitmodules` file and the appropriate submodule configuration in the main project's `.git/config` file.

## Windows Usage

1. Create default **config.json** file.

    ```batch
    python .\dev_tools.py init_config
    ```

2. Edit the config file.

    ```batch
    python .\dev_tools.py config name "your name"
    python .\dev_tools.py config email "your email"
    python .\dev_tools.py config lib_path "library path"
    python .\dev_tools.py config github_token "your_github_token"
    python .\dev_tools.py config github_org "your_github_org"
    ```

3. Create library.

    ```batch
    python .\dev_tools.py create_new_library "sample_lib"
    ```

4. Navigate to the library folder.

    ```batch
    cd ..\libraries\"your library name"
    ```

### Windows Setup Example

```cmd
C:\Users\xl\Documents\vysum_firmware\PDL_Dev_Tools>python dev_tools.py init_config
Config file already exists

C:\Users\xl\Documents\vysum_firmware\PDL_Dev_Tools>python dev_tools.py config name "Peter"
Config updated: name = Peter

C:\Users\xl\Documents\vysum_firmware\PDL_Dev_Tools>python dev_tools.py config email "xutengl@outlook.com"
Config updated: email = xutengl@outlook.com

C:\Users\xl\Documents\vysum_firmware\PDL_Dev_Tools>python dev_tools.py config lib_path "..\libraries"
Config updated: lib_path = ..\libraries

C:\Users\xl\Documents\vysum_firmware\PDL_Dev_Tools>python dev_tools.py config github_token "your_github_token"
Config updated: github_token = your_github_token

C:\Users\xl\Documents\vysum_firmware\PDL_Dev_Tools>python dev_tools.py config github_org "Product-Design-Lab"
Config updated: github_org = Product-Design-Lab

C:\Users\xl\Documents\vysum_firmware\PDL_Dev_Tools>python dev_tools.py create_new_library "sample_lib"
Library created at ..\libraries\sample_lib
```

## Linux & MacOS Setup

1. Create default **config.json** file.

    ```bash
    python ./dev_tools.py init_config
    ```

2. Edit the config file.

    ```bash
    python dev_tools.py config name "Peter"
    python dev_tools.py config email "your email"
    python dev_tools.py config lib_path "library path"
    python dev_tools.py config github_token "your_github_token"
    python dev_tools.py config github_org "your_github_org"
    ```

3. Create library.

    ```bash
    python dev_tools.py create_new_library "example_lib"
    ```

4. Navigate to the new library directory.

    ```bash
    cd ../libraries/"your library name"
    ```

### Linux & MacOS Example

```bash
xl@XL-NUC MINGW64 ~/Documents/vysum_firmware (dev)
$ cd PDL_Dev_Tools/

xl@XL-NUC MINGW64 ~/Documents/vysum_firmware/PDL_Dev_Tools (dev)
$ python dev_tools.py init_config
Config file already exists

xl@XL-NUC MINGW64 ~/Documents/vysum_firmware/PDL_Dev_Tools (dev)
$ python dev_tools.py config name "Peter"
Config updated: name = Peter

xl@XL-NUC MINGW64 ~/Documents/vysum_firmware/PDL_Dev_Tools (dev)
$ python dev_tools.py config email "xutengl@outlook.com"
Config updated: email = xutengl@outlook.com

xl@XL-NUC MINGW64 ~/Documents/vysum_firmware/PDL_Dev_Tools (dev)
$ python dev_tools.py config lib_path "../libraries"
Config updated: lib_path = ../libraries

xl@XL-NUC MINGW64 ~/Documents/vysum_firmware/PDL_Dev_Tools (dev)
$ python dev_tools.py config github_token "your_github_token"
Config updated: github_token = your_github_token

xl@XL-NUC MINGW64 ~/Documents/vysum_firmware/PDL_Dev_Tools (dev)
$ python dev_tools.py config github_org "Product-Design-Lab"
Config updated: github_org = Product-Design-Lab

xl@XL-NUC MINGW64 ~/Documents/vysum_firmware/PDL_Dev_Tools (dev)
$ python dev_tools.py create_new_library "sample_lib"
Library created at ../libraries/sample_lib

xl@XL-NUC MINGW64 ~/Documents/vysum_firmware/PDL_Dev_Tools (dev)
$ cd ../libraries/sample_lib/

xl@XL-NUC MINGW64 ~/Documents/vysum_firmware/libraries/sample_lib (dev)
$ ls
example/  keywords.txt  library.properties  LICENSE  README.md  src/
```


## Removing a Submodule

If the submodule command fails and you need to remove the submodule, you can do so with the following steps:

1. **Remove the Submodule Entry**: Use `git rm` to remove the submodule entry from the repository.

    ```sh
    git rm --cached path_to_submodule
    ```

2. **Delete the Submodule Directory**: Manually delete the submodule directory from your filesystem.

    ```sh
    rm -rf path_to_submodule
    ```

3. **Update the `.gitmodules` File**: Open the `.gitmodules` file in your root repository and remove the corresponding submodule entry.

4. **Update the `.git/config` File**: Open the `.git/config` file in your root repository and remove the corresponding submodule entry under `[submodule "path_to_submodule"]`.

5. **Commit the Changes**: Commit the changes to your repository.

    ```sh
    git add .gitmodules
    git add .git/config
    git commit -m "Removed submodule"
    ```

By following these steps, you can successfully remove a submodule in case the command fails.

## Using tasks.json

The `tasks.json` file in your project allows you to automate various tasks related to creating and configuring Arduino libraries using the `dev_tools.py` script. To use the tasks defined in `tasks.json`, follow these steps:

1. **Copy tasks.json**: Ensure that the `tasks.json` file is located in the `.vscode` folder in your project directory. If it's not there, copy the `tasks.json` file to `.vscode`.

    ```bash
    cp tasks.json .vscode/
    ```

2. **Open Command Palette**: Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (MacOS) to open the Command Palette in Visual Studio Code.

3. **Run Task**: Type `Tasks: Run Task` and select it from the list.

4. **Select a Task**: Choose the task you want to run from the list of available tasks. For example, select `Create Arduino Library` to create a new library, or `Config Name` to set the configuration name.

5. **Follow Prompts**: Follow the prompts to provide the necessary inputs, such as the library name, configuration name, email, library path, GitHub token, or GitHub organization.

6. **Task Execution**: The selected task will execute the corresponding shell command to perform the desired action, such as creating a new library or updating the configuration.

By using these tasks, you can streamline the process of managing your Arduino libraries and configurations, making it easier to automate repetitive tasks and maintain consistency across your projects.

## Using c_cpp_properties.json
The c_cpp_properties.json file in your project is used to configure IntelliSense settings for C/C++ in Visual Studio Code. This file helps IntelliSense understand the include paths and definitions for your project, reducing squiggle lines for libraries and improving code suggestions.

To use the c_cpp_properties.json configuration:

1. **Copy c_cpp_properties.json**: Ensure that the c_cpp_properties.json file is located in the .vscode folder in your project directory. If it's not there, copy the file from the vscode_config_template folder:

```bash
cp vscode_config_template/c_cpp_properties.json .vscode/
```

2. **Open Command Palette**: Press Ctrl+Shift+P (Windows/Linux) or Cmd+Shift+P (MacOS) to open the Command Palette in Visual Studio Code.

3. **Select IntelliSense Configuration**: Type C/C++: Edit Configurations (UI) and select it from the list. This opens the configuration UI where you can manage IntelliSense settings. Choose Configuration: If you have multiple configurations, select the one that matches your system (e.g., ubuntu, windows, or mac). This ensures that IntelliSense uses the correct paths and definitions for your operating system.