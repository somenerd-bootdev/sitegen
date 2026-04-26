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

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

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

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT: # Don't process it if it's already a specific non-text type
            new_nodes.append(old_node)
        else: # Time to split
            original_text = old_node.text
            remaining_text = original_text
            extracted_images = extract_markdown_images(original_text)
            split_nodes = []
            for i in range(len(extracted_images)):
                image_alt = extracted_images[i][0]
                image_link = extracted_images[i][1]
                split_strings = remaining_text.split(f"![{image_alt}]({image_link})", 1)
                if (split_strings[0] == ""):
                    split_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
                else:
                    split_nodes.append(TextNode(split_strings[0], TextType.TEXT))
                    split_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
                remaining_text = split_strings[1]
            if remaining_text != "":
                split_nodes.append(TextNode(remaining_text, TextType.TEXT))
            new_nodes.extend(split_nodes)

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT: # Don't process it if it's already a specific non-text type
            new_nodes.append(old_node)
        else: # Time to split
            original_text = old_node.text
            remaining_text = original_text
            extracted_links = extract_markdown_links(original_text)
            split_nodes = []
            for i in range(len(extracted_links)):
                link_text = extracted_links[i][0]
                link_url = extracted_links[i][1]
                split_strings = remaining_text.split(f"[{link_text}]({link_url})", 1)
                if (split_strings[0] == ""):
                    split_nodes.append(TextNode(link_text, TextType.LINK, link_url))
                else:
                    split_nodes.append(TextNode(split_strings[0], TextType.TEXT))
                    split_nodes.append(TextNode(link_text, TextType.LINK, link_url))
                if (len(split_strings) > 1):
                    remaining_text = split_strings[1]
            if remaining_text != "":
                split_nodes.append(TextNode(remaining_text, TextType.TEXT))
            new_nodes.extend(split_nodes)

    return new_nodes

def text_to_textnodes(text):
    initial_node = TextNode(text, TextType.TEXT)
    nodes = []
    nodes.append(initial_node)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes
