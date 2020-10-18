from lxml import etree
import re
import os  # possibly use this moe extensively


class Reference:
    """
    A class representing a web reference

    ref_target: str
        The target of the reference
    """
    VALID_LOCAL_FILE_SUFFIXES = ["." + suffix for suffix in ["md", "txt", "html", "png", "jpg",
                                                             "jpeg", "gif", "pdf", "csv"]]

    def __init__(self, link_element: etree._Element):
        self.ref_target = ""

    def get_publish_ref(self, directory: str = "", preserve_extension: bool = False) -> str:
        """
        Gets publish path for Reference.

        Converts to lower case; replaces spaces with hyphens.

        Removes reference suffix by default.
        """
        az_target = re.sub(r'[^A-Za-z0-9 .%]+', '', self.ref_target).lower()
        if preserve_extension:
            return os.path.join(os.path.sep, directory, az_target.replace("%20", "-"))
        else:
            ref_prefix = os.path.splitext(az_target.replace("%20", "-"))[0]
            return os.path.join(os.path.sep, directory, ref_prefix)

    def is_local_ref(self) -> bool:
        """
        Determines if Reference is local. Validates against accepted suffixes.

        Assumes all external references start with http_pattern.

        TODO: refactor to return: local, web, invalid (this will allow easier dead link cleansing)
        """
        # valid suffix and doesn't start http...
        http_pattern = r"https?://.*"

        if re.match(http_pattern, self.ref_target):
            return False

        link_suffix = os.path.splitext(os.path.basename(self.ref_target))[1]
        if link_suffix not in self.VALID_LOCAL_FILE_SUFFIXES:
            return False

        return True
