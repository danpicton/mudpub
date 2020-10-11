import os
import markdownpage
import publishtarget
import sourcefile
import re


class MarkdownBase:
    """
    A class representing a markdown note folder
    """

    def __init__(self, directory):
        self.directory = directory
        self.source_files = []
        self.md_files = []
        self.publish_files = []
        self.dead_links = []
        self.dead_link_note = "" # this will be passed through as properties
        # self.dead_web_refs = {}

    def index_source(self, source_directory: str = "", specific_pages: [str] = []) -> None:
        """
        Indexes source directory.

        Defaults to self.directory; specific filenames can be provided as string list
        """
        source_path = os.path.join(self.directory, source_directory)

        source_filenames = [file for file in os.listdir(source_path)
                            if os.path.isfile(os.path.join(source_path, file))]

        for filename in source_filenames:

            if len(specific_pages) > 0:
                if filename not in specific_pages:
                    continue

            self.source_files.append(sourcefile.SourceFile(self.directory, os.path.join(source_directory, filename)))

    def build_page_models(self) -> None:
        """
        Builds list of all MarkdownPage objects in self.directory.
        """
        markdown_sourcefile = [file for file in self.source_files if file.file_suffix == ".md"]

        for md in markdown_sourcefile:
            mdp = markdownpage.MarkdownPage(md)
            mdp.model_pages()
            self.md_files.append(mdp)
            # mdp.convert_local_refs()  # this might need dead links cleaned, in which case, it should be moved

    def is_dead_link(self, link_to_check: str) -> bool:
        """
        Determines if link_to_check has a valid target.
        """
        if link_to_check in self.dead_links:
            return True

        if link_to_check.ref_target not in [pubfile.source_file.linkified_name for pubfile in self.publish_files]:
            self.dead_links.append(link_to_check)
            return True

    def collate_dead_links(self) -> dict:
        """
        Returns dict mapping of SourceFile-to-publish to any dead Links.
        """
        page_dead_links = {}

        for pub_file in self.publish_files:
            dead_links = []

            for link in [links for links in pub_file.body_links if links.is_local_ref()]:
                if self.is_dead_link(link):
                    dead_links.append(link)

            if len(dead_links) > 0:
                page_dead_links[pub_file] = dead_links

        return page_dead_links

    def deactivate_dead_links(self, dead_links: dict):
        """
        Deactivates dead links.
        """
        for markdown_page, dead_links in dead_links.items():
            for link in dead_links:
                if len(self.dead_link_note) > 0:
                    replacement_text = f"_{link.text}_[*]({self.dead_link_note})"
                else:
                    replacement_text = f"_{link.text}_)"
                link_regex = re.compile(rf"\[{link.text}\]\({link.ref_target}\)")
                # link_regex = re.compile(rf"\[.*{link.text}.*\]\(.*{link.ref_target}.*\)")
                new_body_text = re.sub(link_regex, replacement_text, markdown_page.body_text)
                print(f"remove from {markdown_page.source_file.filename}: {link.ref_target}")
                markdown_page.body_text = new_body_text

    def sanitise_dead_links(self, dead_link_note):
        self.dead_link_note = dead_link_note
        self.deactivate_dead_links(self.collate_dead_links())

    def define_publish_list(self):
        """Filters md_files' MarkdownPage objects leaving only those  publish."""
        # TODO:
        #  * Possibly refactor to return the filtered list
        #  * Consider making this a dict {MarkdownPage: [Reference]}
        #    This will allow attachments not referenced by publish pages to be omitted from publishing.
        for pub_file in [md_file for md_file in self.md_files if md_file.publish]:
            self.publish_files.append(pub_file)

    def build_publish_dict(self):
        publish_dict = {}  # TODO: create a PublishTarget class
        for pub_file in self.publish_files:
            pub_file.convert_local_refs()
            publish_dict[pub_file.get_publish_name()] = pub_file.dump_markdown()
        return publish_dict

    def publish_markdown(self, pub_path: str):
        publish_dict = self.build_publish_dict()
        pt = publishtarget.PublishTarget(pub_path)
        pt.define_publish_target(publish_dict)
        pt.create_publish_structure()
        pt.write_markdown()

    def publish_attachments(self):
        pass


