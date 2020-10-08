import frontmatter
from frontmatter.default_handlers import YAMLHandler
import logging
import markdown
from lxml import etree
import link, image
import re
import os

class MarkdownPage:
    """
    A class representing a single markdown page.

    filename: str
        The name of the source
    front_matter: dict
        Metadata parsed from the file's YAML frontmatter
    markdown_body: str
        Markdown portion of file (i.e. anything after the frontmatter)
    hugo_target_filename: str
        Target filename for Hugo
    hugo_target_path: str
        Target path for Hugo
    """

    REQUIRED_FRONT_MATTER_KEYS = set(["title", "publish"]) # TODO: Review these

    def __init__(self, markdown_file: str):
        self.md_filename = markdown_file
        self.md_frontmatter = {}
        self.md_links = []
        self.md_images = []
        self.parse_exceptions = [] # deadlinks, bad yaml, no content, contains wikilinks, unexpected local file suffix,
        self.md_body = ""
        self.publish = False

    def build_file_model(self):
        """Reads in markdown file as MarkDownPage object."""
        self.parse_frontmatter()
        self.check_for_wikilinks()
        self.collect_references()

    def convert_file_model(self):
        """Converts modelled markdown file to publish state."""
        # to be run after all markdown models are built (will require dead link removal)

        # replace local links
        for pkm_link in self.md_links:
            if pkm_link.is_local_ref():
                print()
                self.replace_local_link(pkm_link)

        # replace local images refs (point to /attachments/...)
        for pkm_image in self.md_images:
            if pkm_image.is_local_ref():
                print()
                self.replace_local_image(pkm_image, "attachments")

    def parse_frontmatter(self):
        """
        Splits md file into frontmatter and body.

        Reads publish flag from YAML and sets self.publish accordingly.
        """
        page_to_parse = frontmatter.load(self.md_filename)

        if not self.is_valid_front_matter(page_to_parse):
            self.parse_exceptions.append("Invalid YAML front matter")
        else:
            self.md_frontmatter = page_to_parse.metadata
            self.md_body = page_to_parse.content

            if self.md_frontmatter.get("publish"):
                self.publish = True

    def dump_markdown(self) -> str:
        """Outputs md_frontmatter and md_body as .md file with YAML front matter."""
        post = frontmatter.Post(self.md_body, None, **self.md_frontmatter)
        markdown_file = frontmatter.dumps(post)
        
        return markdown_file

    def is_valid_front_matter(self, page_to_validate: frontmatter.Post) -> bool:
        """Checks for YAML front matter and presence of REQUIRED_FRONT_MATTER_KEYS; returns false if not present."""

        return self.REQUIRED_FRONT_MATTER_KEYS.issubset(set(page_to_validate.metadata.keys()))

    def check_for_wikilinks(self):
        """
        Checks for [[WikiLinks]] and adds an exception.
        """
        wl_re = re.compile(r"\[\[[\w0-9_ -]+\]\]")
        if re.findall(wl_re, self.md_body):
            self.parse_exceptions.append("WikiLinks in markdown body")

    def collect_references(self):
        """Populates the pkm (local) references (links and images)."""

        markdownbody = markdown.markdown(self.md_body)
        # markdownbody = markdown.markdown(page_to_validate.content, extensions=['wikilinks'])

        doc = etree.fromstring(markdownbody, etree.HTMLParser())

        # collect links
        for link_element in doc.xpath('//a'):
            self.md_links.append(link.Link(link_element))

        # collect images
        for image_element in doc.xpath('//img'):
            self.md_images.append(image.Image(image_element))

    def get_publish_name(self):
        """Returns the slug under which page will be published."""
        filename = os.path.basename(self.md_filename)
        return os.path.splitext(filename.replace(" ", "-").lower())[0]

    def replace_local_link(self, link_to_replace: str):
        """Replaces markdown link reference with publish reference."""
        link_re = re.escape(link_to_replace.ref_target)
        pr = link_to_replace.get_publish_ref()
        self.md_body = re.sub(link_re, pr, self.md_body, re.MULTILINE)
        print(self.md_body)

    def replace_local_image(self, link_to_replace, page_slug=""):
        """Replaces markdown image reference with publish reference."""
        link_re = re.escape(link_to_replace.ref_target)
        pr = link_to_replace.get_publish_ref(page_slug, True)
        self.md_body = re.sub(link_re, pr, self.md_body, re.MULTILINE)
        print(self.md_body)

    # create backlinks (graph traversal)
    # create custom extension for wikilinked images
    # allow publish of specific page
    # exception objects with warning, fatal status?