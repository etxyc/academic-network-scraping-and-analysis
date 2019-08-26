from pymongo import MongoClient
from collections import Counter     # Takes in sorted list
from itertools import combinations
import re
import networkx as nx
import community as cm
import pickle
import numpy as np
from numpy.polynomial.polynomial import polyfit, Polynomial
import matplotlib.pyplot as plt
plt.switch_backend('agg')


def partition (category = "stat.ML"):

    url = "mongodb://xxx:xxx@xxx:xxx/arxiv"
    db = MongoClient(url, serverSelectionTimeoutMS = 100).arxiv.papers
    papers = list( db.find({"category.0": re.compile(category)}) )

    # Make coauthorship network
    edges = (pairs for ppr in papers
                   for pairs in combinations(ppr["author"], 2))
    graph = nx.Graph()
    graph.add_edges_from(edges)
    # Some nodes have no edge
    graph.add_nodes_from(db.find({"category.0": re.compile(category)})
                           .distinct("author"))

    # Divide authors into groups
    dendo = cm.generate_dendrogram(graph)
    author_group = cm.partition_at_level(dendo, len(dendo) - 1)

    # Get authors in each group
    group_authors = {}
    for author, group in author_group.items():
        group_authors.setdefault(group, []).append(author)

    # Get paper titles by each author
    author_papers = {}
    for paper in papers:
        for author in paper["author"]:
            author_papers.setdefault(author, []).append(paper["_id"])

    with open(category + "_author_papers.pkl", "wb") as file:
        pickle.dump(author_papers, file)

    # Repeated counting of papers in each group
    group_nPapers = {}
    for group, members in group_authors.items():
        group_nPapers[group] = 0
        for author in members:
            group_nPapers[group] += len(author_papers[author])

    # Warning: dict_keys are unordered
    assert(group_authors.keys() == group_nPapers.keys())
    joined = ((len(group_authors[grp]), group_nPapers[grp])
              for grp in group_authors)
    nAuthors, nPapers = zip(*sorted(joined))
    fit = Polynomial(polyfit(nAuthors, nPapers, 2))

    plt.plot(nAuthors, nPapers, "r.")
    plt.plot(nAuthors, fit(np.array(nAuthors)), "b-", linewidth = 1)
    # fit() takes in a number or NumPy array, but not tuple
    plt.title(category)
    plt.xlabel("Number of Authors in a Group", fontsize = 12)
    plt.ylabel("Number of (Repeated) Papers in a Group", fontsize = 12)
    plt.savefig(category + "_nAuthors_nPapers_rept.png")
    plt.gcf().clear()

    # Fractional counting of papers in each group
    group_nPapers = {}
    for paper in papers:
        total = len(paper["author"])
        groups = (author_group[ath] for ath in paper["author"])
        groups = Counter(sorted(groups))
        groups = {g: n / total for g, n in groups.items()}
        for g in groups:
            group_nPapers[g] = group_nPapers.get(g, 0) + groups[g]

    # Warning: dict_keys are unordered
    assert(group_authors.keys() == group_nPapers.keys())
    joined = ((len(group_authors[grp]), group_nPapers[grp])
              for grp in group_authors)
    nAuthors, nPapers = zip(*sorted(joined))
    fit = Polynomial(polyfit(nAuthors, nPapers, 2))

    plt.plot(nAuthors, nPapers, "r.")
    plt.plot(nAuthors, fit(np.array(nAuthors)), "b-", linewidth = 1)
    # fit() takes in a number or NumPy array, but not tuple
    plt.title(category)
    plt.xlabel("Number of Authors in a Group", fontsize = 12)
    plt.ylabel("Number of (Fractional) Papers in a Group", fontsize = 12)
    plt.savefig(category + "_nAuthors_nPapers_frac.png")
    plt.gcf().clear()

    author_nPapers = {ath: len(ppr) for ath, ppr in author_papers.items()}

    # Degree
    author_deg = dict(graph.degree())
    assert(author_deg.keys() == author_nPapers.keys())
    joined = ((author_deg[ath], author_nPapers[ath])
              for ath in author_nPapers)
    deg, nPapers = zip(* joined)

    plt.plot(deg, nPapers, "r.")
    plt.title(category)
    plt.xlabel("Author's Degree", fontsize = 12)
    plt.ylabel("Number of Papers", fontsize = 12)
    plt.savefig(category + "_degree_nPapers.png")
    plt.gcf().clear()

    # Eigenvector Centrality
    author_central = nx.eigenvector_centrality(graph, max_iter = 256, tol = 1e-9)
    with open(category + "_centrality.pkl", "wb") as file:
        pickle.dump(author_central, file)

    assert(author_central.keys() == author_nPapers.keys())
    joined = ((author_central[ath], author_nPapers[ath])
              for ath in author_nPapers)
    central, nPapers = zip(* joined)

    plt.plot(central, nPapers, "r.")
    plt.title(category)
    plt.xlabel("Author's Eigenvector Centrality", fontsize = 12)
    plt.ylabel("Number of Papers", fontsize = 12)
    plt.savefig(category + "_central_nPapers.png")


if __name__ == "__main__":

    for category in ["stat.ML", "stat", "astro-ph"]:
        partition(category)
