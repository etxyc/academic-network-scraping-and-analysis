'''
This file can be used to calculate the frequency of words in the title of papers.

Function writeFrequency(mongo_url, year, category) can be utilised to do thatself.
mongo_url is the url of database, year is the year you want to get frequency,
category is the category you want to choose paper from.
the function generates the corresponding csv file.
'''

import pymongo
import re
import csv


def loadData(mongo_url, category):
    client = pymongo.MongoClient(mongo_url)
    db = client.arxiv
    posts = db.papers
    res = posts.find({'category' : re.compile(category)})
    return res

def splitTitle(res, category, year):
    words = {}
    frequency = {}
    wordFilter = {'for', 'of', 'and', 'in', 'with', 'a', 'the', 'to', 'on', 'from', 'using', 'via', 'an', 'by', 'towards'}

    for record in res:
        if record['category'][0] == category:
            thisYear = record['published'].split('T')[0].split('-')[0]
            thisYear = int(thisYear)
            if thisYear == year:
                words = record['title'].split(' ')
                for word in words:
                    word = word.lower()
                    if word not in wordFilter:
                        if(word in frequency.keys()):
                            frequency[word] += 1
                        else:
                            frequency[word] = 1;
    sortedFreq = sorted(frequency.items(), key=lambda item:item[1], reverse=True)
    return sortedFreq


def writeFrequency(mongo_url, year, category):
    res = loadData(mongo_url, category)
    frequency = splitTitle(res, category, year)
    yearStr = str(year)
    csvName = yearStr + "_" + category + "_" + "Freq" + ".csv"
    with open(csvName, "w") as csvfile:
        writer = csv.writer(csvfile)
        for item in frequency:
            writer.writerow(item)

def main():  # pragma: no cover
    mongo_url =  "mongodb://xxx:xxx@xxx:xxx/arxiv"
    category = "cs.AI"

    years = range(2005, 2019)

    for year in years:
        writeFrequency(mongo_url, year, category)


if __name__ == "__main__":
    main()
