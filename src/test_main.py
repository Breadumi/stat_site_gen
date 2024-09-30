import unittest
from main import *

class TestMain(unittest.TestCase):

    def test_extract_title(self):
        m1 = "# Hello"
        self.assertEqual(extract_title(m1), "Hello")
        m2 = "Hello"
        self.assertRaises(Exception, extract_title, m2, msg="No h1 header in markdown file")
        m3 = "#       Hello         "
        self.assertEqual(extract_title(m3), "Hello")