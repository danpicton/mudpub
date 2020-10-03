from lxml import etree
import re
import os  # possibly use this moe extensively


class Reference:
    """
    A class representing a web reference

    ref_target: str
        The target of the reference
    """
    VALID_LOCAL_FILE_SUFFIXES = ["md", "txt", "html", "png", "jpg", "jpeg", "gif", "pdf", "csv"]

    def __init__(self, link_element: etree._Element):
        self.ref_target = ""

    def get_publish_ref(self, directory="", preserve_extension=False):
        if preserve_extension:
            return directory + "/" + self.ref_target.replace("%20", "-").lower()
        else:
            ref_prefix = os.path.splitext(self.ref_target.replace("%20", "-").lower())[0]
            return directory + ref_prefix

    def is_local_ref(self):
        # valid suffix and doesn't start http...
        http_pattern = r"https?://.*"
        suffix_pattern = r".*\.(.*)$"

        if re.match(http_pattern, self.ref_target):
            return False

        link_suffix = re.search(suffix_pattern, self.ref_target)
        if link_suffix.group(1) not in self.VALID_LOCAL_FILE_SUFFIXES:
            return False

        return True
