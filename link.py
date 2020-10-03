from lxml import etree
from reference import Reference


class Link(Reference):
    """
    A class representing a HTML link; inherits from Reference

    Additional properties:
        text: str
            The text description of the link (if present)
    """

    # relative_location: boolean
    #     Flag to denote whether link is relative or absolute

    def __init__(self, link_element: etree._Element):
        self.ref_target = link_element.get("href")
        self.text = link_element.text


