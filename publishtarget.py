class PublishTarget:
    """
    A class representing a target directory for publishing to.
    """

    def __init__(self, publish_directory):
        self.publish_directory = publish_directory
        self.subfolders = []

