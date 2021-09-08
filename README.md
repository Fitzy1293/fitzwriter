# This is my static site generator for personal user

This is a hodgepodge way to make a a static site generator that works for me.
I haven't used this for anything outside of testing.

This is not meant for the wider world.


# How to use it?

You can configure a .toml like so to generate an .html file

```toml
[website]
url = 'fitzover.com'
blog = 'articles'

[article]
title = 'Static Site Generator'

[resources.markdown]
path = 'markdown.md'

[resources.style]
path = 'style.css'
```

To start a new article with a single .toml file in your directory.

This needs to be more robust, will probably mess up if there are multiple .toml files.

```shell
python tomltest.py init
```

After initialized.

```shell
python tomltest.py -f blog.toml
```



# Instant feedback with a live server.

To instantly see how it looks in the browser.

- Launch a live server however you want.
  - You can launch a basic HTTP server with python: ```python -m http.server 8000```
 
  - The functionality is also built into most editors. 

- Then run this command to have it update on save.

```shell
ls *.md | entr python tomltest.py -f blog.toml
```

