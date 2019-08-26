import unittest
import pymongo

import sys
sys.path.append('../../')
# from src.function import BasicFunction


import Scraping.arxiv.NewScraper as sp

class TestBasicFunction(unittest.TestCase):
    # def setUp(self):
        # self.func = BasicFunction()


    def test_username_password(self):
        trueFlag = True
        try:
            mongo_url = "mongod://xxx:xxx@xxx:xxx/arxiv"  #example usage of wrong password
            client = MongoClient(mongo_url)
        except:
            trueFlag = False

        self.assertTrue(not trueFlag)


    def test_waiting_time_constrain(self):
        try:
            sp.scrapeArxiv(0, 500, "cat:stat.ML", "mongodb://xxx:xxx@xxx:xxx/arxiv", 0.1)
        except Exception as e:
            self.assertEqual(str(e), "waiting time should be larger than 3 sec")

    def test_max_paper_per_search_constrain(self):
        try:
            sp.scrapeArxiv(0, 5000, "cat:stat.ML", "mongodb://xxx:xxx@xxx:xxx/arxiv", 4)
        except Exception as e:
            self.assertEqual(str(e), "max paper per search is too large")






if __name__ == '__main__':
    unittest.main()
