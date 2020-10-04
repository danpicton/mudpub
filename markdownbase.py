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

    def build_page_models(self, specific_pages: [str]):
        for dirName, subdirList, fileList in os.walk(self.directory):

            print('Found directory: %s' % dirName)
            for fname in fileList:
                print('\t%s' % fname)