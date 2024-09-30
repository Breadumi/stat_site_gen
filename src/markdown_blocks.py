import re
from htmlnode import *
from textnode import *
from inline_markdown import *

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_olist = "ordered_list"
block_type_ulist = "unordered_list"

def markdown_to_blocks(document):
    if document == "":
        return [document]
    
    lines = document.split("\n")

    if len(lines) == 1:
        return [document.strip()]
    
    block = ""
    blocks = []
    i = 0
    while i < len(lines):

        if not lines[i].isspace() and lines[i] != "":
            block = "\n".join([block, lines[i]])

        
        if lines[i].isspace() or lines[i] == "":
            if block != "":
                blocks.append(block.strip())
            block = ""

        i += 1
    
    if block != "":
        blocks.append(block)

    return blocks

def block_to_block_type(block):
    regex_heading = "^(#{1,6} ).*?" # use match
    regex_code = "^(`{3})(.|\n)*(`{3})$" # use match
    regex_quote = "(?m)(^\> .*\n*$)"  # use fullmatch
    regex_unordered_list = "(?m)(^[\*-] .*\n*$)" # use fullmatch
    regex_ordered_list = "(?m)(^\d+\. .*\n*$)" # use fullmatch, also findall to check ordering

    if re.match(regex_heading, block) is not None:
        return block_type_heading
    if re.match(regex_code, block) is not None:
        return block_type_code
    if re.match(regex_quote, block) is not None:
        return block_type_quote
    if re.match(regex_unordered_list, block) is not None:
        return block_type_ulist
    if re.match(regex_ordered_list, block) is not None:
        matches = re.findall("(?m)(^\d+)", block)
        if all(matches[i] < matches[i+1] for i in range(len(matches)-1)):
            return block_type_olist

    return block_type_paragraph

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:

        block_type = block_to_block_type(block)

        if block_type == block_type_paragraph:
            children.append(paragraph_to_html_node(block))
        elif block_type == block_type_heading:
            children.append(heading_to_html_node(block))
        elif block_type == block_type_code:
            children.append(code_to_html_node(block))
        elif block_type == block_type_quote:
            children.append(quote_to_html_node(block))
        elif block_type == block_type_ulist:
            children.append(ulist_to_html_node(block))
        elif block_type == block_type_olist:
            children.append(olist_to_html_node(block))        
        else:
            print("Error found for:", block_type)
            raise ValueError("Invalid block type")

    return ParentNode("div", children)

def paragraph_to_html_node(block):
    block = " ".join(block.split("\n"))
    nodes = text_to_textnodes(block)
    nodes = [text_node_to_html_node(node) for node in nodes]
    return ParentNode("p", nodes)

def heading_to_html_node(block):
    temp = block.split(" ", maxsplit=1)
    nodes = text_to_textnodes(temp[1])
    nodes = [text_node_to_html_node(node) for node in nodes]
    heading_number = len(temp[0])
    return ParentNode(f"h{heading_number}", nodes)
    

def code_to_html_node(block):
    temp = block.split("```", maxsplit=1)[1].rsplit("```", maxsplit=1)[0]
    nodes = text_to_textnodes(temp)
    nodes = [text_node_to_html_node(node) for node in nodes]
    return ParentNode("code", nodes)

def quote_to_html_node(block):
    temp = block.split("\n")
    block = " ".join([x[2:] for x in temp])
    nodes = text_to_textnodes(block)
    html_nodes = []
    for node in nodes:
        html_nodes.append(text_node_to_html_node(node))
    return ParentNode("blockquote", html_nodes)

def ulist_to_html_node(block):
    temp = block.split("\n")
    block = [x[2:] for x in temp]
    ulist_children = []
    for line in block:
        nodes = text_to_textnodes(line)
        nodes = [text_node_to_html_node(node) for node in nodes]
        ulist_children.append(ParentNode("li", nodes))
    return ParentNode("ul", ulist_children)

def olist_to_html_node(block):
    temp = block.split("\n")
    block = [x[3:] for x in temp]
    olist_children = []
    for line in block:
        nodes = text_to_textnodes(line)
        nodes = [text_node_to_html_node(node) for node in nodes]
        olist_children.append(ParentNode("li", nodes))
    return ParentNode("ol", olist_children)

        
