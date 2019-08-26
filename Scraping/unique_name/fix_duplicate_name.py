"""this file fixed the problem that same person having several several 
different names should be considered as one.This file updates the name in
 mongoDB database according to the method set in match_name.py """


from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
import time
import re
from match_name import get_authors, delete_dup_authors, process

def update_duplicate_name(cat, mongo_url):
    
    """update naming format issue, such as J. Smith to John Smith, 
    where J. Smith and John Smith are actually same name in database"""
    
    client = MongoClient(mongo_url)
    db = client.arxiv
    results = db.cs_IT.find({'category' : re.compile(cat)})
    
    authors = get_authors(cat, mongo_url)
    authors = delete_dup_authors(authors)
    
    count = 1

    for record in results:
        fixed_name = []
        updated = False
        ID = record['_id']

        author_in_one_paper = list(record['author'])
        for child in author_in_one_paper:
        
            child_processed = process(child)

            if (child_processed != child):
                updated = True

            if (child_processed in authors):
                full_name = authors[child_processed]
                updated = True
                child_processed = full_name
            
            fixed_name.append(child_processed)

        if (updated): #if there are some name formating issue, then update database
            db.cs_IT.update({"_id": ID}, {"$set":{"author":fixed_name}})       
 
def main():
     update_duplicate_name("cs.IT", "mongodb://xxx:xxx@xxx:xxx/arxiv")

if __name__ == "__main__":
       main()
