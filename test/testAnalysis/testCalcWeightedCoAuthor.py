import unittest
import networkx as nx
import pickle

import sys
sys.path.append('../../Analysis')

import CalcWeightedCoAuthor as cwa

class TestGraph(unittest.TestCase):

    def setUp(self):
        self.no_node = 4
        self.connected_graph = nx.complete_graph(self.no_node)

    def testCloseness(self):
        signal = None
        avg_close, max_close, min_close, min_0_close  = cwa.calCloseness(self.connected_graph,signal)
        closeness = [avg_close, max_close, min_close, min_0_close]
        self.assertTrue(all(x == 1 for x in closeness))



if __name__ == '__main__':
    unittest.main()
