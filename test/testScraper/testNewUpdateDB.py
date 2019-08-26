import unittest
import pymongo

import sys
sys.path.append('../../')

from Scraping.arxiv.NewUpdateDB import *

class TestNewUpdateDB(unittest.TestCase):
    def testUpdateDB(self):
        flag = True
        mongo_url = "mongodb://xxx:xxx@xxx:xxx/arxiv"
        client = pymongo.MongoClient(mongo_url)
        db = client['arxiv']
        collection = db['test']
        collection.drop()

        # update the database
        update_time = "2018-05-12"
        category = 'stat.ML'
        search_query = "cat:{0}".format(category)
        UpdateDB(collection, search_query, update_time)

        result = collection.find()
        for record in result:
            if category not in record['category']:
                flag = False
                break
            if record['updated'] < update_time:
                flag = False
                break
        collection.drop()
        self.assertTrue(flag)

if __name__ == '__main__':
        unittest.main()
