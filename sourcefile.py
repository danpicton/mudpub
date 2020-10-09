import os


class SourceFile:
    """
    Class representing a source file.
    """
    def __init__(self, base_directory: str, relative_path:str):
        self.relative_path = relative_path
        self.full_path = os.path.join(base_directory, self.relative_path)
        self.filename = os.path.basename(self.full_path)
        self.file_prefix, self.file_suffix = os.path.splitext(self.filename)
        self.linkified_name = self.__linkify_filename()

    def __linkify_filename(self) -> str:
        return self.filename.replace(" ", "%20")