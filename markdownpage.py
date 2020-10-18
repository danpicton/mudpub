import frontmatter
from frontmatter.default_handlers import YAMLHandler
import logging
import markdown
from lxml import etree
import link, image
import sourcefile
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

    def __init__(self, markdown_file: sourcefile.SourceFile):
        self.source_file = markdown_file
        self.frontmatter = {}
        self.body_links = []
        self.body_images = []
        self.parse_exceptions = [] # deadlinks, bad yaml, no content, contains wikilinks, unexpected local file suffix,
        self.body_text = ""
        self.publish = False

    def model_pages(self):
        """Reads in markdown file as MarkDownPage object."""
        self.parse_frontmatter()
        if self.publish:
            self.check_for_wikilinks()
            self.collect_references()

    def parse_frontmatter(self):
        """
        Splits md file into frontmatter and body.

        Reads publish flag from YAML and sets self.publish accordingly.
        """
        page_to_parse = frontmatter.load(self.source_file.full_path)

        if not self.is_valid_front_matter(page_to_parse):
            self.parse_exceptions.append("Invalid YAML front matter")
        else:
            self.frontmatter = page_to_parse.metadata
            self.body_text = page_to_parse.content

            if self.frontmatter.get("publish"):
                self.publish = True

    def dump_markdown(self) -> str:
        """Outputs frontmatter and body_text as .md file with YAML front matter."""
        post = frontmatter.Post(self.body_text, None, **self.frontmatter)
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
        if re.findall(wl_re, self.body_text):
            self.parse_exceptions.append("WikiLinks in markdown body")

    def collect_references(self):
        """Populates the pkm (local) references (links and images)."""

        markdownbody = markdown.markdown(self.body_text)
        # markdownbody = markdown.markdown(page_to_validate.content, extensions=['wikilinks'])

        doc = etree.fromstring(markdownbody, etree.HTMLParser())

        # collect links
        for link_element in doc.xpath('//a'):
            self.body_links.append(link.Link(link_element))

        # collect images
        for image_element in doc.xpath('//img'):
            self.body_images.append(image.Image(image_element))

    def get_publish_name(self):
        """Returns the slug under which page will be published."""
        # filename = os.path.basename(self.source_file)
        az_target = re.sub(r'[^A-Za-z0-9 .%]+', '', self.source_file.filename).lower()
        return os.path.splitext(az_target.replace(" ", "-"))[0]

    def convert_local_refs(self):
        """Converts modelled markdown file's references for publishing."""
        # to be run after all markdown models are built (will require dead link removal)

        # replace local links
        for pkm_link in self.body_links:
            if pkm_link.is_local_ref():
                self.replace_local_link(pkm_link)

        # replace local images refs (point to /attachments/...)
        for pkm_image in self.body_images:
            if pkm_image.is_local_ref():
                self.replace_local_image(pkm_image, "attachments")

    def replace_local_link(self, link_to_replace: str):
        """Replaces markdown link reference with publish reference."""
        link_re = re.escape(link_to_replace.ref_target)
        pr = link_to_replace.get_publish_ref()
        self.body_text = re.sub(link_re, pr, self.body_text, re.MULTILINE)

    def replace_local_image(self, link_to_replace, page_slug=""):
        """Replaces markdown image reference with publish reference."""
        link_re = re.escape(link_to_replace.ref_target)
        pr = link_to_replace.get_publish_ref(page_slug, True)
        self.body_text = re.sub(link_re, pr, self.body_text, re.MULTILINE)

    # create backlinks (graph traversal)
    # create custom extension for wikilinked images
    # allow publish of specific page
    # exception objects with warning, fatal status?