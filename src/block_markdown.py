import os

def markdown_to_blocks(markdown):
    # Split empty line found on stackoverflow (https://stackoverflow.com/questions/38852712/python-split-on-empty-new-line)
    return list(map(lambda line: line.strip(), filter(lambda line: len(line) > 0, markdown.split(os.linesep + os.linesep))))


def is_heading(block):
    return block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### "))

def is_code(block):
    lines = block.split(os.linesep)
    return len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```")

def is_quote(block):
    lines = block.splitlines()
    for line in lines:
        if not line.startswith('>'):
            return False
    return True

def is_unordered_list(block):
    lines = block.splitlines()
    for line in lines:
        if not line.startswith(("* ", "- ")):
            return False
    return True

def is_ordered_list(block):
    lines = block.splitlines()
    index = 1
    for line in lines:
        if not line.startswith(f"{index}."):
            return False
        index += 1
    return True

def block_to_block_type(block):
    if is_heading(block):
       return "heading"
    elif is_code(block):
        return "code"
    elif is_quote(block):
        return "quote" 
    elif is_unordered_list(block):
        return "unordered_list"
    elif is_ordered_list(block):
        return "ordered_list"
    else:
        return "paragraph"