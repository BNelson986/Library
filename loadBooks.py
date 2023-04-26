import json
import random
from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor

import authorData


#   Define a function to process each book
def process_book(data):
    # Initialize blank lists for each book
    categories = []
    publishers = []
    title = ""
    author = ""
    isbn13 = ""
    isbn10 = ""

    title = data["title"]

    if "isbn_13" in data:
        isbn13 = data["isbn_13"]
    if "isbn_10" in data:
        isbn10 = data["isbn_10"]
    #   Add author data if it is available
    if "authors" in data:
        author_key: str = data["authors"][0]["key"]
        split_key = author_key.split('/')
        author = authorHash.find(split_key[2])
    #   Add data for publishers if it exists
    if "publishers" in data:
        for publisher in data["publishers"]:
            publishers.append(publisher)
    #   Add categories if they exist
    if "subjects" in data:
        for cat in data["subjects"]:
            categories.append(cat)

    #   Generate random price and initial inventory
    price = f"{random.randint(4, 25)}.99"
    price = float(price)
    inventory = random.randint(10, 50)
    entries.append(
        {
            "isbn_13": isbn13,
            "isbn_10": isbn10,
            "title": title,
            "author": author,
            "publishers": publishers,
            "categories": categories,
            "price": price,
            "inventory": inventory,
        })

    if len(entries) % 5000 == 0:
        completion += 6.67
        print(f"{completion}% finished")

def hash_authors(author: list):
    key = author[0]
    name = author[1]

    authorHash.insert(key, name)


#   Initialize local mongodb connection
client = MongoClient(host='localhost', port=27017)

#   Access 'library' database
db = client['library']

#   Access 'inventory' collection
collection = db['inventory']

entries = []

#   Store authors data for multithreading
authors = []

authorHash = authorData.HashTable(75000000)

#   Read all lines of authors
print("Start storing")
with open("authorsSimple.txt", 'r') as file:
    for author in file:
        line: str = author.replace('\n', '')
        line = line.split('/')
        if len(line) > 1:
            name = line[1].replace('\n', '')
            key = line[0]
        else:
            continue
        authors.append((key, name))
print("Finished storing")

print("Start hashing")
with ThreadPoolExecutor(max_workers=8) as executor:
    future_entry = {executor.submit(hash_authors, author): author for author in authors}
print("Finished hashing")

print("Start book processing")
# Load book data from file
with open('shortListNew.txt', 'r') as file:
    books = [json.loads(line[line.find('{'):]) for line in file]

with ThreadPoolExecutor(max_workers=8) as executor:
    future_entry = {executor.submit(process_book, book): book for book in books}
print("Finished book processing")

insertion = collection.insert_many(entries)
