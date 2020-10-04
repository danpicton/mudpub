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
FILES_TO_TEST_WITH = ["Landscaping my website.md", "Digital Gardens.md"]
HUGO_GIT_PATH = "/home/dan/projects/temp_python/ape-in-progress"
PUBLISH_DIRECTORY = "/home/dan/projects/temp_python/pub1"

def main():
    logging.basicConfig(level=logging.INFO)

    mdb = markdownbase.MarkdownBase(PUBLISH_SOURCE_ROOT)
    mdb.index_files(FILES_TO_TEST_WITH)  # this will feed build_page_models
    mdb.build_page_models(PUBLISH_SOURCE_ROOT, FILES_TO_TEST_WITH)
    mdb.build_publish_list()
    mdb.build_publish_structure(PUBLISH_DIRECTORY)
    #output exceptions


def split_yaml_md():


    page = frontmatter.load(filename)
    print(markdown.markdown(page.content))


if __name__ == '__main__':
    main()