import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("a", "link", None, {"href": "https://example.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com" target="_blank"')

    def test_props_to_html_single_prop(self):
        node = HTMLNode("p", "text", None, {"class": "paragraph"})
        self.assertEqual(node.props_to_html(), ' class="paragraph"')
    
    def test_props_to_html_none(self):
        node = HTMLNode("div", "content", None, None)
        self.assertEqual(node.props_to_html(), "")