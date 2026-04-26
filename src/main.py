from textnode import TextNode, TextType
from pagebuilder import copy_dir, generate_page, generate_pages_recursive
import os, shutil


def main():
    destination = "public"
    if os.path.exists(destination):
        shutil.rmtree(destination)
    copy_dir("static", destination)
    generate_pages_recursive("content", "template.html", "public")

main()