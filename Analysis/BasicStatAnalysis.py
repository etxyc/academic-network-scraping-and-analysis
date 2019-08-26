#########################################################################################################################
# This file is to get some basic statistic analysis information
# 'paper_per_year'
# 'papers_authors_average_per_year'
# 'authors_per_year'
# 'authors_per_paper_per_year'
# 'papers_per_author_per_year'
#########################################################################################################################
import matplotlib.pyplot as plt
import numpy as np
import pymongo
import re
import collections
import csv
import pickle

from DrawGraph import draw_compare
from CNAnalysis import loadMagPaperAll

'''
This function is to get 5 lists which record the information about:
'paper_per_year', 'papers_authors_average_per_year', 'authors_per_year', 'authors_per_paper_per_year', 'papers_per_author_per_year'
'''
def basic_stat_analysis(mongo_url, category = "stat", method = 'arxiv'):

    if method == 'arxiv':
        result = loadData(mongo_url, category)
    elif method == 'mag':
        result = loadMagPaperAll(mongo_url, category)
    list1, list2, list3, list4, list5 = analysis(result, category, method = method)
    return list1, list2, list3, list4, list5

def loadData(mongo_url, category):

    client = pymongo.MongoClient(mongo_url)
    db = client.arxiv
    posts = db.papers
    res = posts.find({'category.0' : re.compile(category)}, no_cursor_timeout = True)
    return res

def analysis(res, category, method):

    # papers per year
    list1 = {}
    # productivity per year - papers/authors
    list2 = {}
    # authors per year
    list3 = {}
    # authors_per_paper_per_year
    list4 = {}
    # papers_per_author_per_year
    list5 = {}

    author_list = {}
    papers_authors = {}
    author_frequency = {}
    for record in res:
        year = None
        authors = []
        if method == 'arxiv':
            year = int(record['published'].split("T")[0].split("-")[0])
            authors = record['author']
        elif method == 'mag':
            year = record['year']
            for author in record["authors"]:
                authors.append(author["name"])

        if year in list1.keys():
            list1[year] += 1
            temp = {}
            for author in authors:
                if author not in author_list[year]:
                    author_list[year].append(author)
                    papers_authors[year][author] = 1
                else:
                    papers_authors[year][author] += 1
        else:
            list1[year] = 1
            author_list[year] = list(authors)
            papers_authors[year] = {}
            for author in authors:
                papers_authors[year][author] = 1
        if year in list4.keys():
            list4[year] += len(authors)
            if len(authors) in author_frequency[year].keys():
                author_frequency[year][len(authors)] += 1
            else:
                author_frequency[year][len(authors)] = 1
        else:
            list4[year] = len(authors)
            temp = {}
            temp[len(authors)] = 1
            author_frequency[year] = temp

    for item in author_list.keys():
        list3[item] = len(author_list[item])
        list2[item] = list1[item] / len(author_list[item])

    for item in list4.keys():
        list4[item] /= list1[item]

    '''
    with open(("../pickle_file/papers_authors_{0}.pkl").format(category), 'wb') as f:
        pickle.dump(papers_authors, f)
    with open(("../pickle_file/author_frequency_{0}.pkl").format(category), 'wb') as f:
        pickle.dump(author_frequency, f)
    '''

    for item in papers_authors.keys():
        sum_papers = 0.0
        for author in papers_authors[item].keys():
            sum_papers += papers_authors[item][author]
        list5[item] = sum_papers / float(list3[item])

    return list1, list2, list3, list4, list5


def main():

    mongo_url = "mongodb://xxx:xxx@xxx:xxx/arxiv"
    # select_field = ['stat', 'astro-ph', 'stat.ML'] # for arxiv
    # method_db = 'arxiv'
    select_field = ['Statistics', 'Astrophysics', 'Machine learning'] # for mag
    method_db = 'mag'
    method_list = ['paper_per_year', 'papers_authors_average_per_year', 'authors_per_year', 'authors_per_paper_per_year', 'papers_per_author_per_year']
    data = [[], [], [], [], []]

    for item in select_field:
        print(item)
        list1, list2, list3, list4, list5 = basic_stat_analysis(mongo_url, category = item, method = method_db)
        data[0].append(list1)
        data[1].append(list2)
        data[2].append(list3)
        data[3].append(list4)
        data[4].append(list5)
    with open('../pickle_file/basic_stat_data_{0}.pkl'.format(method_db), 'wb') as f:
        pickle.dump(data, f)

    '''
    data = None
    with open('../pickle_file/basic_stat_data_{0}.pkl'.format(method_db), 'rb') as f:
        data = pickle.load(f)
    '''

    for i in range(len(method_list)):
        draw_compare(data[i], select_field, method = ("{0}_{1}").format(method_db, method_list[i]))

if __name__ == '__main__':
    main()
