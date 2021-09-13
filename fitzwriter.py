#!/bin/env python3

'''
repo:   https://github.com/Fitzy1293/fitzwriter


This is a program for making html pages given a markdown file.
Perhaps it's a little silly to do this in python with no framework, but it's a good exercise.

Non stdlib packages: markdown, toml
    toml.load() to easily grab the config file into a parsable dict.
    markdown.markdown() to easily turn the markdown into html

There is waaaaaaaaaay more than I would like being done in the global scope here.
A lot of the global stuff is trying to exit on missing data needed for the program to run.
'''

import sys
from defaults import hard_coded_help # Might end up switching from using argpparse.

# Give a briefer help list, before doing anyting else.
# If someone just types "python tomltest.py" into their shell after installing, printing a shorter help and exiting as soon as possible is nice.
ARGC = len(sys.argv)
if ARGC == 1:
    sys.exit(f'{hard_coded_help()}')


from argparse import ArgumentParser, RawTextHelpFormatter
import os
CWD = os.getcwd()
github_repo = 'https://github.com/Fitzy1293/fitzwriter'
example_toml = f'{github_repo}/blob/master/blog.toml'

parser = ArgumentParser(
                          description=f'Fitzwriter - a static site generator\n{github_repo}\n To start:{" "* 14}python tomltest.py init',
                          formatter_class=RawTextHelpFormatter
                        )

parser.add_argument('init', default=False, nargs='?', metavar='init', help='''initializes if it finds a .toml with the right data''')

parser.add_argument('-l', '--loop', dest='LOOP', default=False, action='store_true',
                      help='''continuously update, whenever a change is made to the markdown file, then refresh Firefox
lets you see the what it will look like on an actual site after every save
does this by starting an http server and using xdotool to refresh
                            ''')
parser.add_argument('-f', '--toml', dest='TOML', default=False,
                      help='''explicitly enter the config file
the program tries to handle cases with missing fields

  [website]
  url = 'example.com'
  blog = 'myblog'
  favicon = 'example.com/favicon.ico'

  [article]
  title = 'Article on stuff'

  [resources.markdown]
  path = 'easy-to-work-with-markdown-file.md'

  [resources.style]
  path = 'style.css\'''')


'''
Stuff to deal with missing files.
Want the program to still run even if everything in the config is not , even without
'''

ARGS = parser.parse_args()
INIT_FLAG = False

if ARGS.init == False:
  INIT_FLAG = False
elif ARGS.init == 'init' and ARGC == 2:
  INIT_FLAG = True
elif ARGS.init != 'init':
  parser.print_help()
  sys.exit()
else:
  pass

toml_files = []
markdown_files = []
css_files = []
for file in os.listdir(CWD):
  if file.endswith('.toml'):
    toml_files.append(file)
  elif file.endswith('.md'):
    markdown_files.append(file)
  elif file.endswith('.css'):
    css_files.append(file)

toml_file_count = len(toml_files)
if toml_file_count == 0: # The program gets all config from a .toml file that comes in as dict, if they don't have any exit.
    sys.exit(f'NO .toml file found\nlook at {example_toml} for an example')


markdown_file_count = len(markdown_files)
css_file_count = len(css_files)

if INIT_FLAG:
  if toml_file_count == 1:         # Check if they have a .toml in directory to use.
    CONFIG_FILE = toml_files[0]

  # Doing user input here because -f config.toml already takes a file
  # The init argument is to make it as simple to run as possible
  # You would only run it once in a while, then run "python tomltest.py -f my-config.toml", so input that blocks is okay.
  elif toml_file_count > 1:
    for i, possible_toml_file in enumerate(toml_files):
      print(i + 1, possible_toml_file)

    user_number = input('Pick a file by number:\t'); print()
    CONFIG_FILE =  toml_files[int(user_number) - 1]

elif ARGS.TOML:
  if not os.path.exists(ARGS.TOML):
    sys.exit(f'NO file found: {ARGS.TOML}')
  else:
    CONFIG_FILE = ARGS.TOML


