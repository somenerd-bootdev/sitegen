from textnode import TextNode, TextType
from pagebuilder import copy_dir
import os, shutil


def main():
    text_node = TextNode("Here's some text", TextType.BOLD)
    print(text_node)
    destination = "public"
    if os.path.exists(destination):
        shutil.rmtree(destination)
    copy_dir("static", destination)

main()