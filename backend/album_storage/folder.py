import os
import shutil
from pathlib import Path


class Folder():
    """A class for interacting with a folder"""

    def __init__(self, base_dir, dir_name):
        self.base_dir = base_dir
        self.dir_name = dir_name
        self.create_folder_if_not_exist()

    def get_folder_contents(self):
        path_to_folder = self.get_path()
        return os.listdir(path_to_folder)

    def get_sorted_folder_contents(self):
        return sorted(self.get_folder_contents())

    def get_path(self):
        return os.path.join(
            self.base_dir,
            self.dir_name
        )

    def count_files(self):
        """Return number of files inside the folder"""
        return len(self.get_folder_contents())

    def get_path_to_file(self, filename):
        return os.path.join(
            self.get_path(),
            filename
        )

    def get_relative_url_to_file(self, filename):
        path_to_files = self.get_path_to_file(filename)
        path = list(Path(path_to_files).parts)
        return "/" + "/".join(path)

    def get_relative_urls_to_all_files(self):
        file_names = self.get_sorted_folder_contents()
        urls = list(map(
            lambda name: self.get_relative_url_to_file(name),
            file_names
        ))
        return urls

    def write_file_in_folder(self, filename, content):
        path_to_file = self.get_path_to_file(filename)
        with open(path_to_file, "w") as f:
            f.write(content)

    def read_file_in_folder(self, filename):
        path_to_file = self.get_path_to_file(filename)
        with open(path_to_file, "r") as f:
            return f.read()

    def file_exists_in_folder(self, filename):
        path_to_file = self.get_path_to_file(filename)
        return os.path.exists(path_to_file)

    def remove_all_folder_content(self):
        path_to_folder = self.get_path()
        shutil.rmtree(path_to_folder)
        os.mkdir(path_to_folder)

    def create_folder_if_not_exist(self):
        if not os.path.exists(self.get_path()):
            os.makedirs(self.get_path())
