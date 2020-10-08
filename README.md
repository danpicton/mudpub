# mudpub - Markdown Note Publisher
Copies and modifies markdown notes to publish to a [GoHugo](https://gohugo.io) static site.

## Notes
- All external links should be qualified with the protocol `https://` or `http://`
- Only markdown files from the specified directory will be published (no subfolders)
- Attachments will be sourced from markdown directory, or its attachments sub directory
- All attachments are published to an attachments directory in Hugo's root content folder
- Publishes to Hugo's [content](https://gohugo.io/content-management/organization/) folder only (at present)

## Todo
- [ ] Automate git staging
- [ ] Add formatted git diffs to Chronolog
- [ ] Accommodate sub-folder publish targets
