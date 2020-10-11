import os
import logging
import frontmatter as frontmatter
from bs4 import BeautifulSoup
import markdown
import markdownbase
import frontmatter
import markdownpage

# properties
PUBLISH_SOURCE_ROOT = "/home/dan/Documents/pkm/ever-nearly-ready"
ATTACHMENTS_DIRECTORY = "attachments" # path relative to PUBLISH_SOURCE_ROOT
FILES_TO_TEST_WITH = ["Landscaping my website.md", "Digital Gardens.md"]
HUGO_GIT_PATH = "/home/dan/projects/temp_python/ape-in-progress"
PUBLISH_DIRECTORY = "/home/dan/projects/temp_python/pub1"
DEAD_LINK_NOTE = "https://github.com/danpicton/mudpub/blob/main/README.md#selective-publication"


def main():
    logging.basicConfig(level=logging.INFO)

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