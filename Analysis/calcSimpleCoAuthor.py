#########################################################################################################################
# This file is to get some network analysis information about co-authorship network: 
# the number of nodes and edges, the degrees.
#########################################################################################################################
from pymongo import MongoClient
from collections import Counter     # Takes in sorted list
from itertools import combinations
import re
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import time
import pickle
import DrawGraph as dp

############################################################
# This function is to get the graph from some files
# - f_edges: the pickle file name for the edges
# - f_nodes: the pickle file name for the nodes
# - singal: "weight" or "null" -> for mag database or arxiv
############################################################
def loadGraphPickle(f_edges, f_nodes, signal):

    graph = nx.Graph()
    edge_open = open(f_edges, "rb")
    node_open = open(f_nodes, "rb")
    graph.add_nodes_from(pickle.load(node_open))
    if(signal == "weight"):
        graph.add_weighted_edges_from(pickle.load(edge_open))
    else:
        graph.add_edges_from(pickle.load(edge_open))
    edge_open.close()
    node_open.close()
    return graph

#############################################################
# This function: get the number of edges and nodes
# - graph: a graph constructed by networkx
#############################################################
def basicStats(graph):

    nodes_count = len(graph)
    edge_count = graph.number_of_edges()
    print("Number of Nodes:", nodes_count)
    print("Number of Edges:", edge_count)

    return nodes_count, edge_count

############################################################
# This function: get a degree sequence for the graph
# - graph: a graph constructed by networkx 
############################################################
def calcCentrality(graph):

    degrees = [deg for n,deg in graph.degree()]

    return degrees

# function to store a graph to a pickle file, which don't need to test
def storeGraph(graph_file,auth_graph): # pragma: no cover
    with open(graph_file, 'wb') as f:
        pickle.dump(auth_graph, f)

# function to load a graph from a pickle file, which don't need to test
def loadGraph(graph_file): # pragma: no cover
    graph = pickle.load(open(graph_file,'rb'))
    return graph
        

def main(): # pragma: no cover
    # Load data from saved pickle files    
    category = "astrophysics"  # arxiv = stat.ML / astro-ph / stat  # mag = machine_learning / astrophysics / statistics
    edge_pickle_arxiv = "../pickle_file/edges_arxiv_{0}.pkl".format(category)
    node_pickle_arxiv = "../pickle_file/nodes_arxiv_{0}.pkl".format(category) 
    edge_pickle_mag = "../pickle_file/mag_co_author_edges_{0}.pkl".format(category)
    node_pickle_mag = "../pickle_file/mag_co_author_nodes_{0}.pkl".format(category) 

    edge_weight_arxiv = "../pickle_file/edges_weight_arxiv_{0}.pkl".format(category)
    node_weight_arxiv = "../pickle_file/nodes_weight_arxiv_{0}.pkl".format(category)
    edge_weight_mag = "../pickle_file/edges_weight_mag_spec_{0}.pkl".format(category)
    node_weight_mag = "../pickle_file/nodes_weight_mag_spec_{0}.pkl".format(category)

    # auth_graph_pickle = "../pickle_file/mag_co_author_graph_{0}.pkl".format(category)
    # auth_graph_pickle = "../pickle_file/mag_weight_co_author_graph_{0}.pkl".format(category)
    # auth_graph_pickle = "../pickle_file/arxiv_co_author_graph_{0}.pkl".format(category)
    # auth_graph_pickle = "../pickle_file/arxiv_weight_co_author_graph_{0}.pkl".format(category)
    
    signal = ""    # weight for weighted graph  # null
    # use for non-weighted
    edge_file = edge_pickle_mag     # arxiv # mag
    node_file = node_pickle_mag # arxiv # mag
    
    # use for weighted
    #edge_file = edge_weight_arxiv     # arxiv # mag
    #node_file = node_weight_arxiv     # arxiv # mag
    
    auth_graph = loadGraphPickle(edge_file, node_file, signal)
    #with open(auth_graph_pickle, 'wb') as f:
     #   pickle.dump(auth_graph, f)
        
    node_count, edge_count = basicStats(auth_graph)
    deg = calcCentrality(auth_graph)

    # Plot results

    histo_title = "mag"   # arxiv # mag
    signal = "double_log"   # single_log: log(fraction)  # double_log: log(fraction) vs log(deg)
    label = "Log"   # log   # <empty>
    x_title = "log" # log # <empty>
    weighted = ""  # weighted  # <empty>
    dp.drawHistogramSequence(deg,node_count,("{0}_{1}_{2}_simple_deg_distro").format(histo_title,category,weighted),"Degree")
    dp.drawLogHistogram(deg,node_count,signal,("{0}_{1}_{2}_{3}_log_deg_distro").format(histo_title,category,weighted,x_title),"{0} Degree".format(label), "Log Fraction")

    
if __name__ == "__main__":
    main()
