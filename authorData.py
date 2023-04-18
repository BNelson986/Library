import json

#   Implementation of Bucketed Hash Table for authorKey lookup
class hashTable:
    def __init__(self) -> None:
        self.size = 12000000
        self.buckets = [[] for _ in range(self.size)]

    def __hash__(self, key: str) -> int:
        return hash(key) % self.size

    def insert(self, key: str, name: str):
        index = self.__hash__(key)
        self.buckets[index].append((key, name))

    def find(self, key: str):
        index = self.__hash__(key)
        bucket = self.buckets[index]

        for k, n in bucket:
            if k == key:
                return n
        return None


#   Used to remove unused data from authors list to reduce run time
def simpleList():
    i = 0
    fileOut = open("authorsSimple.txt", 'a')
    with open("ol_dump_authors_2023-03-31.txt", 'r') as file:
        for author in file:
            line = json.loads(author[author.find('{'):])
            key:str = line['key']
            splitkey = key.split('/')
            #   If no name, skip list
            if 'name' not in line:
                name = 'Unknown'
            else:
               name = line['name']
            fileOut.write(f"{splitkey[2]}/{name}\n") 
            i+=1
            if i % 1000000 == 0:
                print(f"{i} entries copied")   