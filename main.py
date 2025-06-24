import os
import shutil
from pathlib import Path

def mainFunc():
    print("This is the main function.")
    HOME_DIR_PATH = Path.home()
    CONFIG_DIR_PATH = f"{HOME_DIR_PATH}/.config"
    DOTIFILES_DIR_PATH = f"{HOME_DIR_PATH}/dotfiles"
    DOTIFLES_CONFIG_DIR_PATH = f"{DOTIFILES_DIR_PATH}/.config"
    DOTIGNORE_FILE_PATH = f"{DOTIFILES_DIR_PATH}/.dotignore"

    files_from_dotfiles = _getFilesInDotfiles(DOTIFILES_DIR_PATH)
    _pretty_show(f"files_from_dotfiles: {files_from_dotfiles}")

    files_from_dotignore = _getFilesFromDotignore(DOTIGNORE_FILE_PATH)

    try:
        _pretty_show(f"files_from_dotignore: {files_from_dotignore}")
        unique_home_files = _getUniqueFilesFromHomeDir(files_from_dotfiles, files_from_dotignore)
        _pretty_show(f"unique_home_files: {unique_home_files}")
        _linkHomeFilesToDotfiles(unique_home_files, DOTIFILES_DIR_PATH, HOME_DIR_PATH)
    except Exception as e:
        _pretty_show(f"An error occurred while reading {DOTIGNORE_FILE_PATH}: {e}")

    dotfiles_config_dirs = _getDirsDotfilesConfig(DOTIFLES_CONFIG_DIR_PATH)
    print(f"dotfiles_config_dirs: {dotfiles_config_dirs}")
    udir_pathnique_config_dirs = _getUniqueDirsFromDotfilesConfig(dotfiles_config_dirs, files_from_dotignore)
    print(f"udir_pathnique_config_dirs: {udir_pathnique_config_dirs}")

    _linkConfigDirsToDotfiles(udir_pathnique_config_dirs, DOTIFILES_DIR_PATH, CONFIG_DIR_PATH)

def _linkConfigDirsToDotfiles(unique_config_dirs, dotfiles_dir_path, config_dir_path):
    for dir in unique_config_dirs:
        source = f"{dotfiles_dir_path}/.config/{dir}"
        destination = Path(config_dir_path)
        try:
            if not Path(source).exists():
                print(f"Source directory {source} does not exist.")
                continue
            
            destination = destination / dir
            if destination.exists() or destination.is_symlink():
                print(f"Removing existing path: {destination}")
                if destination.is_symlink() or destination.is_file():
                    destination.unlink()
                elif destination.is_dir():
                    shutil.rmtree(destination)
            
            destination.symlink_to(source)
            print(f"Linked {source} to {destination}")

        except Exception as e:
            print(f"Failed to link {source} to {destination}: {e}")

def _linkHomeFilesToDotfiles(unique_home_files, dotfiles_dir_path, HOME_DIR_PATH):
    for file in unique_home_files:
        source = f"{dotfiles_dir_path}/{file}"
        destination = Path(HOME_DIR_PATH)
        try:
            if not Path(source).exists():
                print(f"Source file {source} does not exist.")
                continue
            
            destination = destination / file
            if destination.exists():
                print(f"Destination {destination} already exists. Skipping link creation.")
                os.remove(destination)  # Remove existing file before linking
            
            destination.symlink_to(source)
            print(f"Linked {source} to {destination}")

        except Exception as e:
            print(f"Failed to link {source} to {destination}: {e}")

def _getUniqueDirsFromDotfilesConfig(dirs_from_dotfiles, dirs_from_dotignore):
    return set(dirs_from_dotfiles) - set(dirs_from_dotignore)

def _getDirsDotfilesConfig(CONFIG_DIR_PATH):
    try:
        return _getDirsInDir(CONFIG_DIR_PATH)
    except FileNotFoundError:
        print(f"Directory {CONFIG_DIR_PATH} not found.")
        return []

def _getUniqueFilesFromHomeDir(files_from_dotfiles, files_from_dotignore):
    return set(files_from_dotfiles) - set(files_from_dotignore)

def _getFilesFromDotignore(dotignore_file_path):
    try:
        with open(dotignore_file_path, 'r') as file:
            return [line.strip() for line in file if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        print(f"File {dotignore_file_path} not found.")
        return []

def _getFilesInDotfiles(dotfile_dir_path):
    files = _getFilesInDir(dotfile_dir_path)
    return [f for f in files if f not in dotfile_dir_path]
    
def _getFilesInDir(dir_path):
    try:
        return [f.name for f in Path(dir_path).iterdir() if f.is_file()]
    except FileNotFoundError:
        print(f"Directory {dir_path} not found.")
        return []

def _getDirsInDir(dir_path):
    try:
        return [d.name for d in Path(dir_path).iterdir() if d.is_dir()]
    except FileNotFoundError:
        print(f"Directory {dir_path} not found.")
        return []

def _pretty_show(data):
    print("=================================================")
    if type(data) is list:
        for item in data:
            print(item)
    else:
        print(data)
    print("=================================================")

if __name__ == "__main__":
    mainFunc()
