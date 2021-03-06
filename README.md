# mudpub - Markdown Note Publisher
Copies and modifies markdown notes to publish to a [GoHugo](https://gohugo.io) static site.

## Add as CLI tool
1. Create folder `~/.local/bin`:  
`mkdir ~/.local/bin`
2. Add `mudpub` file to `~/.local/bin` with contents:  
    ```
    #!/usr/bin/env bash
    source /home/username/path/to/mudpub/venv/bin/activate
    /usr/bin/env python3 /home/username/path/to/mudpub/mudpub.py
    ```
3. Change `mudpub` permissions:  
   `chmod u+x mudpub`
4. Add `~/.local/bin` to `PATH` in `~/.profile`:  
    ```
    # set PATH so it includes user's private bin if it exists
    if [ -d "$HOME/.local/bin" ] ; then
        PATH="$HOME/.local/bin:$PATH"
    fi
    ```

## Notes
- All external links should be qualified with the protocol `https://` or `http://`
- Only markdown files from the specified directory will be published (no subfolders)
- Attachments will be sourced from markdown directory, or a specified attachments sub directory
- All attachments are published to an attachments directory in Hugo's root content folder
- Selective publishing does not yet work for attachments 
- Written to run on POSIX systems
- Publishes to Hugo's [content](https://gohugo.io/content-management/organization/) folder only (at present)

## Features
### Selective Publication
Pages will be published only of they have valid YAML front-matter and configured with `publish: yes`. This results in
some local links leading nowhere (i.e. the referenced page isn't published). Links to such pages are deactivated prior
to publishing and look like this: _old link text_[*](https://github.com/danpicton/mudpub/blob/main/README.md#selective-publication)

## Todo
- [x] Remove invalid local links
- [x] Publish attachments
- [x] Output exceptions
- [x] Only allow alpha chars and spaces in publish names
- [ ] Refactor to run as command line app
- [ ] Ensure local links have `.md` suffix
- [ ] Add deactivated links to parse exceptions
- [ ] Add logging throughout
- [ ] Handle errors cleanly
- [ ] Refactor OO code
- [ ] Build tests
- [ ] Enable selective attachment publishing
- [ ] Index publish target directory (`path.walk`, not `listdir`)
- [ ] Ensure links to previously published sub-folder pages are not deactivated/cleansed
- [ ] Automate git staging
- [ ] Add formatted git diffs to Chronolog
- [ ] Accommodate sub-folder publish targets
