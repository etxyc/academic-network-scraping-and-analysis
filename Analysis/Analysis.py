'''
This file is used to load the ArXiv data from Mongo database and build a simple coauthorship network.
'''
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


def loadMongo(mongo_url, category): 

    edges = []
    edges_m = {}
    nodes = []
    nodes_m = {}
    try:
        client = MongoClient(mongo_url, serverSelectionTimeoutMS = 1)
        client.server_info()
        results = client.arxiv.papers.find({'category.0': re.compile(category)}, no_cursor_timeout = True)
        
        for record in results:
            print(record)
            authors = list(record["author"])
            newedges = genEdges(authors)
            for item in newedges:
                if item not in edges_m.keys():
                    edges_m[item] = 0
            for item in authors:
                if item not in nodes_m.keys():
                    nodes_m[item] = 0
        for item in edges_m.keys():
            edges.append(item)
        for item in nodes_m.keys():
            nodes.append(item)
    except Exception as err:
        raise err

    return edges, nodes


def genEdges(author_list):

    edges = []
    for i in range(0, len(author_list) - 1):
        item = author_list[i]
        index = i + 1
        for j in range(index, len(author_list)):
            if item < author_list[j]:
                edges.append((item, author_list[j]))
            else:
                edges.append((author_list[j], item))
    return edges


def loadGraphList(edges, nodes):

    graph = nx.Graph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)
    return graph



if __name__ == "__main__": # pragma: no cover
    # Load data from mongoDB
    mongo_url = "mongodb://xxx:xxx@xxx:xxx/arxiv"

    field = ['stat', 'astro-ph', 'stat.ML']
    for category in field:
        print(category)
        edges, nodes = loadMongo(mongo_url, category)
        
        # Save the nodes and edges
        edge_pickle_file = "../pickle_file/edges_arxiv_{0}.pkl".format(category)
        node_pickle_file = "../pickle_file/nodes_arxiv_{0}.pkl".format(category) 
        edge_open = open(edge_pickle_file, "wb")
        node_open = open(node_pickle_file, "wb")
        pickle.dump(edges, edge_open)
        pickle.dump(nodes, node_open)
        edge_open.close()
        node_open.close()
    
    
