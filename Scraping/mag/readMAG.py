import json
import pymongo
from pprint import pprint

"""
a template to retrieve data and store it into mongoDB
*** not all the papers have reference
*** these paper in the microsoft database might have different attribute, some does not contain category
"""
def openMongoDB(mongo_url):
    client = pymongo.MongoClient(mongo_url)
    return client.arxiv


def scrapeLocalDatabase(filename, mongo_url):
    db = openMongoDB(mongo_url)
    with open(filename) as file:
        for line in file:
            temp = line.replace('"id":', '"_id":')
            data = json.loads(temp)

            if("fos" in data):
                print(data)
                posts = db.mag_papers_all
                try:
                    post_id = posts.insert_one(data).inserted_id
                    print("Loading:" + filename)
                    print("Loading:" + filename)
                    print("Loading:" + filename)
                    print("Loading:" + filename)
                    print("Loading:" + filename)
                except Exception as err:
                    print(err)
                    print("Loading:" + filename)
    print("Completed"+ filename)
    db.logout()

def main():
    for i in range(120,167):
        filename = ('/data/dataset/toLoad/mag_papers_{0}.txt').format(i)
        scrapeLocalDatabase(filename, "mongodb://xxx:xxx@xxx:xxx/arxiv")

if __name__ == "__main__":
    main()
