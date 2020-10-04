import os


class MarkdownBase:
    """
    A class representing a markdown note folder
    """

    def __init__(self, directory):
        self.directory = directory
        self.md_files = []
        self.dead_local_refs = {}
        # self.dead_web_refs = {}

    def page_index(dir_to_index: str):
        for dir_to_walk in dir_to_index:
            for dirName, subdirList, fileList in os.walk(dir_to_walk):

                print('Found directory: %s' % dirName)
                for fname in fileList:
                    print('\t%s' % fname)