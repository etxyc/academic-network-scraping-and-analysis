'''
This file is to calculate the closeness centrality of the weighted coauthorship network
'''
import networkx as nx

from calcSimpleCoAuthor import loadGraphPickle
from calcSimpleCoAuthor import basicStats

def calCloseness(graph,signal):
    nodes, edges = basicStats(graph)
    close_tuple = (nx.closeness_centrality(graph,distance=signal)).values()
    avg_close = sum(close_tuple)/len(close_tuple)
    max_close = max(close_tuple)
    min_0_close = min(close_tuple)
    min_close = min(i for i in close_tuple if i > 0)
    print("Average closeness = ",avg_close)
    print("Max, min, min(with 0) closeness = ",max_close,min_close,min_0_close)
    return avg_close, max_close, min_close, min_0_close



def main(): # pragma: no cover
    category = 'astrophysics'
    edge_weight_arxiv = "../pickle_file/edges_weight_arxiv_inverse_{0}.pkl".format(category)
    node_weight_arxiv = "../pickle_file/nodes_weight_arxiv_inverse_{0}.pkl".format(category)
    edge_weight_mag = "../pickle_file/edges_weight_mag_spec_inverse_{0}.pkl".format(category)
    node_weight_mag = "../pickle_file/nodes_weight_mag_spec_inverse_{0}.pkl".format(category)

    edge_file = edge_weight_mag     # arxiv # mag
    node_file = node_weight_mag     # arxiv # mag
    signal = "weight"  # weight # None
    auth_graph = loadGraphPickle(edge_file, node_file, signal)
    calCloseness(auth_graph,signal)
    
if __name__ == "__main__":
    main()
