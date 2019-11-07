"""username: admin
password: NgVOFbfdPLigRe67
IP address: 174.81.29.129
"""
# Install postgres
import os
os.system('pip install pymongo')
import pymongo
from pprint import pprint
os.system('sudo service mongodb start')

client = pymongo.MongoClient("mongodb://AlexGerwer:NgVOFbfdPLigRe67@cluster0-shard-00-00-wymel.mongodb.net:27017,cluster0-shard-00-01-wymel.mongodb.net:27017,cluster0-shard-00-02-wymel.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client.test

print('db = client.test')
pprint(db)
print('\n')

# Check how many machines are working
print('The machines incorporated into the cluster')
pprint(client.nodes)
print('\n')

# help(db)

print('The directory of db.test')
print(dir(db.test), '\n')

# help(db.test.insert_one)

# print('The number of documents before any documents have been inserted')
# print(db.test.count_documents({'x':1}), '\n')

# Insert a document
db.test.insert_one({'x':1})

print('The number of documents after a document has been inserted')
pprint(db.test.count_documents({'x':1}))
print('\n')

print('The result of the find_one command')
pprint(db.test.find_one({'x':1}))
print('\n')

print('The result of the find command')
pprint(db.test.find({'x':1}))
print('\n')

# Create a cursor
curs = db.test.find({'x':1})

print('The directory of the cursor')
dir(curs)
pprint(list(curs))
print('\n')

# Create some items
samantha_doc = {
    'favorite animal': ['Kokopo', 'Dog']
}

rosie_doc = {
    'favorite animal': 'Snakes',
    'favorite color': 'Cyan'
}

amer_doc = {
    'favorite animal': 'Red Panda'
}

# Add the items just created
db.test.insert_many([samantha_doc, rosie_doc, amer_doc])

print('The list of newly added items')
pprint(list(db.test.find()))
print('\n')

# Creating more documents
more_docs = []
for i in range(10):
  doc = {'even': i % 2 == 0}
  doc['value'] = i
  more_docs.append(doc)

print ('Viewing additional documents that were made')
pprint(more_docs)
print('\n')

# Adding more documents all at one time
db.test.insert_many(more_docs)

print('Finding items that are labeled even')
pprint(list(db.test.find({'even': False})))
print('\n')

print('Finding items where the favorite animal is Red Panda')
pprint(list(db.test.find({'favorite animal': 'Red Panda'})))
print('\n')

# help(db.test.update_one)

# Make a change to one of the items
db.test.update_one({'value':3},
                   {'$inc': {'value':5}})

print('View the database to see change that was made')
pprint(list(db.test.find()))
print('\n')

# Make a change to multiple items
db.test.update_many({'even':True},
                    {'$inc': {'value':100}})

print('View change made to multiple items')
pprint(list(db.test.find({'even':True})))
print('\n')

# Delete items labeled odd
db.test.delete_many({'even':False})

print('View list after removing odd items')
pprint(list(db.test.find()))
print('\n')

# Create an rpg character
rpg_character = (1, "King Bob", 10, 3, 0, 0, 0)

#Wrap this in a simple dictionary so that the insert_one method works
db.test.insert_one({'rpg_character' : rpg_character})

print('View database after adding an rpg_character')
pprint(list(db.test.find()))
print('\n')

# Add another rpg character
db.test.insert_one({
    'sql_id': rpg_character[0],
    'name': rpg_character[1],
    'hp': rpg_character[2],
    'level': rpg_character[3]
})
