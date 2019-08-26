import requests
import pymongo
import time
from bs4 import BeautifulSoup


def openRequest(num, number, search_query):
    url = ('http://export.arxiv.org/api/query?search_query={2}&start={0}&max_results={1}&sortBy=lastUpdatedDate&sortOrder=descending').format(num,number,search_query)
    data = requests.get(url).text
    bsdata = BeautifulSoup(data, "html.parser")
    return bsdata


def openMongoDB(mongo_url):
    client = pymongo.MongoClient(mongo_url)
    return client.arxiv

def scrapeArxiv(num, number, search_query, mongo_url, wait):

    try:
        if wait < 3:
            raise
    except Exception as error:
        raise Exception("waiting time should be larger than 3 sec")
        return

    try:
        if number > 500:
            raise
    except Exception as error:
        raise Exception("max paper per search is too large")
        return

    while(True):
        data = openRequest(num, number, search_query)

        entry_list = data.find_all('entry')
        if(len(entry_list)==0):
            total_result = data.feed.find('opensearch:totalresults').get_text()
            if int(total_result) <= num:
                break;
            else:
                time.sleep(20)
                continue

        db = openMongoDB(mongo_url)

        
        for item in entry_list:
            arxiv_id = item.id.get_text()
            title = item.title.get_text()
            title = "".join(title.split("\n "))
            author_list = item.find_all('author')
            author = []
            for child in author_list:
                author.append(child.contents[1].contents[0])
            category_list = item.find_all('category')
            category = []
            for child in category_list:
                category.append(child['term'])

            summary = item.summary.get_text()

            updated = item.updated.get_text()

            published = item.published.get_text()


            try:
                post = {'_id': arxiv_id,
                        'title': title,
                        'author': author,
                        'category': category,
                        'summary': summary,
                        'updated': updated,
                        'published': published
                        }

                posts = db.papers
                post_id = posts.insert_one(post).inserted_id

            except:# Exception as err:
                # z = 1
                #print(err)
                num = num + 1
                continue
                # print("Error: Store paper")

            num = num + 1

        # db.logout()
        time.sleep(wait)

def main():

    field = ["stat.AP", "stat.CO", "stat.ML", "stat.ME", "stat.OT", "stat.TH"]

    for category in field:
        scrapeArxiv(0, 500, "cat:{0}".format(category), "mongodb://xxx:xxx@xxx:xxx/arxiv", 3)

if __name__ == "__main__":
    main()
