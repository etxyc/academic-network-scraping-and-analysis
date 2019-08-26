'''
This file is to calculate network analysis results from the citation network:
- directGraphBasicStat(graph): number of nodes, number of edges
- calcCentrality(graph): in_degree, out_degree
- calcEigen(graph): eigenvector centrality (average, max, min and non-zero min)
'''
import pymongo as mg
import re
import networkx as nx
import numpy as np
import pickle
from collections import Counter
import DrawGraph as dp


def directGraphBasicStat(graph):

    nodes_count = graph.number_of_nodes()
    edges_count = graph.size()
    
    print("Number of Nodes:", nodes_count)
    print("Number of Edges:", edges_count)
   
    return nodes_count, edges_count
    
def calcDeg(graph):
    
    in_degrees = [deg for name, deg in graph.in_degree()]
    out_degrees = [deg for name, deg in graph.out_degree()]
    return in_degrees, out_degrees


def calcEigen(graph):
    eigen_tuple = (nx.eigenvector_centrality(graph)).values()
    avg_eigen = sum(eigen_tuple)/len(eigen_tuple)
    max_eigen = max(eigen_tuple)
    min_0_eigen = min(eigen_tuple)
    min_eigen = min(i for i in eigen_tuple if i > 0)
    print("Average eigenvector = ",avg_eigen)
    print("Max, min, min(with 0) eigenvector = ",max_eigen,min_eigen,min_0_eigen)
    return avg_eigen, max_eigen, min_eigen, min_0_eigen


def main(): # pragma: no cover
    mongo_url = "mongodb://xxx:xxx@xxx:xxx/arxiv"
    
    collection_name = "machine_learning" # machine_learning # astrophysics # statistics
    # edge_pickle_file = "../pickle_file/mag_spec_cn_edges_{0}.pkl".format(collection_name)
    # node_pickle_file = "../pickle_file/mag_spec_cn_nodes_{0}.pkl".format(collection_name)
    graph_file = ("../pickle_file/mag_spec_cn_graph_{0}.pkl").format(collection_name)
    
    # load the graph
    graph = None
    with open(graph_file, 'rb') as f:
        graph = pickle.load(f)

    nodes_count, edges_count = directGraphBasicStat(graph)
    in_d,out_d = calcDeg(graph)
    
    signal = "double_log"   # single_log: log(fraction)  # double_log: log(fraction) vs log(deg)
    dp.drawHistogramSequence(in_d,nodes_count,("mag_{0}_simple_in_deg_distro").format(collection_name),"In Degree")
    dp.drawHistogramSequence(out_d,nodes_count,("mag_{0}_simple_out_deg_distro").format(collection_name),"Out Degree")
   
    dp.drawLogHistogram(in_d,nodes_count,signal,("mag_{0}_log_log_in_deg_distro").format(collection_name),"Log In Degree", "Log Fraction")
    dp.drawLogHistogram(out_d,nodes_count,signal,("mag_{0}_log_log_out_deg_distro").format(collection_name),"Log Out Degree", "Log Fraction")

    # calcEigen(graph)

    
if __name__ == "__main__":
    main()
