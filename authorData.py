import json


#   Implementation of Bucketed Hash Table for authorKey lookup
class HashTable:
    def __init__(self, size) -> None:
        self.size = size
        self.buckets = [[] for _ in range(self.size)]

    def hash_(self, key: str) -> int:
        return hash(key) % self.size

    def insert(self, key: str, name):
        index = self.hash_(key)
        self.buckets[index].append((key, name))

    def find(self, key: str):
        index = self.hash_(key)
        bucket = self.buckets[index]

        for k, n in bucket:
            if k == key:
                return n
        return None
    
    def is_in_table(self, key:str):
        index = self.hash_(key)
        bucket = self.buckets[index]

        for k in bucket:
            if k == key:
                return True
        return False


#   Used to remove unused data from authors list to reduce run time
def simple_list():
    i = 0
    file_out = open("authorsSimple.txt", 'a')
    with open("ol_dump_authors_2023-03-31.txt", 'r') as file:
        for author in file:
            line = json.loads(author[author.find('{'):])
            key: str = line['key']
            split_key = key.split('/')
            #   If no name, skip list
            if 'name' not in line:
                name = 'Unknown'
            else:
                name = line['name']
            file_out.write(f"{split_key[2]}/{name}\n")
            i += 1
            if i % 1000000 == 0:
                print(f"{i} entries copied")
