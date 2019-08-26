import sys
sys.path.append('../../Analysis')
import unittest

from WeightedCoAuthorNetwork import *

class TestWeightedCoAuthorNetwork(unittest.TestCase):
    def testGetWeightedCoAuthorNetwork(self):
        flag = True
        test_post = [
            {'_id': 1,
             'category': ['A', 'B'],
             'author': [1, 3, 4]
            },
            {'_id': 3,
             'category': ['A', 'B'],
             'author': [1, 5]
            },
            {'_id': 4,
             'category': ['A'],
             'author': [1, 4, 6]
        }]
        test_post2 = [
            {'_id': 1,
             'fos': ['A', 'B'],
             'year': 1997,
             'authors': [{'name': 1}, {'name': 3}, {'name': 4}]
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
        }]
        # t_edges = [(1, 3, 0.5), (1, 4, 1.0), (1, 5, 1.0), (1, 6, 0.5), (3, 4, 0.5), (4, 6, 0.5)]
        t_edges = [(1, 3, 2.0), (1, 4, 1.0), (3, 4, 2.0), (1, 5, 1.0), (1, 6, 2.0), (4, 6, 2.0)]
        t_nodes = [1, 3, 4, 5, 6]

        m = 'arxiv'
        edges, nodes = getWeightedCoAuthorNetwork(test_post, method = m)
        if len(t_edges) != len(edges):
            flag = False
        if flag and len(t_nodes) != len(nodes):
            flag = False
        if flag:
            nodes = sorted(nodes)
            for i in range(len(t_nodes)):
                if nodes[i] != t_nodes[i]:
                    flag = False
                    break
        if flag:
            for item in t_edges:
                if item not in edges:
                    if (item[1], item[0], item[2]) not in edges:
                        flag = False
                        break

        m = 'mag'
        edges, nodes = getWeightedCoAuthorNetwork(test_post2, method = m)
        if len(t_edges) != len(edges):
            flag = False
        if flag and len(t_nodes) != len(nodes):
            flag = False
        if flag:
            nodes = sorted(nodes)
            for i in range(len(t_nodes)):
                if nodes[i] != t_nodes[i]:
                    flag = False
                    break
        if flag:
            for item in t_edges:
                if item not in edges:
                    if (item[1], item[0], item[2]) not in edges:
                        flag = False
                        break
        self.assertTrue(flag)

if __name__ == "__main__":
    unittest.main()
