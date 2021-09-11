import toml
from pprint import pprint
import os, sys
import markdown
from markdown.extensions.toc import TocExtension
import argparse
from shutil import copyfile
from pathlib import Path

ARGC = len(sys.argv)


parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description='Make things difficult for yourself with a custom SSG! OS: Linux | Python Version: 3.8'
)
parser.add_argument('-i, --init', dest='INIT', default=False, action='store_true', help="initialize article directory")
parser.add_argument('-f', '--toml', dest='TOML', default=False, help="initialize article directory")
parser.add_argument('-t', '--test', dest='TEST', default=False, help="a test argument")

if ARGC == 1:
    parser.print_help()
    sys.exit('\n**Please read the options above!**')


ARGS = parser.parse_args()


toml_files = [file for file in os.listdir(os.getcwd()) if file.endswith('.toml')]
config_file = toml_files[0] if len(toml_files) == 1  else ARGS.TOML
blog = toml.load(config_file)

if ARGS.TEST:
    print(ARGS)
    print()


def markdown_blog_text(markdown_file):
    with open(markdown_file, 'r') as f:
        markdown_text = f.read()
    return markdown_text


def creat_initial_directory(article_dir, new_article_dir, stylesheet_path):
    '''
    Creates directories if they do not exist:
        -> articles/
        -> ./articles/article-name/style.css
    Touches file if it doesn't exist:
        -> ./articles/article-name/style.css

    '''

    if not os.path.exists(new_article_dir):
        os.mkdir(new_article_dir)
        print('created dir:', new_article_dir, sep='\t')
    else:
      return 

    if blog['resources']['style']['path'] in os.listdir(new_article_dir):
      print(f'**run with "init" after making sure the directory below is empty**\n->\t"{new_article_dir}""')
      print(*[os.path.join(new_article_dir, file) for file in os.listdir(new_article_dir)], sep='\n')
    else:
      Path(stylesheet_path).touch()
      print('created empty .css file:', stylesheet_path, sep='\t')

    


if __name__ == '__main__':


    website = blog['website']['url']
    article_dir = blog['website']['blog']
    title = blog['article']['title']

    markdown_file = blog['resources']['markdown']['path']
    stylesheet = blog['resources']['style']['path']


    new_article_dir = os.path.join(article_dir, title)
    article_path = os.path.join(new_article_dir, 'index.html')
    stylesheet_path = os.path.join(new_article_dir, stylesheet)

    if ARGS.INIT:
      if not os.path.exists(article_dir):
        os.mkdir(article_dir)
        print('created dir:', article_dir, sep='\t')

      creat_initial_directory(article_dir, new_article_dir, stylesheet_path)
    
    copyfile(stylesheet, stylesheet_path)


    #os.system(f'bat -p {config_file}')

    '''
    This is where it gets into formatting the HTML.
    A little messy right now.
    '''

    stylesheet_head = f'<link rel="stylesheet" href="{stylesheet}">'

    header_doc_str = f'''<div class="site-wrap">
  <header class="site-header px2 px-responsive">
  <div class="mt2 wrap">
    <div class="measure">
      <a href="https://{website}" class="site-title">{website}</a>
      <nav class="site-nav">
        <a href="https://{website}/{article_dir}">{article_dir}</a>
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
    <a style="font-size:1.5rem; font-weight: bold" href="https://{website}/{article_dir}/{title}/index.html">{title}</a>
  </header>'''

    with open(article_path, 'w+') as f:
        f.write(f'<!DOCTYPE HTML>\n<html>\n<head>\n{stylesheet_head}\n</head>\n<body class="site">\n{header_doc_str}')
        f.write('<article class="post-content">\n<div class="post p2 p-responsive wrap" role="main">\n<div class="measure">\n<div class="post">\n')
        markdown_html = markdown.markdown(markdown_blog_text(markdown_file), extensions=['tables', 'fenced_code', 'toc'])
        f.write(markdown_html + '\n')
        f.write('</article></div></div></div></div></div></body></html>')
