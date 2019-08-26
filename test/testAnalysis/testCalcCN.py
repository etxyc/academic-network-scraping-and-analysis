import unittest
import pymongo
import networkx as nx

import sys
sys.path.append('../Analysis')
# from src.function import BasicFunction

import CalcCN as ccn

class TestCalcCN(unittest.TestCase):

    def setUp(self):
        self.no_node = 4
        self.connected_graph = nx.complete_graph(self.no_node)

    def testEigen(self):
        avg_eigen, max_eigen, min_eigen, min_0_eigen  = ccn.calcEigen(self.connected_graph)
        eigenvector = [avg_eigen, max_eigen, min_eigen, min_0_eigen]
        self.assertTrue(len(set(eigenvector))==1)

        
    def testDirectGraphBasicStat(self):
        flag = True
        edges = [('1', '2'), ('1', '3'), ('1', '4'), ('1', '5'), ('2', '3'), ('2', '4'), ('2', '5'), ('3', '4'), ('3', '6'), ('6', '8')]
        nodes = ['1', '2', '3', '4', '5', '6', '8']
        t_nodes_count = 7
        t_edges_count = 10
        graph = nx.DiGraph()
        graph.add_nodes_from(nodes)
        graph.add_edges_from(edges)
        nodes_count, edges_count = ccn.directGraphBasicStat(graph)
        if t_nodes_count != nodes_count or t_edges_count != edges_count:
            flag = False
        self.assertTrue(flag)

    def testCalcDeg(self):
        flag = True
        edges = [('1', '2'), ('1', '3'), ('1', '4'), ('1', '5'), ('2', '3'), ('2', '4'), ('2', '5'), ('3', '4'), ('3', '6'), ('6', '8')]
        nodes = ['1', '2', '3', '4', '5', '6', '8']
        graph = nx.DiGraph()
        graph.add_nodes_from(nodes)
        graph.add_edges_from(edges)
        t_in_degree = [0, 1, 1, 1, 2, 2, 3]
        t_out_degree = [0, 0, 0, 1, 2, 3, 4]
        in_degree, out_degree = ccn.calcDeg(graph)
        in_degree.sort()
        out_degree.sort()
        if len(t_in_degree) != len(in_degree) or len(t_out_degree) != len(out_degree):
            flag = False
        if flag:
            for i in range(len(t_in_degree)):
                if t_in_degree[i] != in_degree[i]:
                    flag = False
                    break
        if flag:
            for i in range(len(t_out_degree)):
                if t_out_degree[i] != out_degree[i]:
                    flag = False
                    break
        self.assertTrue(flag)


        
        
if __name__ == '__main__':
    unittest.main()
