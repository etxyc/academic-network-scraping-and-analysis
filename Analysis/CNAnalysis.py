'''
This file is used to generate the citation network from the MAG data in the Mongo database
'''
import pymongo as mg
import re
import networkx as nx
import numpy as np
import pickle
from collections import Counter
from DrawGraph import drawHistogramSequence

'''
This function is to get a particular category from mag_papers_all
- mongo_url: the url used to connect to the mongo database
- category: type(string), the category selected to construct the citation network
'''
def loadMagPaperAll(mongo_url, category): # load from collection: mag_papers_all (non field-specific)

    edges = []
    nodes = []
    edge_pickle_file = "../pickle_file/CN_edges_{0}.pkl".format(category)
    node_pickle_file = "../pickle_file/CN_nodes_{0}.pkl".format(category)
    try:
        client = mg.MongoClient(mongo_url, serverSelectionTimeoutMS = 1)
        results = client.arxiv.mag_papers_all.find({'fos': re.compile(category), 'year': {'$gte': 2007}, "authors": {'$exists': True, '$ne': None}}, no_cursor_timeout = True)
    except Exception as err:
        raise err

    return results


def loadDiGraphList(edges, nodes): # don't need to connect with the mongo database again and delete the mongo_url

    graph = nx.DiGraph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)

    return graph


def loadDiGraphPickle(f_edges, f_nodes):

    edges = pickle.load(open(f_edges, 'rb'))
    nodes = pickle.load(open(f_nodes, 'rb'))
    graph = loadDiGraphList(edges, nodes)

    return graph

# load from the the field-specific collection
def loadSpecDatabase(mongo_url, collection_name):

    try:
        client = mg.MongoClient(mongo_url, serverSelectionTimeoutMS = 1)
        db = client.arxiv
        collection = db[collection_name]
        # get all the information stored in the database
        results = collection.find(no_cursor_timeout = True)
    except Exception as err:
        print(err)

    return results


def loadDiGraphData(results):

    edges = []
    nodes = []
    edges_m = {}
    nodes_m = {}

    for record in results:
        if 'references' in record.keys():
            ref = record['references']
            for item in ref:
                if (record['_id'], item) not in edges_m.keys():
                    edges_m[(record['_id'], item)] = 0
                if item not in nodes_m.keys():
                    nodes_m[item] = 0
        if record['_id'] not in nodes_m.keys():
            nodes_m[record['_id']] = 0
    for item in edges_m.keys():
        edges.append(item)
    for item in nodes_m.keys():
        nodes.append(item)
    
    return edges, nodes


def main():  #pragma: no cover
    category = "Astrophysics"     # Machine learning # Astrophysics # Computer Science # Statistics
    mongo_url = "mongodb://xxx:xxx@xxx:xxx/arxiv"

    '''
    res = loadMagPaperAll(mongo_url, category)
    edges, nodes = loadDiGraphData(res)

    
    edge_pickle_file = "../pickle_file/CN_edges_{0}_2007.pkl".format(category)
    node_pickle_file = "../pickle_file/CN_nodes_{0}_2007.pkl".format(category)
    graph_file = ("../pickle_file/CN_graph({0})_2007.pkl").format(category)
    '''
    
    ############ above - load from the mag_paper_all and have some limitation

    ############ below - load from the specific database
    
    collection_name = "computer_science" # machine_learning # astrophysics # computer_science # statistics
    edge_pickle_file = "../pickle_file/mag_spec_cn_edges_{0}.pkl".format(collection_name)
    node_pickle_file = "../pickle_file/mag_spec_cn_nodes_{0}.pkl".format(collection_name)
    graph_file = ("../pickle_file/mag_spec_cn_graph_{0}.pkl").format(collection_name)
    
    
    res = loadSpecDatabase(mongo_url, collection_name)
    edges, nodes = loadDiGraphData(res)
    
    ############ Analysis and store the edges, nodes, and graph

    #store the edges and nodes

    with open(edge_pickle_file, 'wb') as f:
        pickle.dump(edges, f)
    with open(node_pickle_file, 'wb') as f:
        pickle.dump(nodes, f)

    
    # load the edges and nodes

    edges = None
    nodes = None
    with open(edge_pickle_file, 'rb') as f:
        edges = pickle.load(f)
    with open(node_pickle_file, 'rb') as f:
        nodes = pickle.load(f)


    graph = loadDiGraphList(edges, nodes)
    
    #store the graph

    with open(graph_file, 'wb') as f:
        pickle.dump(graph, f)

     
if __name__ == "__main__":
    main()
