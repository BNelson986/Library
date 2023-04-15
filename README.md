# Library
Simulated library using MongoDb and python scripts

"loadBooks.py" - Uses a data dump from openLibrary.org (editions) to process data and add specified fields to 
   the 'library' db. *recommend using file "reduceFileSize.py" to reduce the 40+ GB (~44,000,000 entries) of data to 
   usable 500,000 entries*

"customers.py" - Generates fake data for each customer to add to a separate collection within the 'library' db. Currently   set to create 100,000 different customers, each with specific checked out books. 

#WILL BE ADDING FURTHER FUNCTIONALITY TO ACT AS LIBRARIAN TO ADD CUSTOMERS, CHECK IN/OUT BOOKS, ADD BOOKS, ETC.
  
