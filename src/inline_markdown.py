import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            sections  = node.text.split(delimiter)
            if len(sections) % 2 == 0:
                raise ValueError("Invalid markdown, formatted section not closed")
            split_nodes = []
            for i in range(len(sections)):
                if sections[i] == "":
                    continue
                if i % 2 == 0:
                    split_nodes.append(TextNode(sections[i], TextType.TEXT))
                else:
                    split_nodes.append(TextNode(sections[i], text_type))
            new_nodes.extend(split_nodes)
        else:
            new_nodes.append(node)
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

# regex images du cours
# r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
# Celle que j'ai faite originellement:
# r"!\[(.*?)\]\((.*?)\)" => plus concise, mais avec des cas d'erreurs

# regex regular links du cours
# r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
# La mienne:
# r"[^!]\[(.*?)\]\((.*?)\)" => En plus de l'erreur des doubles crochets/parenthèses, je n'accrocherai pas les liens en début de ligne

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        child_nodes = []
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        text = node.text
        for (alt, url) in images:
            parts = text.split(f"![{alt}]({url})", maxsplit = 1)
            if len(parts) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if parts[0] != "":
                child_nodes.append(TextNode(parts[0], TextType.TEXT))
            child_nodes.append(TextNode(alt, TextType.IMAGE, url))
            text = parts[1]
        if text != "":
            child_nodes.append(TextNode(text, TextType.TEXT))
        new_nodes.extend(child_nodes)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        child_nodes = []
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        text = node.text
        for (alt, url) in links:
            parts = text.split(f"[{alt}]({url})", maxsplit = 1)
            if len(parts) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if parts[0] != "":
                child_nodes.append(TextNode(parts[0], TextType.TEXT))
            child_nodes.append(TextNode(alt, TextType.LINK, url))
            text = parts[1]
        if text != "":
            child_nodes.append(TextNode(text, TextType.TEXT))
        new_nodes.extend(child_nodes)
    return new_nodes

def text_to_textnodes(text):
    node = TextNode(text, 'text')
    nodes = split_nodes_link([node])
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    return split_nodes_delimiter(nodes, "`", TextType.CODE)