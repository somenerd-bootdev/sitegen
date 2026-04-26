import unittest

from pagebuilder import  extract_title

class TestTextNode(unittest.TestCase):
    def test_extract_title(self):
        md = "# Let's get this party started"
        extracted_title = extract_title(md)
        self.assertEqual(extracted_title, "Let's get this party started")

    def test_extract_title_longer_body(self):
        md = """# Let's get this party started

        And now some extra lines.
        Just to see what happens.
        # """
    
        extracted_title = extract_title(md)
        self.assertEqual(extracted_title, "Let's get this party started")

    def text_extract_title_missing_tag(self):
        md = "Let's not"
        self.assertRaises(ValueError, extract_title(md))


    if __name__ == "__main__":
        unittest.main()