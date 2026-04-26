from textnode import TextNode, TextType
from pagebuilder import copy_dir, generate_page, generate_pages_recursive
import os, shutil, sys


def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    destination = "docs"
    if os.path.exists(destination):
        shutil.rmtree(destination)
    copy_dir("static", destination)
    generate_pages_recursive("content", "template.html", destination, basepath)

main()