import os
import logging
import frontmatter as frontmatter
from bs4 import BeautifulSoup
import markdown
import markdownbase
import frontmatter
import markdownpage
import argparse


# properties
# config = configparser.ConfigParser()
# config["PUBLISH_SOURCE_ROOT"] = "/home/dan/Documents/pkm/ever-nearly-ready"
# config["ATTACHMENTS_DIRECTORY"] = "attachments"  # path relative to PUBLISH_SOURCE_ROOT
# config["FILES_TO_TEST_WITH"] = ["Landscaping my website.md", "Digital Gardens.md"]
# config["HUGO_GIT_PATH"] = "/home/dan/projects/temp_python/ape-in-progress"
# config["PUBLISH_DIRECTORY"] = "/home/dan/projects/temp_python/pub1"
# config["DEAD_LINK_NOTE"] = "https://github.com/danpicton/mudpub/blob/main/README.md#selective-publication"


def main():
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description='Publish a directory of markdown files.')
    parser.add_argument('source', type=str, nargs=1, help='source markdown directory')
    parser.add_argument('--attachments', type=str, nargs=1, help='source attachments directory')
    parser.add_argument('--files', type=str, nargs='+', help='specific files to publish')
    parser.add_argument('publish', type=str, nargs=1, help='target publish directory')

    mdb = markdownbase.MarkdownBase(PUBLISH_SOURCE_ROOT)
    mdb.index_source(specific_pages=FILES_TO_TEST_WITH)  # this will feed build_page_models
    mdb.index_source(ATTACHMENTS_DIRECTORY) # this can be called for specific files, later, according to links
    mdb.build_page_models()
    mdb.define_publish_list()
    # mdb.convert_local_refs()
    mdb.sanitise_dead_links(DEAD_LINK_NOTE)
    mdb.publish_markdown(PUBLISH_DIRECTORY)     # <- by this method too
    mdb.publish_attachments()
    #output exceptions


if __name__ == '__main__':
    main()