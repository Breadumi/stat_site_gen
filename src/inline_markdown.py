from textnode import *
from htmlnode import *
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    
    new_node_list = []

    for node in old_nodes:

        new_node_text = node.text.split(delimiter)

        if node.text_type != text_type_text:
            new_node_list.append(node)
            continue
        
        if len(new_node_text) % 2 == 0:
            raise Exception(f"missing delimiter pair for {delimiter}: {old_nodes.text}")
        
        for k in range(len(new_node_text)):
            if new_node_text[k] == "":
                continue
            if k % 2 != 0:
                new_node_list.append(
                    TextNode(new_node_text[k], text_type)
                )
            else:
                new_node_list.append(
                    TextNode(new_node_text[k], text_type_text)
                )
        
    return new_node_list
        
def extract_markdown_images(text):
    #( ) are the capture groups
    #\[ \] \( \) are escaped and are literal matches
    # each full string can have multiple capture groups, these groups
    # are grouped in one tuple per matched string
    # each string tuple in a single line of text are stored in a list
    # .*? means match any character, 
    #           zero or more times, 
    #           as few times as possible
    return re.findall(r"!\[(.*?)\]\((.*?)\)" ,text)

def extract_markdown_links(text):
    # (?<!.) will look behind a matched string and check it is NOT preceded
    # by any string in the place of the .
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)" ,text)

def split_nodes_image(old_nodes):
    
    new_node_list = []
    
    for node in old_nodes:
        text = node.text
        images = extract_markdown_images(text)
        
        if images is None or len(images) == 0:
            new_node_list.append(node)
            continue # there are no images found, skip this node
        
        for image in images:
            
            image_string = f"![{image[0]}]({image[1]})"
            
            cur_split = text.split(image_string)

            if cur_split[0] == "" and cur_split[1] == "":
                new_node_list.append(
                    TextNode(image[0], text_type_image, image[1])
                    )
                
                return new_node_list

            new_node_list.extend(
                [TextNode(cur_split[0], text_type_text),
                 TextNode(image[0], text_type_image, image[1])]
            )
            text = cur_split[1]
        
        # append last piece of text
        if text != "":
            new_node_list.append(
                TextNode(text, text_type_text)
            )        

    return new_node_list


def split_nodes_link(old_nodes):
    
    new_node_list = []

    for node in old_nodes:
        text = node.text
        links = extract_markdown_links(text)

        if links is None or len(links) == 0:
            new_node_list.append(node)
            continue # there are no images found, skip this node
        
        for link in links:
            link_string = f"[{link[0]}]({link[1]})"

            cur_split = text.split(link_string)

            if cur_split[0] == "" and cur_split[1] == "":
                new_node_list.append(
                    TextNode(link[0], text_type_image, link[1])
                    )
                
                return new_node_list

            new_node_list.extend(
                [TextNode(cur_split[0], text_type_text),
                 TextNode(link[0], text_type_link, link[1])]
            )
            text = cur_split[1]
        
        # append last piece of text
        if cur_split[1] != "":
            new_node_list.append(
                TextNode(text, text_type_text)
            )  
    
    return new_node_list

def text_to_textnodes(text): # bold, italic, code, images, links in that order
    first_node = TextNode(text, text_type_text)

    new_nodes = split_nodes_delimiter([first_node], "**", text_type_bold)
    new_nodes = split_nodes_delimiter(new_nodes, "*", text_type_italic)
    new_nodes = split_nodes_delimiter(new_nodes, "`", text_type_code)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
        
    return new_nodes