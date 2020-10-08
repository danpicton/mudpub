import os
import markdownpage
import publishtarget

class MarkdownBase:
    """
    A class representing a markdown note folder
    """

    def __init__(self, directory):
        self.directory = directory
        self.md_files = []
        self.publish_files = []
        self.dead_local_refs = {}
        # self.dead_web_refs = {}

    def index_files(self, specific_pages: [str]):
        file_set = set()

        # Understand what this list comprehension is doing.
        # https://stackoverflow.com/questions/1192978/python-get-relative-path-of-all-files-and-subfolders-in-a-directory
        files = [os.path.relpath(os.path.join(dirpath, file), self.directory) for (dirpath, dirnames, filenames) in
                 os.walk(self.directory) for file in filenames]

        for file in files:
            if file in specific_pages:
                print(file)

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
            mdp.convert_file_model()

    def build_publish_dict(self):
        publish_dict = {} # TODO: create a PublishTarget class
        for pub_file in [md_file for md_file in self.md_files if md_file.publish]:
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

    def build_page_ref_mappings(self):
        pass

    def publish_attachments(self):
        pass