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
        self.source_file_objs = []
        self.md_files = []
        self.publish_files = []
        self.dead_links = []
        # self.dead_web_refs = {}

    def index_source(self, source_directory: str = "", specific_pages: [str] = []):
        source_path = os.path.join(self.directory, source_directory)

        source_filenames = [file for file in os.listdir(source_path)
                            if os.path.isfile(os.path.join(source_path, file))]

        for filename in source_filenames:
            self.source_file_objs.append(sourcefile.SourceFile(self.directory, os.path.join(source_directory, filename)))
            if len(specific_pages) > 0:
                if filename in specific_pages:
                    self.source_files.append(filename)
            else:
                self.source_files.append(filename)

        # for dirName, subdirList, fileList in os.walk(self.directory):
        #
        #     print('Found directory: %s' % dirName)
        #     for fname in fileList:
        #         rel_dir = os.path.relpath(dirName, self.directory)
        #         rel_file = os.path.join(rel_dir, fname)
        #         file_set.add(rel_file)
        #         print('\t%s\t%s' % (dirName, fname))
        #         print(rel_file)

    def build_page_models(self, publish_root, file_list):

        parseme = [os.path.join(publish_root, f) for f in file_list]  # will ultimately use all files if !file_list

        for md in parseme:
            mdp = markdownpage.MarkdownPage(md)
            mdp.build_file_model()
            self.md_files.append(mdp)
            mdp.convert_file_model() # this might need dead links cleaned, in which case, it should be moved


    def define_publish_list(self):
        """Creates list of MarkDownPage objects to publish."""
        for pub_file in [md_file for md_file in self.md_files if md_file.publish]:
            self.publish_files.append(pub_file)

    def build_publish_dict(self):
        publish_dict = {} # TODO: create a PublishTarget class
        for pub_file in self.publish_files:
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

    def sanitise_dead_links(self):
        pass