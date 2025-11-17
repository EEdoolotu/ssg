import unittest
from htmlnode import LeafNode
from textnode import TextNode,split_nodes_delimiter, TextType, text_node_to_html_node, text_to_textnodes, split_nodes_image, split_nodes_link, extract_markdown_images, extract_markdown_links


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
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("This is ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("bold", TextType.BOLD))
        self.assertEqual(new_nodes[2], TextNode(" text", TextType.TEXT))

    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is `code` here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("This is ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("code", TextType.CODE))
        self.assertEqual(new_nodes[2], TextNode(" here", TextType.TEXT))

    def test_split_nodes_delimiter_multiple(self):
        node = TextNode("**bold** and **more bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("bold", TextType.BOLD))
        self.assertEqual(new_nodes[1], TextNode(" and ", TextType.TEXT))
        self.assertEqual(new_nodes[2], TextNode("more bold", TextType.BOLD))

    def test_split_nodes_delimiter_non_text_node(self):
        node = TextNode("Already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], node)

    def test_split_nodes_delimiter_invalid(self):
        node = TextNode("Unmatched **delimiter", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)


    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertListEqual([
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ], matches)

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ], matches)

    def test_extract_markdown_links_single(self):
        matches = extract_markdown_links("Check out [this link](https://example.com)")
        self.assertListEqual([("this link", "https://example.com")], matches)

    def test_extract_no_images(self):
        matches = extract_markdown_images("Just plain text here")
        self.assertListEqual([], matches)

    def test_extract_no_links(self):
        matches = extract_markdown_links("Just plain text here")
        self.assertListEqual([], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_all_types(self):
        text = "This is **bold** and *italic* and `code` and ![img](https://example.com/img.png) and [link](https://example.com)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "https://example.com/img.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
        ]
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_plain_text(self):
        text = "Just plain text here"
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, [TextNode("Just plain text here", TextType.TEXT)])

    def test_text_to_textnodes_bold_only(self):
        text = "This is **bold text** here"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_multiple_same_type(self):
        text = "**bold1** and **bold2**"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("bold1", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold2", TextType.BOLD),
        ]
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_nested_not_supported(self):
        # Note: This shows the limitation - nested markdown isn't handled
        text = "**bold and *italic* together**"
        nodes = text_to_textnodes(text)
        # This will split on bold first, then italic won't be inside bold text
        # Just documenting expected behavior
        self.assertIsInstance(nodes, list)


if __name__ == "__main__":
    unittest.main()