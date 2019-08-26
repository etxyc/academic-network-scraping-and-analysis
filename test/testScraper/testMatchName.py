import unittest
import pymongo

import sys
sys.path.append('../../')

import Scraping.unique_name.match_name as mn

class TestMatchName(unittest.TestCase):
    def test_translate_name(self):
        name = "Jôhn Smith"
        name = mn.translate_name(name)
        self.assertEqual(name, "John Smith")

    def test_find_duplicate_name(self):
        name = "J. Smith"
        match_name = "John Smith"
        self.assertTrue(mn.find_duplicate_name(name,match_name))

    def test_process1(self):
        name = "John Mith Smith"
        processed_name = mn.process(name)
        self.assertEqual(processed_name, "John Smith")

    def test_process2(self):
        name = "John M. Smith"
        processed_name = mn.process(name)
        self.assertEqual(processed_name, "John Smith")
        

    def test_get_authors(self):
        cat = "cs.IT"
        mongo_url = "mongodb://xxx:xxx@xxx:xxx/arxiv"
        authors = mn.get_authors(cat, mongo_url)
        self.assertEqual(authors["Alexey Kovalev"], 1)


        
if __name__ == '__main__':
    unittest.main()
