import os
import logging
import frontmatter as frontmatter
from bs4 import BeautifulSoup
import markdown
import frontmatter
import markdownpage

# properties
PUBLISH_DIRS = ["/home/dan/Documents/pkm/ever-nearly-ready"]


def main():
    # parseme = "/home/dan/Documents/pkm/ever-nearly-ready/Disco.md"  # no yaml
    parseme = "/home/dan/Documents/pkm/ever-nearly-ready/Landscaping my website.md"  # valid
    # parseme = "/home/dan/Documents/Dan Test.md"

    logging.basicConfig( level=logging.INFO)
    logging.info("Starting main")

    mdp = markdownpage.MarkdownPage(parseme)
    mdp.build_file_model()
    mdp.convert_file_model()

    #output exceptions

def page_index(dirs_to_index: [str]):
    for dir_to_walk in dirs_to_index:
        for dirName, subdirList, fileList in os.walk(dir_to_walk):

            print('Found directory: %s' % dirName)
            for fname in fileList:
                print('\t%s' % fname)


def split_yaml_md():


    page = frontmatter.load(filename)
    print(markdown.markdown(page.content))


if __name__ == '__main__':
    main()