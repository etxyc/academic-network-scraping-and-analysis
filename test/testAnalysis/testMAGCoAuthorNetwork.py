import unittest
import pymongo

import sys
sys.path.append('../../Analysis')

from MAGCoAuthorNetwork import *

class TestMAGCoAuthorNetwork(unittest.TestCase):
    def testLoadCoAuthorData(self):
        flag = False
        mongo_url = "mongodb://xxx:xxx@xxx:xxx/arxiv"
        collection_name = 'machine_learning'
        category = 'Machine learning'
        result = loadCoAuthorData(mongo_url, collection_name, category)
        for i in result:
            if category in i['fos']:
                flag = True
                break
        self.assertTrue(flag)

    def testGenEdgesNodes(self):
        flag = True
        results = [
            {'_id': 1,
             'authors': [{'name': 1}, {'name': 2}]
             },
            {'_id': 2,
             'authors': [{'name': 1}, {'name': 2}, {'name': 3}]
             }
            ]
        t_nodes = [1, 2, 3]
        t_edges = [(1, 2), (2, 3), (1, 3)]
        edges, nodes = genEdgesNodes(results)
        if len(edges) != len(t_edges) or len(nodes) != len(t_nodes):
            flag = False
        if flag:
            for i in t_nodes:
                if i not in nodes:
                    flag = False
                    break
        if flag:
            for i in t_edges:
                if i not in edges:
                    flag = False
                    break
        self.assertTrue(flag)

if __name__ == '__main__':
        unittest.main()
