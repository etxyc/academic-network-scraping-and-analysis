"""this file is to find out the string matching the names of same 
person used in arxiv. Three types of string matchng is conducted
1. name matching non-english characters, Jôhn Smith and John Smith
2. name matching with and without duplicate name(three words), John Smith and John M. Smith
3. name matching using first name initial, such as John Smith and J. Smith"""


from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
import time
import re

def translate_name(person):
    #replace non-english character to english character
    translationTable = str.maketrans("ğěýÇäéàèùâêîôûçíòáöžİŞłąóşøüúńÖãřÁšćëñ", "gěýCaeaeuaeioucioaozISlaosouunOarAscen") 
    person = person.translate(translationTable)
    return str(person)

def find_duplicate_name(name,match_name):
    #match name == J. Smith with match_name == John Smith
    if(len(match_name.split()) != 2):
        return False
    name_initial = match_name.split()[0][0]+". "+match_name.split()[1]
    if(name == name_initial):
        return True
    return False

def replace_non_english_char(name):
    return translate_name(name)

def process(name):
    
    """remove middle name and non-English character
    assume John M smith, John M. smith, John Middle smith is same person"""
    
    name = translate_name(name)
    R = re.compile(r"(\b(\w+)\s(\w+\.)\s(\w+))\b")
    R2 = re.compile(r"(\b(\w+)\s(\w+)\s(\w+))\b")
    name_split = name.split()
    if(len(name.split()) == 3):
        if(R.match(name) or R2.match(name)):
            name_no_mid = name_split[0] + " " + name_split[2]
            return(name_no_mid)
    return(name)

def get_authors(cat, mongo_url):
    
    """return a dictionary with {"authors" : count}
    authors middle name has been removed """
    
    client = MongoClient(mongo_url)
    db = client.arxiv
    results = db.cs_IT.find({'category' : re.compile(cat)})
    error_count = 0
    total_count = 0
   
    authors = {}
    for record in results:
        authors_in_one_paper = list(record['author'])
        for author in authors_in_one_paper:
            author = process(author)
      
            if (author not in authors):
                authors[author] = 1
            else:
                authors[author]=authors[author]
                
    return authors
     
def delete_dup_authors(authors):
    
    """return a dictionary of format {J. Smith: John Smith}, 
    where J. Smith and John Smith actually same name"""
    
    count = 0
    count_duplicate = 0
    total_count = 0
    author_delete = []
    author_dup = {}
    for name in authors:
        if(len(name.split()) == 2):
            same_lastName = 0
            total_count = total_count + 1
            if(re.compile(r"(\b(\w\.)\s(\w+))\b").match(name)):
                count = count + 1
                for name_match in authors:
                    if (name_match != name and find_duplicate_name(name, name_match)):
                        same_lastName = same_lastName + 1
                        count_duplicate = count_duplicate + 1
                        name_stored = name_match
                # if there are more than two people having the same initial and last name, then dont deal with it
                #if (this is the type that people have the same initial and last name)
                if (same_lastName == 1):
                    #update the authors dictionary, delete the duplicate name
                    authors[name] = authors[name_stored] + authors[name]
                    author_delete.append(name_stored)
                    author_dup[name] = name_stored  #e.g. {J. smith: John smith}

    return author_dup

def main():
     authors = get_authors("cs.IT", "mongodb://xxx:xxx@xxx:xxx/arxiv")
     authors = delete_dup_authors(authors)


if __name__ == "__main__":
       main()
