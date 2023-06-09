from faker import Faker
import faker.providers.address.en
import random
import uszipcode
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import time
import bson

import authorData

from pymongo import MongoClient


'''
    EACH CUSTOMER WILL HAVE THE FOLLOWING:
    -   NAME
    -   EMAIL
    -   ADDRESS
    -   CHECKED BOOKS
'''

def make_address():
    #   Address broken down into:
    #   Street Address
    #   City
    #   State
    #   Zipcode    
    #   Prep search engine

    #   Check cache before calling to API
    street_address = faker.street_address()
    result = random.choice(list(keys))

    if result:
        place = zipCache.find(result)
        city = place[0]
        state = place[1]
        address = {'street': street_address, 'city': city, 'state': state, 'zipcode': result}
        return address
    else:
        make_address()


'''
    RULES FOR CHECKED BOOKS:
    -   Max of 5 checked books per customer
    -   Limit of 2 copies of each book per customer

    PROCESS TO GENERATE CHECKED BOOKS:
    -   Randomly generate index from list of books 
'''


#   Used to generate the checked out books, update inventory, and create total cost per order
def makeOrder(inventory, count, usedBooks):
    cost = float()
    isbnList = list()

    #   Generate random number of books to check out
    num_books = random.randint(1, min(5, count))

    #   Gather random sample of num_books from inventory
    selected_books = random.sample(inventory, num_books)

    #   Loop through selected_books and process
    for book in selected_books:
        if book['inventory'] == 0:
            continue
        qty = random.randint(1, min(2, book['inventory']))
        if book['_id'] in usedBooks:
            usedBooks[book['_id']] += qty
        else:
            usedBooks[book['_id']] = qty
            
        book['inventory'] -= qty
        cost += book['price'] * qty
        isbnList.append(str(book['isbn_13'] or book['isbn_10']))

    order_individual = {'isbn': isbnList}
    orders_dict = {'books': order_individual, 'cost': round(cost, 2)}

    return orders_dict

#   Used to generate customer data and append to global list for insertion to dB
def create_customer(inventory, objectCount):
    first = faker.first_name()
    last = faker.last_name()

    name = first + " " + last
    email = first[:2] + "." + last + "@" + faker.free_email_domain()

    address = make_address()

    order = makeOrder(inventory, objectCount, usedBooks)

    customer = {'name': name, 'email': email, 'address': address, 'order': order}

    return customer


#   Initialize local mongodb connection
client = MongoClient(host='localhost', port=27017)

#   Access 'library' database
db = client['library']

#   Create and access collections
customerCollection = db['customers']
inventoryCollection = db['inventory']

faker = Faker()
search = uszipcode.SearchEngine()

#   Gather all data from 'inventory' collection
inventory = inventoryCollection.find({}, {'_id': 1, 'price': 1, 'inventory': 1, 'isbn_10': 1, 'isbn_13': 1})
inventory = sorted(inventory, key=lambda item: item['_id'])

#   Get count of documents for indexing operations
objectCount = inventoryCollection.count_documents(filter={})

#   Create set of customers to enable single DB connection on insertion
customers = list()

futures = []

usedBooks = {}

#   Cache to store retrieved zipcodes
zipCache = authorData.HashTable(700)
keys = set()

print("start")
st = time.time()

for i in range(100):
    zip = faker.zipcode_in_state('CA')

    if zip in keys:
        # If the result is already in the cache, decrement i to keep 100 zips
        i -= 1
    else:
        # If the result is not in the cache, query the search engine
        result = search.by_zipcode(zip)
        if not result:
            i -= 1
            continue
        place = [result.city, result.state]
        # Store the result in the cache
        zipCache.insert(zip, place)
        keys.add(zip)

perCompl = 0

with ThreadPoolExecutor(max_workers=8) as executor:
    #   Generate random number of orders for each person
    for i in range(20000):
        future = executor.submit(create_customer, inventory, objectCount)
        futures.append(future)
    #   Collect all results from the futures
    for i, future in enumerate(as_completed(futures)):
        customers.append(future.result())
        if (i + 1) % 2000 == 0:
            perCompl += 10
            print(f"{perCompl}% completed")

et = time.time()

print("Runtime:" + str(et-st))

print("Entry time:" + str((et-st)/20000))

book_ids = list(usedBooks.keys())
book_qtys = list(usedBooks.values())

inventoryCollection.update_many({'_id': {'$in': book_ids}}, {'$inc': {'inventory': -1 * bson.Int64(qty) for qty in book_qtys}})

result = customerCollection.insert_many(customers)
