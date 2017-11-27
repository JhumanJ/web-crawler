import unittest
import sys
sys.path.append("..") # Adds higher directory to python modules path.

from parser import Parser

class TestParser(unittest.TestCase):
    """
    Test for the Parser Class
    """

    def test_linkOnSameDomain(self):
          domain = "http://example.com"
          htmlParser = Parser(domain)
          self.assertTrue(htmlParser.linkOnSameDomain("http://example.com/test"))
          self.assertFalse(htmlParser.linkOnSameDomain("http://google.com/"))

    def test_handle_starttag(self):
          domain = "http://example.com"
          htmlToParse = "<head><script src='script.js'/><link rel='stylesheet' type='text/css' href='css/style.css'></head><body><div><a href='http://example.com/contact'></a><p>This is a test</p><div><a href='http://google.com'>external link</a></div><div></body>"
          linksToFind = set()
          linksToFind.add('/contact')
          assetsToFind = set()
          assetsToFind.add('script.js')
          assetsToFind.add('css/style.css')

          htmlParser = Parser(domain)
          htmlParser.feed(htmlToParse)
          htmlParser.close()

          self.assertEqual(htmlParser.links,linksToFind)
          self.assertEqual(htmlParser.staticAssets,assetsToFind)

if __name__ == '__main__':
    unittest.main()
