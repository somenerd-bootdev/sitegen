import unittest

from textnode import TextNode, TextType
from helpers import split_nodes_delimiter, split_nodes_image, split_nodes_link


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

   # Split segments

    def test_split_bold(self):
        node = TextNode("This is a **text** node", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

    def test_split_italic(self):
        node = TextNode("This is a _text_ node", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

    def test_split_code(self):
        node = TextNode("This is a `text` node", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text_type, TextType.CODE)
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

    def test_split_code_double(self):
        node = TextNode("This is a `text` `node`", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text_type, TextType.CODE)
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

    def test_split_code_multi_word(self):
        node = TextNode("This is a `text node`, I guess", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text_type, TextType.CODE)
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

    def test_split_one_code_delimiter(self):
        node = TextNode("This is a `text node", TextType.TEXT)
        with self.assertRaises(ValueError) as error: split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(f"{error.exception}", "Invalid Markdown syntax")

    # Split images and links

    def test_split_images(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)
        nodes = split_nodes_image([node])

        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(nodes[2].text_type, TextType.TEXT)
        self.assertEqual(nodes[3].text_type, TextType.IMAGE)

        self.assertEqual(nodes[1].text, "image")
        self.assertEqual(nodes[1].url, "https://i.imgur.com/zjjcJKZ.png")
        self.assertEqual(nodes[3].text, "second image")
        self.assertEqual(nodes[3].url, "https://i.imgur.com/3elNhQu.png")
        
    def test_split_images_only(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)
        nodes = split_nodes_image([node])

        self.assertEqual(nodes[0].text_type, TextType.IMAGE)
        self.assertEqual(nodes[1].text_type, TextType.IMAGE)

        self.assertEqual(nodes[0].text, "image")
        self.assertEqual(nodes[0].url, "https://i.imgur.com/zjjcJKZ.png")
        self.assertEqual(nodes[1].text, "second image")
        self.assertEqual(nodes[1].url, "https://i.imgur.com/3elNhQu.png")

    def test_split_links(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)
        nodes = split_nodes_link([node])

        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text_type, TextType.LINK)
        self.assertEqual(nodes[2].text_type, TextType.TEXT)
        self.assertEqual(nodes[3].text_type, TextType.LINK)

        self.assertEqual(nodes[1].text, "to boot dev")
        self.assertEqual(nodes[1].url, "https://www.boot.dev")
        self.assertEqual(nodes[3].text, "to youtube")
        self.assertEqual(nodes[3].url, "https://www.youtube.com/@bootdotdev")

    def test_split_links_only(self):
        node = TextNode("[to boot dev](https://www.boot.dev)[to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)
        nodes = split_nodes_link([node])

        self.assertEqual(nodes[0].text_type, TextType.LINK)
        self.assertEqual(nodes[1].text_type, TextType.LINK)

        self.assertEqual(nodes[0].text, "to boot dev")
        self.assertEqual(nodes[0].url, "https://www.boot.dev")
        self.assertEqual(nodes[1].text, "to youtube")
        self.assertEqual(nodes[1].url, "https://www.youtube.com/@bootdotdev")

if __name__ == "__main__":
    unittest.main()