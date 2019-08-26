import unittest
import pymongo

import sys
sys.path.append('../../')
# from src.function import BasicFunction

import Scraping.arxiv.NewScraper as sp


class TestBasicFunction(unittest.TestCase):
    # def setUp(self):
        # self.func = BasicFunction()

    def testOpenRequest(self):
        bsdata = sp.openRequest(0, 500, "cat:stat.ML")
        category_list = bsdata.entry.find_all('category')

        trueFlag = False
        for child in category_list:
            if child['term'] == 'stat.ML':
                trueFlag = True
                break
        self.assertTrue(trueFlag)

    def testOpenMongoDB(self):
        trueFlag = True
        try:
            arxiv = sp.openMongoDB("mongodb://xxx:xxx@xxx:xxx/arxiv")
        except Exception:
            trueFlag = False
        self.assertTrue(trueFlag)


    def testScrapeArxiv(self):
        sp.scrapeArxiv(0, 500, "Gautam Kamath", "mongodb://xxx:xxx@xxx:xxx/arxiv", 3)
        db = sp.openMongoDB("mongodb://xxx:xxx@xxx:xxx/arxiv")
        post = db.papers.find_one({'title': 'Actively Avoiding Nonsense in Generative Models'})
        self.assertEqual('http://arxiv.org/abs/1802.07229v1', post['_id'])


if __name__ == '__main__':
    unittest.main()

    
