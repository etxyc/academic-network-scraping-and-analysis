import unittest
import pymongo
import networkx as nx

import sys
sys.path.append('../../Analysis')
# from src.function import BasicFunction

from CNAnalysis import *

class TestCNAnalysis(unittest.TestCase):
    # def setUp(self):
        # self.func = BasicFunction()

    def testLoadDiGraphData(self):
        flag = True
        results = [{'_id': '1',
                    'references': ['2', '3', '4', '5']
                    },
                   {'_id': '2',
                    'references': ['3', '4', '5']
                    },
                   {'_id': '3',
                    'references': ['4', '6']
                    },
                   {'_id': '4'
                    },
                   {'_id': '6',
                    'references': ['8']
                    }
        ]
        t_edges = [('1', '2'), ('1', '3'), ('1', '4'), ('1', '5'), ('2', '3'), ('2', '4'), ('2', '5'), ('3', '4'), ('3', '6'), ('6', '8')]
        t_nodes = ['1', '2', '3', '4', '5', '6', '8']
        edges, nodes = loadDiGraphData(results)
        if len(t_edges) != len(edges) or len(t_nodes) != len(nodes):
            flag = False
        if flag:
            for i in t_edges:
                if i not in edges:
                    flag = False
                    break
        if flag:
            for i in t_nodes:
                if i not in nodes:
                    flag = False
                    break

        self.assertTrue(flag)

    def testLoadMagPaperAll(self):
        flag = False
        category = "Astrophysics"
        mongo_url = "mongodb://xxx:xxx@xxx:xxx/arxiv"
        results = loadMagPaperAll(mongo_url, category)
        for i in results:
            if category in i['fos']:
                flag = True
                break
        self.assertTrue(flag)

    def testLoadDiGraphList(self):
        flag = True
        nodes = [1, 2, 3]
        edges = [(1, 2), (1, 3), (2, 3)]
        test_graph = loadDiGraphList(edges, nodes)
        if len(edges) != len(test_graph.edges) or len(nodes) != len(test_graph.nodes):
            flag = False
        if flag:
            for i in edges:
                if i not in test_graph.edges:
                    flag = False
                    break
        if flag:
            for i in nodes:
                if i not in test_graph.nodes:
                    flag = False
                    break

        self.assertTrue(flag)

    def testLoadSpecDatabase(self):
        flag = False
        collection = "astrophysics"
        category = 'Astrophysics'
        mongo_url = "mongodb://xxx:xxx@xxx:xxx/arxiv"
        results = loadSpecDatabase(mongo_url, collection)
        for i in results:
            if category in i['fos']:
                flag = True
                break
        self.assertTrue(flag)

    def testLoadDiGraphData(self):
        flag = True
        results = [
            {'_id': 1,
             'references': [2, 3]
            },
            {'_id': 2,
             'references': [3]
            }
        ]
        nodes = [1, 2, 3]
        edges = [(1, 2), (1, 3), (2, 3)]
        t_edges, t_nodes = loadDiGraphData(results)
        if len(nodes) != len(t_nodes) or len(edges) != len(t_edges):
            flag = False
        if flag:
            for i in nodes:
                if i not in t_nodes:
                    flag = False
                    break
        if flag:
            for i in edges:
                 if i not in t_edges:
                     flag = False
                     break
        self.assertTrue(flag)

if __name__ == '__main__':
    unittest.main()
