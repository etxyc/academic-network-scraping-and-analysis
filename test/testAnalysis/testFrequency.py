import unittest

import sys
sys.path.append('../../Analysis')

import frequency as fre

class TestFrequency(unittest.TestCase):
  def testscrapeLocal(self):

    try:
        mongo_url =  "mongodb://xxx:xxx@xxx:xxx/arxiv"
        category = "cs.AI"
        fre.writeFrequency(mongo_url, 2000, category)

    except Exception as e:
        trueFlag = False
        self.assertTrue(trueFlag)

if __name__ == '__main__':
    unittest.main()
