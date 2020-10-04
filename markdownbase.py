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

    def index_files(self, specific_pages: [str]):
        file_set = set()

        # Understand what this list comprehension is doing.
        # https://stackoverflow.com/questions/1192978/python-get-relative-path-of-all-files-and-subfolders-in-a-directory
        files = [os.path.relpath(os.path.join(dirpath, file), self.directory) for (dirpath, dirnames, filenames) in
                 os.walk(self.directory) for file in filenames]
]
        for file in files:
            print(file)

        # for dirName, subdirList, fileList in os.walk(self.directory):
        #
        #     print('Found directory: %s' % dirName)
        #     for fname in fileList:
        #         rel_dir = os.path.relpath(dirName, self.directory)
        #         rel_file = os.path.join(rel_dir, fname)
        #         file_set.add(rel_file)
        #         print('\t%s\t%s' % (dirName, fname))
        #         print(rel_file)