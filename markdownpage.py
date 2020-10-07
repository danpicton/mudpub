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

    REQUIRED_FRONT_MATTER_KEYS = set(["title", "publish"])

    def __init__(self, markdown_file: str):
        self.md_filename = markdown_file
        self.md_frontmatter = {}
        self.md_links = []
        self.md_images = []
        self.parse_exceptions = [] # deadlinks, bad yaml, no content, contains wikilinks, unexpected local file suffix,
        self.md_body = ""
        self.publish = False


    def build_file_model(self):
        """Reads in markdown file as MarkDownPage object"""
        # check for wikilinks and add page_exception see contains_wikilinks() below

        self.parse_frontmatter()
        self.check_for_wikilinks()
        self.collect_references()


    def convert_file_model(self):
        """Converts modelled markdown file to published state"""
        # to be run after all markdown models are built (will require dead link removal)

        for pkm_link in self.md_links:
            if pkm_link.is_local_ref():
                print()
                self.replace_local_link(pkm_link)

        for pkm_image in self.md_images:
            if pkm_image.is_local_ref():
                print()
                self.replace_local_image(pkm_image, self.get_publish_name())
        # replace local links with appropriate targets - this will be the friendly page name of the target
        # replace image references to local reference - this will get the friendly page name of the markdownpage as a parameter for a prefix to the location
        # create new friendly filename for markdownpage

    def parse_frontmatter(self):  # add return hint
        page_to_parse = frontmatter.load(self.md_filename)

        if not self.is_valid_front_matter(page_to_parse):
            self.parse_exceptions.append("Invalid YAML front matter")
        else:
            # page_to_parse.content = "blah"   # this can be manually edited and added later
            # self.front_matter = frontmatter.dumps(page_to_parse)  # this can be created after manually editing content
            # self.front_matter_dict = page_to_parse.metadata # necessary?
            self.md_frontmatter = page_to_parse.metadata
            # self.front_matter = frontmatter.dumps(page_to_parse)
            self.md_body = page_to_parse.content

            if self.md_frontmatter.get("publish"):
                self.publish = True

    def dump_markdown(self):
        """Outputs front_matter_dict and markdown_body as YAML frontmatter and body content .md file."""
        # will need to build up a post object - create a new one, add content, header, etc
        # frontmatter.dumps()
        post = frontmatter.Post(self.md_body, None, **self.md_frontmatter)
        dump =  frontmatter.dumps(post)
        
        return dump

    def is_valid_front_matter(self, page_to_validate: frontmatter.Post) -> bool:
        """Checks for YAML front matter and presence of REQUIRED_FRONT_MATTER_KEYS; returns false if not present."""

        return self.REQUIRED_FRONT_MATTER_KEYS.issubset(set(page_to_validate.metadata.keys()))

    def check_for_wikilinks(self):
        """
        Checks for [[WikiLinks]] and adds an exception
        """
        wl_re = re.compile(r"\[\[[\w0-9_ -]+\]\]")
        if re.findall(wl_re, self.md_body):
            self.parse_exceptions.append("WikiLinks in markdown body")


    def collect_references(self):
        """Populates the pkm (local) references (links and images)"""

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
        """Returns the slug under which page will be published """
        # TODO: allow for nested dirs
        filename = os.path.basename(self.md_filename)
        return os.path.splitext(filename.replace(" ", "-").lower())[0]
        # return publish_location + self.pkm_filename.replace(" ", "-").lower()

    def replace_local_link(self, link_to_replace, page_slug=""):
        # TODO: add preceding to replaced links / by default
        # link_re = re.compile(re.escape(link_to_replace))
        link_re = re.escape(link_to_replace.ref_target)
        pr = link_to_replace.get_publish_ref()
        self.md_body = re.sub(link_re, pr, self.md_body, re.MULTILINE)
        print(self.md_body)

    def replace_local_image(self, link_to_replace, page_slug=""):
        # TODO: verify paths relative to referencing md can see images
        # link_re = re.compile(re.escape(link_to_replace))
        link_re = re.escape(link_to_replace.ref_target)
        pr = link_to_replace.get_publish_ref(page_slug, True)
        self.md_body = re.sub(link_re, pr, self.md_body, re.MULTILINE)
        print(self.md_body)

    # create backlinks (graph traversal)
    # create custom extension for wikilinked images
    # allow publish of specific page
    # exception objects with warning, fatal status?