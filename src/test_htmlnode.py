import unittest
from htmlnode import *


class TestHTMLNode(unittest.TestCase):

    def test_default(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_props(self):
        expected = ' href="https://www.google.com" target="_blank"'
        node = HTMLNode(props = {"href": "https://www.google.com", "target": "_blank"})
        actual = node.props_to_html()
        self.assertEqual(actual,expected)

    def test_full(self):
        node = HTMLNode("p", "how's it going", [HTMLNode(), HTMLNode()], {"blah": "bleh"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "how's it going")
        self.assertEqual(str(node.children),str([HTMLNode(), HTMLNode()]))
        self.assertEqual(node.props, {"blah": "bleh"})

    def test_leaf(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
        node2 = LeafNode("a", "Click me!")
        self.assertEqual(node2.to_html(), "<a>Click me!</a>")

    def test_single_parent(self):
        node = ParentNode(
                            "p",
                            [
                                LeafNode("b", "Bold text"),
                                LeafNode(None, "Normal text"),
                                LeafNode("i", "italic text"),
                                LeafNode(None, "Normal text"),
                            ],
                        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

if __name__ == "__main__":
    unittest.main()