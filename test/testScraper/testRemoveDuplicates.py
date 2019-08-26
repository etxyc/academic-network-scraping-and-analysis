import unittest
import pymongo

import sys
sys.path.append('../../Scraping/arxiv')

import RemoveDuplicates as rd

class TestRemoveDuplicates(unittest.TestCase):

    def testDuplicatesRemove(self):
        flag = True
        mongo_url = "mongodb://xxx:xxx@xxx:xxx/arxiv"
        client = pymongo.MongoClient(mongo_url)
        db = client['arxiv']
        collection = db['test']
        collection.drop()
        # add the test code to the test
        posts = [
            {'_id': "1v1",
             'author': [1, 2, 3]
             },
            {'_id': "1v2",
             'author': [1, 2, 3]
             },
            {'_id': "2v1",
             'author': [1, 3, 4]
             },
            {'_id': "2v13",
             'author': [1, 3, 4]
             },
            {'_id': "1v4",
             'author': [1, 2, 3]
             },
            {'_id': "2v3",
             'author': [1, 3, 4]
             }
            ]
        validation = [
            {'_id': "2v13",
             'author': [1, 3, 4]
             },
            {'_id': "1v4",
             'author': [1, 2, 3]
             }
            ]

        post_id = collection.insert_many(posts)
        results = collection.find()
        rd.DuplicatesRemove(collection, results)
        results = collection.find()
        after_duplicates = []
        for record in results:
            after_duplicates.append(record)
        if len(validation) != len(after_duplicates):
            flag = False
        if flag:
            for i in validation:
                if i not in after_duplicates:
                    flag = False
                    break
        collection.drop()

        self.assertTrue(flag)

if __name__ == '__main__':
    unittest.main()
