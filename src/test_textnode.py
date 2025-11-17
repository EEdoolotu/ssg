import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_different_text(self):
        node = TextNode("Hello", TextType.TEXT)
        node2 = TextNode("World", TextType.TEXT)
        self.assertNotEqual(node, node2)
    
    def test_eq_url_none(self):
        node = TextNode("No URL", TextType.TEXT, None)
        node2 = TextNode("No URL", TextType.TEXT, None)
        self.assertEqual(node, node2)


if __name__ == "__main__":
    unittest.main()