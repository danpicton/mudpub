from lxml import etree
from reference import Reference


class Image(Reference):
    """
    A class representing a HTML image reference; inherits from Reference

    Additional properties:
        alt_text: str
            The alternate text for the image
        title: str
            The title text for the image
    """

    # relative_location: boolean
    #     Flag to denote whether link is relative or absolute

    def __init__(self, image_element: etree._Element):
        self.ref_target = image_element.get("src")
        self.alt_text = image_element.get("alt")
        self.title = image_element.get("title")

