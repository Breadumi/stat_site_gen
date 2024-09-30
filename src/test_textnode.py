import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("This is a text node", "bold", "https://blahblah.org")
        node2 = TextNode("This is a text node", "bold", "https://blahblah.org")
        self.assertEqual(node, node2)

    def test_neq_texttype(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bol")
        self.assertNotEqual(node, node2)

    def test_neq_text(self):
        node = TextNode("This is a xt node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)

    def test_neq_1_none_url(self):
        node = TextNode("This is a text node", "bold", "https://blahblah.org")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()