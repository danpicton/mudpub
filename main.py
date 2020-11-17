#!/usr/bin/env python3

import logging
import markdownbase
import argparse


def main():
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description='Publish a directory of markdown files.')
    parser.add_argument('source', type=str, help='source markdown directory')
    parser.add_argument('publish', type=str, help='target publish directory')
    parser.add_argument('--attachments', type=str, nargs=1, help='source attachments directory')
    parser.add_argument('--files', type=str, nargs='+', help='specific files to publish')
    parser.add_argument('--deadurl', type=str, nargs=1, help='URL for deactivated link note')

    args = parser.parse_args()

    if not args.attachments:
        args.attachments = "attachments"

    if not args.files:
        args.files = []

    if not args.deadurl:
        args.deadurl = "https://github.com/danpicton/mudpub/blob/main/README.md#selective-publication"

    mdb = markdownbase.MarkdownBase(args.source)
    mdb.index_source(specific_pages=args.files)  # this will feed build_page_models
    mdb.index_source(args.attachments)  # this can be called for specific files, later, according to links
    mdb.build_page_models()
    mdb.define_publish_list()
    # mdb.convert_local_refs()
    mdb.sanitise_dead_links(args.deadurl)
    publish_target = mdb.create_publish_target(args.publish)
    publish_target.publish_markdown()  # <- by this method too
    publish_target.publish_attachments()
    # output exceptions
    mdb.output_exceptions()

if __name__ == '__main__':
    main()
