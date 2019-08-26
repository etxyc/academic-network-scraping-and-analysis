'''
This file is to create a special database(collection) from the Microsoft Academic Graph database
'''
import pymongo as mg

'''
- db: a particular database object
- old_collection: the collection object from which the information is extracted
- category: string, a particular category you want to find
- collection_name: the name of the new collection
- begin: the beginning year
- end: the ending year
'''
def databaseStore(db, old_collection, category, collection_name, begin, end):
    for year in range(begin, end+1):
        results = old_collection.find({'fos': category, 'year': year, "authors": {'$exists': True, '$ne': None}}, no_cursor_timeout = True)
        for record in results:
            try:
                new_collection = db[collection_name]
                post_id = new_collection.insert_one(record).inserted_id
            except Exception as err:
                print(err)

def main(): #pragma: no cover
    mongo_url = "mongodb://xxx:xxx@xxx:xxx/arxiv"
    client = mg.MongoClient(mongo_url)
    db = client['arxiv']
    old_collection = db['mag_papers_all']
    category = "Statistics"
    collection_name = "statistics"
    begin = 2014
    end = 2016
    databaseStore(db, old_collection, category, collection_name, begin, end)

if __name__ == "__main__":
    main()
