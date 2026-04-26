import re
from htmlnode import LeafNode, ParentNode
from textnode import TextNode, TextType
from blocktypes import BlockType, block_to_block_type, markdown_to_blocks

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

# Markdown to HTML

def text_to_children(text:str) -> list[LeafNode]:
    result = []
    textnodes = text_to_textnodes(text)
    for textnode in textnodes:
        result.append(text_node_to_html_node(textnode))
    return result

def markdown_to_html_node(markdown: str):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            children.append(paragraph_to_html_node(block))
        elif block_type == BlockType.HEADING:
            children.append(heading_to_html_node(block))
        elif block_type == BlockType.CODE:
            children.append(code_to_html_node(block))
        elif block_type == BlockType.QUOTE:
            children.append(quote_to_html_node(block))
        elif block_type == BlockType.UNORDERED_LIST:
            children.append(ulist_to_html_node(block))
        elif block_type == BlockType.ORDERED_LIST:
            children.append(olist_to_html_node(block))
        else:
            raise ValueError(f"Unknown block type: {block_type}")

    return ParentNode("div", children)

def paragraph_to_html_node(block:str):
    children = text_to_children(block.replace("\n", " "))
    return ParentNode("p", children)

def heading_to_html_node(block:str):
    heading_intensity = len(block) - len(block.lstrip("#"))
    if heading_intensity > 6 or heading_intensity == 0:
        raise ValueError("Incorrect heading level")
    clean_block = block[heading_intensity + 1:]
    if len(clean_block) < 1:
        raise ValueError("Heading specified but no text to apply it to")
    heading_tag = f"h{heading_intensity}"
    children = text_to_children(clean_block)
    return ParentNode(heading_tag, children)

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    cleanblock = block[4:-3]
    leafnode = text_node_to_html_node(TextNode(cleanblock, TextType.TEXT))
    codenode = ParentNode("code", [leafnode])
    return ParentNode("pre", [codenode])

def quote_to_html_node(block):
    lines = block.split("\n")
    clean_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Quote block line was missing markdown")
        clean_line = line.lstrip(">").strip()
        clean_lines.append(clean_line)

    combined_quote = " ".join(clean_lines)
    children = text_to_children(combined_quote)
    return ParentNode("blockquote", children)
    

def ulist_to_html_node(block):
    lines = block.split("\n")
    children = []
    for line in lines:
        clean_line = line[2:]
        inner_children = text_to_children(clean_line)
        children.append(ParentNode("li", inner_children))
    return ParentNode("ul", children)

def olist_to_html_node(block):
    lines = block.split("\n")
    children = []
    for line in lines:
        clean_line = line.split(". ", 1)[1]
        inner_children = text_to_children(clean_line)
        children.append(ParentNode("li", inner_children))
    return ParentNode("ol", children)