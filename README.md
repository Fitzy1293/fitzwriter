
## Links
- [Github repo](https://github.com/fitzy1293/fitzwriter)

## Requirements

- Requires python 3.8 or greater, with two packages not in the standard library.

    ```
    pip install markdown toml
    ```

This requires X11 as the window manager, because it uses **xdotool** to update the Firefox tab.

- **Arch install**

    ```
    sudo pacman -S xdotool
    ```

- **Ubuntu install**

    ```
    sudo apt install xdotool
    ```

xdotool is what I used to implement automatically updating Firefox

# How to use it

This program is meant to read a simple config, and stylesheet, to create a nice looking page based on what's in based in the given markdown file.

## Configure a TOML file like below

```toml
[website]
url = 'example.com'
blog = 'articlestorage'
favicon = 'ghost.svg'

[article]
title = 'README'

[resources.markdown]
path = 'README.md'

[resources.style]
path = 'style.css'

```

### Running after setup

- Run this to initialize.

    ```
    python fitzwriter.py init
    ```

- If it was initialized earlier.

    ```
    python fitzwriter.py -f blog.toml
    ```

- To launch an HTTP server and view the updates on save.

    ```
    python fitzwriter.py -l -f blog.toml
    ```


# Features

## See changes in the browser on save

Right now it is set up to handle reloading on save, in Firefox.

- You can launch a basic HTTP server with python.

    ```
    python -m http.server 8000
    ```

    - Then open ***localhost:8000*** in Firefox.

- Or just open index.html in Firefox.

## Automatically create a table of contents

Just add ***\[TOC\]*** to the first line of the .md file to create a table of contents.


<!-- EXAMPLE OF EMBEDDING HTML
# Sample Tweet

<blockquote class="twitter-tweet">
    <p lang="en" dir="ltr">All smiles from our crew as we near launch of <a href="https://twitter.com/hashtag/Inspiration4?src=hash&amp;ref_src=twsrc%5Etfw">#Inspiration4</a>. <a href="https://t.co/UrBdOlxLPJ">pic.twitter.com/UrBdOlxLPJ</a></p>
    &mdash; Inspiration4 (@inspiration4x) <a href="https://twitter.com/inspiration4x/status/1437067512567451654?ref_src=twsrc%5Etfw">September 12, 2021</a>
</blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
-->
