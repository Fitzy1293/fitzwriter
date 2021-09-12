[TOC]

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

# How to use it

This program is meant to read a simple config, and stylesheet, to create a nice looking page based on what's in based in the given markdown file.

## Configure a TOML file like below

```toml
[website]
url = 'fitzover.com'
blog = 'random'
favicon = 'fitzover.com/ghost.svg'

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
    python tomltest.py init
    ```

- If it was initialized earlier.

    ```
    python tomltest.py -f blog.toml
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

## This is just a little demonstration of the program, hope you enjoyed
