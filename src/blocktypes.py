from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    result = []
    for block in blocks:
        stripped_block = block.strip()
        if stripped_block != "":
            result.append(stripped_block)

    return result

def block_to_block_type(block):
    if re.match(r"#{1,6} .+", block):
        return BlockType.HEADING
    if re.match(r"`{3}\n[\w\d\s]*`{3}", block):
        return BlockType.CODE
    if re.match(r"> ?.+", block):
        lines = block.split("\n")
        match = False
        for line in lines:
            match |= re.match(r"> ?.+", line) != None
        if match:
            return BlockType.QUOTE
    if re.match(r"(- .+)+", block):
        lines = block.split("\n")
        match = False
        for line in lines:
            match |= re.match(r"- ", line) != None
        if match:
            return BlockType.UNORDERED_LIST
    if re.match(r"\d+. ", block):
        lines = block.split("\n")
        increment = 1
        match = False
        for line in lines:
            match |= re.match(fr"{increment}\. ", line) != None
            increment += 1
        if match:
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH