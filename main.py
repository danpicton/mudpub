import os
import logging
import frontmatter as frontmatter
from bs4 import BeautifulSoup
import markdown
import frontmatter
import markdownpage

# properties
PUBLISH_ROOT = "/home/dan/Documents/pkm/ever-nearly-ready"
FILES_TO_TEST_WITH = ["Landscaping my website.md", "Digital Gardens.md"]

def main():
    pages = []
    # parseme = "/home/dan/Documents/pkm/ever-nearly-ready/Disco.md"  # no yaml
    parseme = [os.path.join(PUBLISH_ROOT, f) for f in FILES_TO_TEST_WITH]  # valid
    # parseme = "/home/dan/Documents/Dan Test.md"

    logging.basicConfig( level=logging.INFO)
    logging.info("Starting main")
    for md in parseme:
        mdp = markdownpage.MarkdownPage(md)
        mdp.build_file_model()
        pages.append(mdp)
        # mdp.convert_file_model()

    #output exceptions


def split_yaml_md():


    page = frontmatter.load(filename)
    print(markdown.markdown(page.content))


if __name__ == '__main__':
    main()