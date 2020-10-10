import os
import markdownpage
import publishtarget
import sourcefile


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
        Builds list of MarkdownPage objects.
        """
        markdown_sourcefile = [file for file in self.source_files if file.file_suffix == ".md"]

        for md in markdown_sourcefile:
            mdp = markdownpage.MarkdownPage(md)
            mdp.model_pages()
            self.md_files.append(mdp)
            # mdp.convert_local_refs()  # this might need dead links cleaned, in which case, it should be moved

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
            print("publish: " + pub_file.get_publish_name())
            publish_dict[pub_file.get_publish_name()] = pub_file.dump_markdown()
        return publish_dict

    def publish_markdown(self, pub_path: str):
        publish_dict = self.build_publish_dict()
        pt = publishtarget.PublishTarget(pub_path)
        pt.define_publish_target(publish_dict)
        pt.create_publish_structure()
        pt.write_markdown()
        #
        print()

    def publish_attachments(self):
        pass

    def is_dead_link(self, link_to_check: str) -> bool:
        if link_to_check in self.dead_links:
            return True

        if link_to_check.ref_target not in [pubfile.source_file.linkified_name for pubfile in self.publish_files]:
            self.dead_links.append(link_to_check)
            return True

    def sanitise_dead_links(self):
        deadlinks = {}

        # for publish_filename in self.md_files.
        for pub_file in self.publish_files:
            for link in [links for links in pub_file.body_links if links.is_local_ref()]:
                if self.is_dead_link(link):
                    print("dead: " + link.ref_target)
                else:
                    print("live: " + link.ref_target)
        pass
