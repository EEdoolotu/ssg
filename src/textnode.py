from enum import Enum
import re
from htmlnode import LeafNode

class Bender(Enum):
    AIR_BENDER = "air"
    WATER_BENDER = "water"
    EARTH_BENDER = "earth"
    FIRE_BENDER = "fire"

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (self.text == other.text and 
                self.text_type == other.text_type and 
                self.url == other.url)


    def __repr__(self):
        return f"TextNode({self.text!r}, {self.text_type!r}, {self.url!r})"

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue


        parts = old_node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid markdown: unmatched delimiter {delimiter}")

        for i, part in enumerate(parts):
            if part =="":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes

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
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Invalid text type: {text_node.text_type}")

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches
        



def split_nodes_image(old_nodes):
    new_nodes = []
    
    for old_node in old_nodes:
        # If it's not a text node, keep it as-is
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        # Extract all images from this node
        images = extract_markdown_images(old_node.text)
        
        # If no images, keep the node as-is
        if not images:
            new_nodes.append(old_node)
            continue
        
        # Split the text by images
        remaining_text = old_node.text
        for alt_text, url in images:
            # Split on the image syntax
            parts = remaining_text.split(f"![{alt_text}]({url})", 1)
            
            # Add text before the image (if any)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            
            # Add the image node
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            
            # Continue with remaining text
            remaining_text = parts[1] if len(parts) > 1 else ""
        
        # Add any remaining text after the last image
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    
    for old_node in old_nodes:
        # If it's not a text node, keep it as-is
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        # Extract all links from this node
        links = extract_markdown_links(old_node.text)
        
        # If no links, keep the node as-is
        if not links:
            new_nodes.append(old_node)
            continue
        
        # Split the text by links
        remaining_text = old_node.text
        for anchor_text, url in links:
            # Split on the link syntax
            parts = remaining_text.split(f"[{anchor_text}]({url})", 1)
            
            # Add text before the link (if any)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            
            # Add the link node
            new_nodes.append(TextNode(anchor_text, TextType.LINK, url))
            
            # Continue with remaining text
            remaining_text = parts[1] if len(parts) > 1 else ""
        
        # Add any remaining text after the last link
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    
    return new_nodes

def text_to_textnodes(text):
    # Start with a single text node containing all the text
    nodes = [TextNode(text, TextType.TEXT)]
    
    # Split by bold (**text**)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    
    # Split by italic (*text*)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    
    # Split by code (`text`)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    
    # Split by images
    nodes = split_nodes_image(nodes)
    
    # Split by links
    nodes = split_nodes_link(nodes)
    
    return nodes