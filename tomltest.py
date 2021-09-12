import toml
from pprint import pprint
import os, sys
from markdown import markdown
from markdown.extensions.toc import TocExtension
import argparse
from hashlib import md5


ARGC = len(sys.argv)

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description='A static site generator'
)
#parser.add_argument('init', dest='INIT', default=False, action='store_true', help="initialize article directory")
parser.add_argument('init', default=False, nargs='?', help="initialize article directory")
parser.add_argument('-f', '--toml', dest='TOML', default=False, help="initialize article directory")

if ARGC == 1:
    parser.print_help()
    sys.exit('\n**Please read the options above!**')


ARGS = parser.parse_args()

if ARGS.init == 'init':
    INIT_FLAG = True
else:
    INIT_FLAG = False

toml_files = [file for file in os.listdir(os.getcwd()) if file.endswith('.toml')]
config_file = toml_files[0] if len(toml_files) == 1  else ARGS.TOML

if INIT_FLAG and len(toml_files) > 1:
    config_file =  input('Enter which .toml file to init:\t')
    print()

BLOG = toml.load(config_file)

BASE_URL = BLOG['website']['url']
MAIN_DIR = BLOG['website']['blog']
FAVICON = BLOG['website']['favicon']
TITLE = BLOG['article']['title']

MARKDOWN_FILE = BLOG['resources']['markdown']['path']
STYLESHEET = BLOG['resources']['style']['path']

def markdown_blog_text():
    with open(MARKDOWN_FILE, 'r') as f:
        markdown_text = f.read()
    return markdown_text

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

def write_new_css(css_destination):
    with open(css_destination, 'w+') as destination:
        destination.write('')
    with open(STYLESHEET, 'r') as original, open(css_destination, 'a') as destination:
        style_text = original.read()
        destination.write(style_text)


def creat_initial_directory(new_article_dir, stylesheet_path):
    '''
    Creates the page's directory if it does not exist:
        -> ./articles/article-name/style.css
    Touches stylesheet if it doesn't exist:
        -> ./articles/article-name/style.css
    '''

    if not os.path.exists(new_article_dir):
        os.mkdir(new_article_dir)
        print('created dir:', new_article_dir, sep='\t')
        write_new_css(stylesheet_path)
        print('.css:', stylesheet_path, sep='\t')
        return
    else:
      print(f'"{new_article_dir}" already exists\n')
      return

def run_html_update(markdown_string):
    new_article_dir = os.path.join(MAIN_DIR, TITLE)
    article_path = os.path.join(new_article_dir, 'index.html')
    stylesheet_path = os.path.join(new_article_dir, STYLESHEET)

    if INIT_FLAG:
      if not os.path.exists(MAIN_DIR):
        os.mkdir(MAIN_DIR)
        print('created dir:', MAIN_DIR, sep='\t')

      creat_initial_directory(new_article_dir, stylesheet_path)

    print(f'copying {STYLESHEET}')

    stylesheet_head = f'<link rel="stylesheet" href="{STYLESHEET}">'
    markdown_html = markdown(markdown_string, extensions=['tables', 'fenced_code', 'toc'])

    favicon_fname = FAVICON.replace('https://', '')
    favicon_html_link = f'<link rel="icon" href="https://{favicon_fname}" type="image/svg">'

    print('writing HTML...')

    with open(article_path, 'w+') as f:
        f.write(f'<!DOCTYPE HTML>\n<html>\n<head>\n{stylesheet_head}\n{favicon_html_link}\n</head>\n<body class="site">\n{top_doc_string()}')
        f.write('<article class="post-content">\n<div class="post p2 p-responsive wrap" role="main">\n<div class="measure">\n<div class="post">\n')
        f.write(f'{markdown_html}\n')
        f.write('</article></div></div></div></div></div></body></html>\n')

    print(f'\nFinished, check for updates in "{new_article_dir}"')

if __name__ == '__main__':
    markdown_string = markdown_blog_text()
    checksum = md5(markdown_string.encode('utf-8')).hexdigest()
    run_html_update(markdown_string)
    if INIT_FLAG:
      sys.exit()

    while True:
        if checksum != md5(markdown_blog_text().encode('utf-8')).hexdigest():
            new_markdown_text = markdown_blog_text()
            checksum = md5(new_markdown_text.encode('utf-8')).hexdigest()
            run_html_update(new_markdown_text)
            os.system('xdotool key --window "$(xdotool search --class firefox | tail -n 1)" F5')
