import os
import shutil
from pathlib import Path

from classes.Print import Print


class Dotfiles:
    def __init__(self):
        self.HOME_DIR_PATH = Path.home()
        self.CONFIG_DIR_PATH = f"{self.HOME_DIR_PATH}/.config"
        self.DOTIFILES_DIR_PATH = f"{self.HOME_DIR_PATH}/dotfiles"
        self.DOTIFLES_CONFIG_DIR_PATH = f"{self.DOTIFILES_DIR_PATH}/.config"
        self.DOTIGNORE_FILE_PATH = f"{self.DOTIFILES_DIR_PATH}/.dotignore"

    def start(self):
        files_from_dotfiles = self._getFilesInDotfiles()
        files_from_dotignore = self._getFilesFromDotignore()
        unique_home_files = self._getUniqueFilesFromHomeDir(
            files_from_dotfiles, files_from_dotignore)
        dotfiles_config_dirs = self._getDirsDotfilesConfig()
        unique_config_dirs = self._getUniqueDirsFromDotfilesConfig(
            dotfiles_config_dirs, files_from_dotignore)
        self._linkHomeFilesToDotfiles(
            unique_home_files, self.DOTIFILES_DIR_PATH, self.HOME_DIR_PATH)
        self._linkConfigDirsToDotfiles(
            unique_config_dirs, self.DOTIFLES_CONFIG_DIR_PATH, self.CONFIG_DIR_PATH)

    def deleteLinks(self):
        files_from_dotfiles = self._getFilesInDotfiles()
        files_from_dotignore = self._getFilesFromDotignore()
        unique_home_files = self._getUniqueFilesFromHomeDir(
            files_from_dotfiles, files_from_dotignore)
        dotfiles_config_dirs = self._getDirsDotfilesConfig()
        unique_config_dirs = self._getUniqueDirsFromDotfilesConfig(
            dotfiles_config_dirs, files_from_dotignore)

        self._deleteHomeFilesLinks(unique_home_files, self.HOME_DIR_PATH)
        self._deleteConfigDirsLinks(unique_config_dirs, self.CONFIG_DIR_PATH)

    def _deleteHomeFilesLinks(self, unique_home_files, HOME_DIR_PATH):
        for file in unique_home_files:
            destination = Path(HOME_DIR_PATH) / file
            try:
                if destination.exists() or destination.is_symlink():
                    Print.success(f"Removing existing link: {destination}")
                    destination.unlink()
                else:
                    Print.error(
                        f"File {destination} does not exist, skipping.")
            except Exception as e:
                Print.error(f"Failed to remove link for {file}: {e}")

    def _deleteConfigDirsLinks(self, unique_config_dirs, config_dir_path):
        for dir in unique_config_dirs:
            destination = Path(config_dir_path) / dir
            try:
                if destination.exists() or destination.is_symlink():
                    Print.success(f"Removing existing link: {destination}")
                    if destination.is_symlink() or destination.is_file():
                        destination.unlink()
                    elif destination.is_dir():
                        shutil.rmtree(destination)
                else:
                    Print.error(
                        f"Directory {destination} does not exist, skipping.")
            except Exception as e:
                Print.error(f"Failed to remove link for {dir}: {e}")

    def _linkConfigDirsToDotfiles(self, unique_config_dirs, dotfiles_dir_path, config_dir_path):
        for dir in unique_config_dirs:
            source = f"{dotfiles_dir_path}/{dir}"
            destination = Path(config_dir_path)
            try:
                if not Path(source).exists():
                    Print.error(f"Source directory {source} does not exist.")
                    continue

                destination = destination / dir
                if destination.exists() or destination.is_symlink():
                    Print.success(f"Removing existing path: {destination}")
                    if destination.is_symlink() or destination.is_file():
                        destination.unlink()
                    elif destination.is_dir():
                        shutil.rmtree(destination)

                destination.symlink_to(source)
                Print.success(f"Linked {source} to {destination}")

            except Exception as e:
                Print.error(f"Failed to link {source} to {destination}: {e}")

    def _linkHomeFilesToDotfiles(self, unique_home_files, dotfiles_dir_path, HOME_DIR_PATH):
        for file in unique_home_files:
            source = f"{dotfiles_dir_path}/{file}"
            destination = Path(HOME_DIR_PATH)
            try:
                if not Path(source).exists():
                    Print.error(f"Source file {source} does not exist.")
                    continue

                destination = destination / file
                if destination.exists():
                    Print.success(
                        f"Skipping {file} as it already exists in home directory.")
                    # Remove existing file before linking
                    os.remove(destination)

                destination.symlink_to(source)
                Print.success(f"Linked {source} to {destination}")

            except Exception as e:
                Print.error(f"Failed to link {source} to {destination}: {e}")

    def _getUniqueDirsFromDotfilesConfig(self, dirs_from_dotfiles, dirs_from_dotignore):
        return set(dirs_from_dotfiles) - set(dirs_from_dotignore)

    def _getDirsDotfilesConfig(self):
        return self._getDirsInDir(self.DOTIFLES_CONFIG_DIR_PATH)

    def _getUniqueFilesFromHomeDir(self, files_from_dotfiles=[], files_from_dotignore=[]):
        return set(files_from_dotfiles) - set(files_from_dotignore)

    def _getFilesFromDotignore(self):
        with open(self.DOTIGNORE_FILE_PATH, 'r') as file:
            return [line.strip() for line in file if line.strip() and not line.startswith('#')]

    def _getFilesInDotfiles(self):
        files = self._getFilesInDir(self.DOTIFILES_DIR_PATH)
        return [f for f in files if f not in self.DOTIFILES_DIR_PATH]

    def _getFilesInDir(self, dir_path):
        try:
            return [f.name for f in Path(dir_path).iterdir() if f.is_file()]
        except FileNotFoundError:
            Print.error(f"Directory {dir_path} not found.")
            return []

    def _getDirsInDir(self, dir_path):
        try:
            return [d.name for d in Path(dir_path).iterdir() if d.is_dir()]
        except FileNotFoundError:
            Print.error(f"Directory {dir_path} not found.")
            return []
