import unittest
import pymongo

import sys
sys.path.append('../../Analysis')

from DBConstruct import *

class testDBConstruct(unittest.TestCase):
    def testDatabaseStore(self):
        flag = True
        mongo_url = "mongodb://xxx:xxx@xxx:xxx/arxiv"
        client = pymongo.MongoClient(mongo_url)
        db = client['arxiv']
        old_collection = db['test_old']
        old_collection.drop()
        collection = db['test']
        collection.drop()

        test_post = [
            {'_id': 1,
             'fos': ['A', 'B'],
             'year': 1997,
             'authors': [{'name': 1}, {'name': 3}, {'name': 4}]
            },
            {'_id':2,
             'fos': ['B'],
             'year': 1997,
             'authors': [{'name': 1}, {'name': 2}, {'name': 3}]
            },
            {'_id': 3,
             'fos': ['A', 'B'],
             'year': 1998,
             'authors': [{'name': 1}, {'name': 5}]
            },
            {'_id': 4,
             'fos': ['A'],
             'year': 1997,
             'authors': [{'name': 1}, {'name': 4}, {'name': 6}]
            }
        ]
        post_id = old_collection.insert_many(test_post)

        category = 'A'
        begin = 1997
        end = 1997
        collection_name = 'test'
        databaseStore(db, old_collection, category, collection_name, begin, end)

        result = collection.find()
        for i in result:
            if category not in i['fos'] or i['year'] != 1997:
                flag = False
                break
        old_collection.drop()
        collection.drop()
        self.assertTrue(flag)

if __name__ == '__main__':
    unittest.main()
