import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_none(self):
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(None, node2)
    
    def test_eq_none2(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, None)

    def test_eq_diff_text(self):
        node = TextNode("This is totally not a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_diff_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()