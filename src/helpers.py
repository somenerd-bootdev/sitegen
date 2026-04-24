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
            split_node_pieces = old_node.text.split(delimiter)
            if len(split_node_pieces) == 1: # No instances of the delimiter
                new_nodes.append(old_node)
            elif len(split_node_pieces) % 2 == 0: # Only one instance of the delimiter
                raise ValueError("Invalid Markdown syntax")
            else:
                new_nodes.append(TextNode(split_node_pieces[0], TextType.TEXT))
                new_nodes.append(TextNode(split_node_pieces[1], text_type))
                new_nodes.append(TextNode(split_node_pieces[2], TextType.TEXT))

    return new_nodes