import unittest
import networkx as nx
import pickle
import os

import sys
sys.path.append('../../Analysis')

from calcSimpleCoAuthor import loadGraphPickle, basicStats, calcCentrality

class TestCalcSimpleCoAuthor(unittest.TestCase):
    def testLoadGraphPickle(self):
        flag = True
        edges = [(1, 2), (1, 3), (2, 3)]
        nodes = [1, 2, 3, 4]
        edges_file = 'test_edges.pkl'
        nodes_file = 'test_nodes.pkl'
        with open(edges_file, 'wb') as f:
            pickle.dump(edges, f)
        with open(nodes_file, 'wb') as f:
            pickle.dump(nodes, f)
        signal = "null"
        graph = loadGraphPickle(edges_file, nodes_file, signal)
        t_edges = graph.edges
        t_nodes = graph.nodes
        if len(edges) != len(t_edges) or len(nodes) != len(t_nodes):
            flag = False
        if flag:
            for i in edges:
                if i not in t_edges or (i[1], i[0]) not in t_edges:
                    flag = False
                    break
        if flag:
            for i in nodes:
                if i not in t_nodes:
                    flag = False
                    break
        os.remove(edges_file)
        os.remove(nodes_file)

        edges = [(1, 2, 1.0), (1, 3, 1.0), (2, 3, 0.5)]
        nodes = [1, 2, 3, 4]
        with open(edges_file, 'wb') as f:
            pickle.dump(edges, f)
        with open(nodes_file, 'wb') as f:
            pickle.dump(nodes, f)
        signal = 'weight'
        graph = loadGraphPickle(edges_file, nodes_file, signal)
        t_nodes = graph.nodes
        if flag:
            if len(edges) != len(t_edges) or len(nodes) != len(t_nodes):
                flag = False
        if flag:
            for i in edges:
                if graph[i[0]][i[1]]['weight'] != i[2] or graph[i[1]][i[0]]['weight'] != i[2]:
                    flag = False
                    break
        if flag:
            for i in nodes:
                if i not in t_nodes:
                    flag = False
                    break
        os.remove(edges_file)
        os.remove(nodes_file)
        self.assertTrue(flag)

    def testBasicStats(self):
        flag = True
        edges = [(1, 2), (1, 3), (2, 3)]
        nodes = [1, 2, 3, 4]
        graph = nx.Graph()
        graph.add_edges_from(edges)
        graph.add_nodes_from(nodes)
        nodes_count, edges_count = basicStats(graph)
        if nodes_count != 4 or edges_count != 3:
            flag = False
        self.assertTrue(flag)

    def testCalcCentrality(self):
        flag = True
        edges = [(1, 2), (1, 3), (2, 3)]
        nodes = [1, 2, 3, 4]
        graph = nx.Graph()
        graph.add_edges_from(edges)
        graph.add_nodes_from(nodes)
        t_degree = [2, 2, 2, 0]
        degree = calcCentrality(graph)
        if len(degree) != len(t_degree):
            flag = False
        if flag:
            for i in range(len(t_degree)):
                if t_degree[i] != degree[i]:
                    flag = False
                    break
        self.assertTrue(flag)
        
if __name__ == '__main__':
        unittest.main()
