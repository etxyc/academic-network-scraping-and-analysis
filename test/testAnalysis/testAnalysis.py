import unittest
import networkx as nx
import pickle

import sys
sys.path.append('../../Analysis')

import Analysis as aly

class TestGraph(unittest.TestCase):

    def setUp(self):

        self.author_nodes = ['A', 'B', 'C']
        self.author_edges = [('A', 'B'), ('A', 'C'), ('B', 'C')]
        self.author_nodes_two = ['A', 'B', 'C', 'D']
        self.author_edges_two = [('A', 'B'), ('A', 'C'), ('B', 'C'),
                                 ('A', 'D'), ('B', 'D'), ('C', 'D')]
        self.no_node = 4
        self.connected_graph = nx.complete_graph(self.no_node)



    def test_genEdges(self):     # Tests the edge generation function (which joins two authors in a list of authors to form an edge)

        test_edges_one = aly.genEdges(self.author_nodes)
        test_edges_two = aly.genEdges(self.author_nodes_two)

        self.assertTrue(sorted(self.author_edges) == sorted(test_edges_one))
        self.assertTrue(sorted(self.author_edges_two) == sorted(test_edges_two))


    def test_loadGraphList(self):   # Tests loading adjacency list function to make sure the graph created is correct

        test_graph = aly.loadGraphList(self.author_edges,self.author_nodes_two).adj
        correct_graph = {'A': {'B': {}, 'C': {}}, 'B': {'A': {}, 'C': {}},'D': {}, 'C': {'B': {}, 'A': {}}}

        self.assertTrue(test_graph == correct_graph)


    def test_loadMongoConnection(self):     # Tests wrong domain/login credentials

        wrong_domain = "mongod://xxx:xxx@xxx:xxx/arxiv"
        wrong_login = "mongod://xxx:xxx@xxx:xxx/arxiv"
        correct_login = "mongodb://xxx:xxx@xxx:xxx/arxiv"
        control_category = "stat.ML"

        self.assertRaises(Exception, aly.loadMongo, wrong_domain, control_category)
        self.assertRaises(Exception, aly.loadMongo, wrong_login, control_category)


if __name__ == '__main__':
    unittest.main()
