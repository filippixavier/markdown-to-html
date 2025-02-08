from block_markdown import (
    markdown_to_blocks,
    block_to_block_type
)
from inline_markdown import text_to_textnodes
from parentnode import ParentNode
from textnode import text_node_to_html_node

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    texts = text_to_textnodes(block[level + 1 :])
    children = list(map(lambda text: text_node_to_html_node(text), texts))
    return ParentNode(f"h{level}", children)

def code_to_node(block):
    code = block.strip("```")
    leafs = list(map(lambda text: text_node_to_html_node(text), text_to_textnodes(code)))
    return ParentNode("pre", [ParentNode("code", leafs)])

def quote_to_node(block):
    text = " ".join(map(lambda line: line.strip(">").strip(), block.splitlines()))
    full_text = list(map(lambda text: text_node_to_html_node(text), text_to_textnodes(text)))
    return ParentNode("blockquote", full_text)

def list_to_node(block, tag):
    lines = block.splitlines()
    children = []
    for line in lines:
        texts = text_to_textnodes(line.split(maxsplit=1)[1])
        leafs = list(map(lambda text: text_node_to_html_node(text), texts))
        children.append(ParentNode("li", leafs))
    return ParentNode(tag, children)

def paragraph_to_node(block):
    return ParentNode("p", list(map(lambda text: text_node_to_html_node(text), text_to_textnodes(block.replace("\n", " ")))))

def type_to_node(block):
    type = block_to_block_type(block)
    if type == "heading":
        return heading_to_html_node(block)
    elif type == "code":
        return code_to_node(block)
    elif type == "quote":
        return quote_to_node(block)
    elif type == "unordered_list":
        return list_to_node(block, "ul")
    elif type == "ordered_list":
        return list_to_node(block, "ol")
    elif type == "paragraph":
        return paragraph_to_node(block)
    else:
        raise TypeError("Invalid block type")

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        nodes.append(type_to_node(block))
    
    return ParentNode("div", nodes)

def extract_title(markdown):
    for line in markdown.splitlines():
        if line.startswith("#") and line[1] != "#":
            return line[1:]
    raise Exception("No title!")