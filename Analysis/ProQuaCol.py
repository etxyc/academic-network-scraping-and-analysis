'''
This file can be used to calculate the productiviy, quality and collaboration value
of the author.

Productivity = No. of papers published by each author in the period
Collaboration = Ave No. of authors per paper by each author in the period
Quality = Ave. No. of citations per paper by each author

You can use the function getOneCategory(startYear, endYear, collection_name, graph_file, sampleNo, outputFileName)
to get those vaue for all the author in one category.
startYear and endYear can justify the time period.collection_name is the name of
collection you want to analysis in the database. graph_file is the file that contain the
citation network information. sampleNo is the number of sample you want to select. outputFileName is the file name
of the output.
The function generates a pickle file. This pickle file can be used to draw corresponding diagram and do further analysis.
'''

import networkx as nx
import pymongo
import re
import pickle
import random

def loadResult(mongo_url, collection_name, startYear, endYear):
    client = pymongo.MongoClient(mongo_url)
    db = client.arxiv
    posts = db[collection_name]
    res = posts.find({'year': {"$gte": startYear, "$lte": endYear}})
    return res


def loadRawData(mongo_url, collection_name):
    client = pymongo.MongoClient(mongo_url)
    db = client.arxiv
    posts = db[collection_name]
    return posts


def findActivePeriod(posts, author, startYear, endYear):
    first = posts.find({'authors.name': author, 'year': {"$gte": startYear, "$lte":endYear}}).sort('year', +1).limit(1)
    last = posts.find({'authors.name': author, 'year': {"$gte": startYear, "$lte":endYear}}).sort('year', -1).limit(1)

    firstPublish = first.next()
    lastPublish = last.next()

    firstPublishYear = firstPublish['year']
    lastPublishYear = lastPublish['year']

    return firstPublishYear, lastPublishYear


def activePeriod(firstPublish, lastPublish):
    activePeriod = lastPublish - firstPublish + 1
    return activePeriod

def thisAuthorPaper(posts, author, firstPublish, lastPublish):
    oneAuthorPaper = posts.find({'authors.name': author, 'year': {"$gte": firstPublish, "$lte":lastPublish}})
    return oneAuthorPaper

def noPaperThisAuthor(posts, author, firstPublish, lastPublish):
    return posts.find({'authors.name': author, 'year': {"$gte": firstPublish, "$lte":lastPublish}}).count()

def productivity(noPaperThisAuthor, actPeriod):
    return noPaperThisAuthor / actPeriod

def collaboration(oneAuthorPaper):
    noPaperThisAuthor = oneAuthorPaper.count()

    sum_total = 0
    for paper in oneAuthorPaper:
        sum_total += len(paper['authors'])-1

    return sum_total / noPaperThisAuthor

def quality(oneAuthorPaper, citation):

    no = oneAuthorPaper.count()

    sum_total = 0.0
    for paper in oneAuthorPaper:
        try: #TODO
            sum_total += citation[paper['_id']]
        except Exception as err:
            pass

    return sum_total / no

def oneAuthorValue(author, posts, starYear, endYear, citation):
    firstPublish, lastPublish = findActivePeriod(posts, author, starYear, endYear)
    act = activePeriod(firstPublish, lastPublish)
    thisAuthorAllPaper1 = thisAuthorPaper(posts, author, firstPublish, lastPublish)
    thisAuthorAllPaper2 = thisAuthorPaper(posts, author, firstPublish, lastPublish)

    noPaperThisAuthor = thisAuthorAllPaper1.count()

    thisProductivity = productivity(noPaperThisAuthor, act)
    thisCollaboration = collaboration(thisAuthorAllPaper1)
    thisQuality = quality(thisAuthorAllPaper2, citation)

    return thisProductivity, thisQuality, thisCollaboration

def getCitationNum(graph):
    citation = {}
    for item in graph.in_degree():
        citation[item[0]] = item[1]
    return citation


def getOneCategory(startYear, endYear, collection_name, graph_file, sampleNo, outputFileName):
    mongo_url = "mongodb://xxx:xxx@xxx:xxx/arxiv"
    posts = loadRawData(mongo_url, collection_name)
    authors = []
    collection = posts.find()

    for post in collection:
        for authorJSON in post['authors']:
            authors.append(authorJSON['name'])
    authors = list(set(authors))

    results = {}
    graph = None

    with open(graph_file, 'rb') as f:
        graph = pickle.load(f)
    citation = getCitationNum(graph)

    noAuthor = len(authors)
   # print("No. of authers:", noAuthor)

    count = 0
    authorSample = random.sample(authors, sampleNo)

    for author in authorSample:
        pro, qua, col = oneAuthorValue(author, posts, startYear, endYear, citation)
        results[author] = {'productivity': pro, 'quality': qua, 'collaboration': col}

        if(qua > 0):
            pass
   #         print(results[author])
        count += 1
   #     print("Completed: ", count, "/" , noAuthor)
   #     print(collection_name)

    with open(outputFileName, 'wb') as f:
        pickle.dump(results, f)


def main(): #pragma: no cover

    mongo_url = "mongodb://xxx:xxx@xxx:xxx/arxiv"
    startYear = 2014
    endYear = 2016

    collection_name = 'statistics'
    posts = loadRawData(mongo_url, collection_name)
    ProQuaColData = "ProQuaColData_" + collection_name + ".pkl"
    authors = []
    graph_file = "../pickle_file/mag_spec_cn_graph_statistics.pkl"
    sampleNo = 9000

    collection = posts.find()

    for post in collection:
        for authorJSON in post['authors']:
            authors.append(authorJSON['name'])
    authors = list(set(authors))

    results = {}

    graph = None

    with open(graph_file, 'rb') as f:
        graph = pickle.load(f)
    citation = getCitationNum(graph)

    noAuthor = len(authors)
    #print("No. of authers:", noAuthor)

    count = 0
    authorSample = random.sample(authors, sampleNo)

    for author in authorSample:
        pro, qua, col = oneAuthorValue(author, posts, startYear, endYear, citation)
        results[author] = {'productivity': pro, 'quality': qua, 'collaboration': col}


        if(qua > 0):
            pass
    #        print(results[author])
        count += 1
    #    print("Completed: ", count, "/" , noAuthor)
    #    print(collection_name)


    with open(ProQuaColData, 'wb') as f:
        pickle.dump(results, f)


if __name__ == '__main__':
    main()
