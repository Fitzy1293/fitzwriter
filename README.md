# This is my static site generator for personal user

 This is a hodgepodge way to make a a static site generator that works for me.
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

```shell
python tomltest.py init
```

After initialized.

```shell
python tomltest.py -f blog.toml
```



# Using with a live server

Launch a live server however you want.
Then run this command to have it update on save.

```shell
ls *.md | entr python tomltest.py -f blog.toml
```

This lets you edit markdown files with instant feedback on how it will look in the browser.
