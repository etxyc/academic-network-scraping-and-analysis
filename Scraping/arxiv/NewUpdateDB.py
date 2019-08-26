import requests
import pymongo
import time
from bs4 import BeautifulSoup

def UpdateDB(collection, search_query, update_time):
    num = 0
    number = 500
    wait = 3
    end = False
    while(not end):
        url = ('http://export.arxiv.org/api/query?search_query={2}&start={0}&max_results={1}&sortBy=lastUpdatedDate&sortOrder=descending').format(num, number, search_query)
        data = requests.get(url).text
        data = BeautifulSoup(data,"html.parser")
        entry_list = data.find_all('entry')
        if(len(entry_list) == 0):
            time.sleep(20)
            continue

        for item in entry_list:
            arxiv_id = item.id.get_text()
            # print(arxiv_id)
            title = item.title.get_text()
            title = "".join(title.split("\n "))
            # print(title)
            author_list = item.find_all('author')
            author=[]
            for child in author_list:
                author.append(child.contents[1].contents[0])
            # print(author)
            category_list = item.find_all('category')
            category = []
            for child in category_list:
                category.append(child['term'])
            # print(category)
            summary = item.summary.get_text()
            # print(summary)
            updated = item.updated.get_text()
            # print(updated)
            published = item.published.get_text()
            # print(published)
            post = {'_id': arxiv_id,
                    'title': title,
                    'author': author,
                    'category': category,
                    'summary': summary,
                    'updated': updated,
                    'published': published
            }
            # print(post)
            # print(search_query)
            try:
                # when the updated is new
                if(updated >= update_time):
                    post_id = collection.insert_one(post).inserted_id
                else:
                    end = True
            except Exception as err:
                print(err)
                # print("Error: store paper")
            num = num + 1

        time.sleep(wait)

def main():
    mongo_url = "mongodb://xxx:xxx@xxx:xxx/arxiv"
    client = pymongo.MongoClient(mongo_url)
    db = client['arxiv']
    collection = db['papers']
    update_time = "2018-05-08"
    # field = ["astro-ph.GA", "astro-ph.CO", "astro-ph.EP", "astro-ph.HE", "astro-ph.IM", "astro-ph.SR"] # astrophysics
    field = ["stat.AP", "stat.CO", "stat.ML", "stat.ME", "stat.OT", "stat.TH"] # statistics
    # field = ["cs.AI", "cs.CL", "cs.CC", "cs.CE", "cs.CG", "cs.GT", "cs.CV", "cs.CY", "cs.CR", "cs.DS", "cs.DB", "cs.DL", "cs.DM", "cs.DC", "cs.ET", "cs.FL", "cs.GL", "cs.GR", "cs.AR", "cs.HC", "cs.IR", "cs.IT", "cs.LG", "cs.LO", "cs.MS", "cs.MA", "cs.MM", "cs.NI", "cs.NE", "cs.NA", "cs.OS", "cs.OH", "cs.PF", "cs.PL", "cs.RO", "cs.SI", "cs.SE", "cs.SD", "cs.SC", "cs.SY"] # computer science
    for category in field:
        search_query = "cat:{0}".format(category) # cat: category
        UpdateDB(collection, search_query, update_time)
    # db.logout()

if __name__ == "__main__":
    main()
