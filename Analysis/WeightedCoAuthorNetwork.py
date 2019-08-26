'''
This file is used to generate the weighted co-authorship network
'''
import pickle

from Analysis import genEdges
from BasicStatAnalysis import loadData
from CNAnalysis import loadSpecDatabase
import DrawGraph as dp
import calcSimpleCoAuthor as an

def getWeightedCoAuthorNetwork(res, method = 'arxiv'):

    # gen edges and nodes
    edges = []
    nodes = []
    edges_m = {}
    nodes_m = {}

    for record in res:
        authors_list = []
        if method == 'arxiv':
            authors_list = record['author']
        elif method == 'mag':
            for author in record["authors"]:
                authors_list.append(author["name"])

        newedges = genEdges(authors_list)
        for item in newedges:
            weight_collab = 1.0 / (len(authors_list) - 1)
            if item not in edges_m.keys():
                edges_m[item] = weight_collab
            else:
                edges_m[item] += weight_collab
        for i in authors_list:
            if i not in nodes_m.keys():
                nodes_m[i] = 0
    for item in edges_m.keys():
        edges.append((item[0], item[1], 1/(edges_m[item])))
    for item in nodes_m.keys():
        nodes.append(item)

    return edges, nodes


def main(): # pragma: no cover
    mongo_url = "mongodb://xxx:xxx@xxx:xxx/arxiv"

    field = ['stat', 'astro-ph', 'stat.ML']
    for category in field:
        print(category)
        res = loadData(mongo_url, category)
        edges, nodes = getWeightedCoAuthorNetwork(res, method = 'arxiv')
        edge_pickle_file = "../pickle_file/edges_weight_arxiv_inverse_{0}.pkl".format(category)
        node_pickle_file = "../pickle_file/nodes_weight_arxiv_inverse_{0}.pkl".format(category)
        with open(edge_pickle_file, 'wb') as f:
            pickle.dump(edges, f)
        with open(node_pickle_file, 'wb') as f:
            pickle.dump(nodes, f)

    ######## above - for arxiv

    ######## below - for mag_spec

    # field = ['Statistics', 'Computer Science', 'Astrophysics', 'Machine learning']
    mag_field = [("machine_learning", "Machine learning"), ("astrophysics", "Astrophysics"), ("computer_science", "Computer Science"), ("statistics", "Statistics")]     
    for collection_name, category in mag_field:
        print(category)
        res = loadSpecDatabase(mongo_url, collection_name)
        edges, nodes = getWeightedCoAuthorNetwork(res, method = 'mag')
        edge_pickle_file = "../pickle_file/edges_weight_mag_spec_inverse_{0}.pkl".format(collection_name)
        node_pickle_file = "../pickle_file/nodes_weight_mag_spec_inverse_{0}.pkl".format(collection_name)

        ######## store the edges and nodes(weighted)

        with open(edge_pickle_file, 'wb') as f:
            pickle.dump(edges, f)
        with open(node_pickle_file, 'wb') as f:
            pickle.dump(nodes, f)
    
if __name__ == "__main__":
    main()
