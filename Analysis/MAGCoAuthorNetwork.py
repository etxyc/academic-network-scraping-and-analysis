'''
This file is used to generate the co-authorship network from Microsoft Academic Graph database
'''
import pymongo
import pickle
import networkx as nx
from collections import Counter

from Analysis import genEdges, loadGraphList
from calcSimpleCoAuthor import basicStats
from DrawGraph import drawHistogramSequence

def loadCoAuthorData(mongo_url, collection_name, category):

    results = None
    try:
        client = pymongo.MongoClient(mongo_url,serverSelectionTimeoutMS = 1)
        db = client.arxiv
        collection = db[collection_name]
        results = collection.find(no_cursor_timeout = True) # through a special category
    except Exception as err:
        raise err

    return results

'''
This function is to generate the edges and nodes from the results, which can construct the co-authorship network
'''
def genEdgesNodes(results):

    edges = []
    edges_m = {}
    nodes = []
    nodes_m = {}
    for record in results:
        authors = []
        for author in record["authors"]:
            authors.append(author["name"])
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

    return edges, nodes

def main():           # pragma: no cover
    url = "mongodb://xxx:xxx@xxx:xxx/arxiv"
    mag_field = [("astrophysics", "Astrophysics"), ("statistics", "Statistics"), ("machine_learning", "Machine learning")]
    for (collection_name, category) in mag_field:
        print(category)
        res = loadCoAuthorData(url, collection_name, category)
        edges, nodes = genEdgesNodes(res)
        edges_file = "../pickle_file/mag_co_author_edges_{0}.pkl".format(collection_name)
        nodes_file = "../pickle_file/mag_co_author_nodes_{0}.pkl".format(collection_name)
        auth_graph_file = "../pickle_file/mag_co_auth_graph_{0}.pkl".format(collection_name)

        with open(edges_file, 'wb') as f:
            pickle.dump(edges, f)
        with open(nodes_file, 'wb') as f:
            pickle.dump(nodes, f) 

if __name__ == "__main__":
    main()
