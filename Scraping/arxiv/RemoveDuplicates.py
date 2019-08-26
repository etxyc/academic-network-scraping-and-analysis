import pymongo

def DuplicatesRemove(collection, result):

    map_unique = {}
    # if cannot find and delete at the same time
    for record in result:
        i = -1
        while record['_id'][i] != 'v':
            i = i - 1
        id = record['_id'][ : i]
        version = int(record['_id'][(i + 1) : ])
        if id not in map_unique.keys():
            map_unique[id] = [version]
        else:
            map_unique[id].append(version)

    for i in map_unique.keys():
        # map_unique[i] = sorted(map_unique[i])
        map_unique[i].sort()
        for j in range(len(map_unique[i]) - 1):
            delete_item = ("{0}v{1}").format(i, map_unique[i][j])
            # print(delete_item)
            collection.delete_one({'_id': delete_item})

def main():
    mongo_url = "mongodb://xxx:xxx@xxx:xxx/arxiv"
    client = pymongo.MongoClient(mongo_url)
    db = client['arxiv']
    collection = db['papers']
    result = collection.find()
    DuplicatesRemove(collection, result)

if __name__ == "__main__":
    main()
