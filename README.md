# Library
Simulated library using MongoDb and python scripts

"loadBooks.py" - Uses a data dump from openLibrary.org (editions) to process data and add specified fields to 
   the 'library' db. *recommend using file "reduceFileSize.py" to reduce the 40+ GB (~44,000,000 entries) of data to 
   usable 75,000 entries*

"authorData.py" - Uses a data dump from openLibrary.org (authors) to generate a local file with only the necessary
   information needed for creation of the 'inventory' collection. Also provides a general outline for a bucketed
   Hash Table to store and quickly access data 

"customers.py" - Generates fake data for each customer to add to a separate collection within the 'library' db.
   Currently set to create 20,000 different customers, each with specific checked out books, and a total cost of 
   books checked out. 

#WILL BE ADDING FURTHER FUNCTIONALITY TO ACT AS LIBRARIAN TO ADD CUSTOMERS, CHECK IN/OUT BOOKS, ADD BOOKS, ETC.
  
