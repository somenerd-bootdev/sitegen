import re
from htmlnode import LeafNode
from textnode import TextNode, TextType

def text_node_to_html_node(text_node): 
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href" : text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src" : text_node.url, "alt": text_node.text})
        case _:
            raise ValueError("Node type was not in the allowed set")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT: # Don't process it if it's already a specific non-text type
            new_nodes.append(old_node)
        else: # Time to split
            split_strings = old_node.text.split(delimiter)
            split_nodes = []
            if len(split_strings) % 2 == 0: # Mismatched number of delimiters
                raise ValueError("Invalid Markdown syntax")
            for i in range(len(split_strings)):
                if split_strings[i] == "":
                    continue # Nothing to parse
                if i % 2 == 0:
                    split_nodes.append(TextNode(split_strings[i], TextType.TEXT))
                else:
                    split_nodes.append(TextNode(split_strings[i], text_type))
            new_nodes.extend(split_nodes)

    return new_nodes

def extract_markdown_images(text):
    hits = re.findall(r"!\[.*?\]\(.*?\)", text)
    results = []
    for hit in hits:
        hit = re.sub("!", "", hit)
        front = re.sub(r"\(.*?\)", "", hit)
        back = re.sub(r"\[.*?\]", "", hit)
        results.append((f"{front[1:len(front)-1]}", f"{back[1:len(back)-1]}"))
    return results

def extract_markdown_links(text):
    hits = re.findall(r"\[.*?\]\(.*?\)", text)
    results = []
    for hit in hits:
        front = re.sub(r"\(.*?\)", "", hit)
        back = re.sub(r"\[.*?\]", "", hit)
        results.append((f"{front[1:len(front)-1]}", f"{back[1:len(back)-1]}"))
    return results