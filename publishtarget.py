import os


class PublishTarget:
    """
    A class representing a target directory for publishing to.
    """

    def __init__(self, publish_directory, publish_files, publish_attachments):
        self.publish_directory = publish_directory
        self.publish_target = {}
        self.publish_files = publish_files
        self.attachments = publish_attachments

    def define_publish_target(self, publish_target):
        self.publish_target = publish_target

    def create_publish_structure(self):
        if not os.path.exists(self.publish_directory):
            os.mkdir(self.publish_directory)

        if not os.path.exists(os.path.join(self.publish_directory, "attachments")):
            os.mkdir(os.path.join(self.publish_directory, "attachments"))

        for subfolder in self.publish_target.keys():
            dir_to_create = os.path.join(self.publish_directory, subfolder)
            if not os.path.exists(dir_to_create):
                os.mkdir(dir_to_create)

    def write_markdown(self):
        for subfolder, md in self.publish_target.items():
            f = open(os.path.join(self.publish_directory, subfolder, "index.md"), "w")
            f.write(md)

    def build_publish_dict(self):
        publish_dict = {}
        for pub_file in self.publish_files:
            pub_file.convert_local_refs()
            publish_dict[pub_file.get_publish_name()] = pub_file.dump_markdown()

        return publish_dict

    def publish_markdown(self):
    # def publish_markdown(self, pub_path: str):
        publish_dict = self.build_publish_dict()
        self.define_publish_target(publish_dict)
        self.create_publish_structure()
        self.write_markdown()

    def publish_attachments(self):
        for attachment in self.attachments:
            print(attachment.filename)