from toml import load
BLOG = load(CONFIG_FILE)

'''
Changed doing it like dict[key1][key2], which erros if they don't exist.

This works:
    resources = BLOG.get('resources', {})
    MARKDOWN_FILE = resources.get('markdown', {}).get('path')
This doesn't:
    resources = BLOG.get('resources')
    MARKDOWN_FILE = resources.get('markdown').get('path')

You have to set the default as an empty dict that way it's not trying to run dict.get() on a None type.
'''

website = BLOG.get('website', {})
BASE_URL = website.get('url', 'google.com')
MAIN_DIR = website.get('blog', 'articlestorage')
FAVICON = website.get('favicon', 'NO-FAVICON')

resources = BLOG.get('resources', {})
MARKDOWN_FILE = resources.get('markdown', {}).get('path')
if MARKDOWN_FILE is None:
  if markdown_file_count == 0:
    print(f'NO markdown files found')
  else:
    print(f'markdown files found, none included in config: {markdown_files}\nlook at {example_toml} for an example config\n')

  sys.exit(f'**an example on the next two lines**\n[resources.markdown]\npath = \'{markdown_files[0]}\'')
elif not os.path.exists(MARKDOWN_FILE):
  sys.exit(f'not found: "{MARKDOWN_FILE}" - currently listed in {CONFIG_FILE}')


STYLESHEET = resources.get('style', {}).get('path')
if STYLESHEET is None:
  if css_file_count == 0:
    print(f'NO stylsheet found')
  else:
    print(f'stylesheet found, none included in config: {css_files}\nlook at {example_toml} for an example config\n')
  sys.exit(f'**an example on the next two lines**\n[resources.style]\npath = \'{css_files[0]}\'')

# Defaults to the markdown filename without the ".md".
TITLE = BLOG.get('article', {}).get('title', MARKDOWN_FILE[:-3])


# All this is down here because it's not necessarry for the stuff above.
# Don't want to iimport a bunch of stuff before trying to
from pprint import pprint
from markdown import markdown
from markdown.extensions.toc import TocExtension
from hashlib import md5
from time import time
from shutil import copy
from bs4 import BeautifulSoup


def markdown_blog_text():
    with open(MARKDOWN_FILE, 'r') as f:
        return f.read()


#-------------------------------------------------------------------------------------------------------------------------------------------------------
def top_doc_string():
    '''
    This is where it gets into formatting the HTML.
    A little messy right now.
    '''

    return  f'''
    <div class="site-wrap">
    <header class="site-header px2 px-responsive">
      <div class="mt2 wrap">
        <div class="measure">
          <a href="https://{BASE_URL}" class="site-title">{BASE_URL}</a>
          <nav class="site-nav">
            <a href="https://{BASE_URL}/{MAIN_DIR}">{MAIN_DIR}</a>
          </nav>
          <div class="clearfix"></div>

            </div>
        <!--
        <div style="text-align:center">
          <a href="https://github.com/fitzover">Check out my Github account</a>
        </div>
         -->
      </div>
    </header>

        <div class="post p2 p-responsive wrap" role="main">
          <div class="measure">
            <div class="post">
      <header class="post-header" style="fontsize:74em">
        <a style="font-size:1.5rem; font-weight: bold" href="https://{BASE_URL}/{MAIN_DIR}/{TITLE}/">{TITLE}</a>
      </header>
    '''


#-------------------------------------------------------------------------------------------------------------------------------------------------------
def write_new_css(css_destination):
    with open(STYLESHEET, 'r') as original, open(css_destination, 'w+') as destination:
        style_text = original.read()
        destination.write(style_text)


#-------------------------------------------------------------------------------------------------------------------------------------------------------
def creat_initial_directory(new_article_dir, stylesheet_path):
    '''
    Creates the page's directory if it does not exist:
        -> ./articles/MAIN_DIR/style.css
    Touches stylesheet if it doesn't exist:
        -> ./articles/MAIN_DIR-name/style.css
    '''
    if not os.path.exists(new_article_dir):
        os.mkdir(new_article_dir)
        print('created dir:', new_article_dir, sep='\t')
        write_new_css(stylesheet_path)
        print('created .css:', stylesheet_path, sep='\t')
    else:
        write_new_css(stylesheet_path)
        print('created .css:', stylesheet_path, sep='\t')
        copy(FAVICON, os.path.join(new_article_dir, FAVICON))


