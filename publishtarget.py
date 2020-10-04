import os

class PublishTarget:
    """
    A class representing a target directory for publishing to.
    """

    def __init__(self, publish_directory):
        self.publish_directory = publish_directory
        self.subfolders = []

    def build_structure(self, directory_list):
        self.subfolders = directory_list

    def write_structure(self):
        if not os.path.exists(self.publish_directory):
            os.mkdir(self.publish_directory)

        for subfolder in self.subfolders:
            if not os.path.exists(subfolder):
                os.mkdir(os.path.join(self.publish_directory, subfolder))