#-------------------------------------------------------------------------------------------------------------------------------------------------------
def run_html_update(markdown_string):
    print(f'config file:\t', CONFIG_FILE)

    new_article_dir = os.path.join(MAIN_DIR, TITLE)
    article_path = os.path.join(new_article_dir, 'index.html')
    stylesheet_path = os.path.join(new_article_dir, STYLESHEET)

    if INIT_FLAG or ARGS.TOML:
      if not os.path.exists(MAIN_DIR):
        os.mkdir(MAIN_DIR)
        print('created dir:', MAIN_DIR, sep='\t')

      creat_initial_directory(new_article_dir, stylesheet_path)

    favicon_fname = f'{https://}{FAVICON}' if FAVICON.startswith(BASE_URL) else FAVICON
    favicon_html_link = f'<link rel="icon" href="{favicon_fname}" type="image/svg">'

    print('writing HTML...')
    with open(article_path, 'w+') as f:
        stylesheet_head = f'<link rel="stylesheet" href="{STYLESHEET}">'
        markdown_html = markdown(markdown_string, extensions=['tables', 'fenced_code', 'toc'])
        final_html_before_beautifying = ''.join( (
                        f'<!DOCTYPE HTML>\n<html>\n<head>\n{stylesheet_head}\n{favicon_html_link}\n</head>\n<body class="site">\n{top_doc_string()}',
                        '<article class="post-content">\n<div class="post p2 p-responsive wrap" role="main">\n<div class="measure">\n<div class="post">\n',
                        f'{markdown_html}\n',
                        '</article></div></div></div></div></div></body></html>\n'
            ) )

        f.write(BeautifulSoup(final_html_before_beautifying, "html.parser").prettify())

    print(f'Finished, check for updates in "{new_article_dir}"')

    return


#-------------------------------------------------------------------------------------------------------------------------------------------------------
def current_http_pid():
  previously_active_pid = os.popen('ps aux | grep "python.*http.server.*8000" | head -n 1 | awk \'{ print $2 }\'').read()
  return previously_active_pid

def refresh_firefox():
  os.system('xdotool key --window "$(xdotool search --class firefox | tail -n 1)" F5')


#-------------------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    markdown_string = markdown_blog_text()
    run_html_update(markdown_string)
    if INIT_FLAG:
      sys.exit()

    if ARGS.LOOP:
      http_serving_dir = os.path.join(MAIN_DIR, TITLE)
      port = 8000
      previously_active_pid = current_http_pid()

      print('\nkilling previous http.server pid:', previously_active_pid )
      os.system(f'kill {previously_active_pid}') # In case I ran localhost:8000 in another process.

      print('STARTING NEW SERVER ON PORT 8000')
      os.system(f'python3 -m http.server -d {http_serving_dir} 8000 &')

      '''
      Do a checkum on the text from the markdown file to see if it has changed.
      If it has, run a the xdotool to refresh firefox.

      '''

      try:
        checksum = md5(markdown_string.encode('utf-8')).hexdigest() # Create a hash of the file, compare

        while True:
          if checksum !=  md5(markdown_blog_text().encode('utf-8')).hexdigest():
              print('Redoing...')
              markdown_string = markdown_blog_text()
              checksum = md5(markdown_string.encode('utf-8')).hexdigest()
              run_html_update(markdown_string)

              # refreshes firefox assuming it's open, will refresh the most recently clicked on window
              os.system('xdotool key --window "$(xdotool search --class firefox | tail -n 1)" F5')


      except KeyboardInterrupt: # The first keyboard interrupt kills the python http.server, so if it sees that it nees to ends
        os.system(f'kill {current_http_pid()}') # Don't leave localhost:8000 open, don't need it active.
      finally:
        sys.exit('\n')
