# Read data
import pandas as pd

df_buddymove_holidayiq = pd.read_csv('buddymove_holidayiq.csv')
df_buddymove_holidayiq.head()

# Create connection
import sqlite3 as sq
conn = sq.connect('buddymove_holidayiq.sqlite3')

# Create review table
try:
    df_buddymove_holidayiq.to_sql('review', conn)
except:
    pass

# Create cursor
curs = conn.cursor()

# Count the number of rows
NOR = curs.execute('SELECT COUNT("User Id") FROM review').fetchall()
print("The number of rows:\n ",\
       ' '.join(map(str, NOR[0])))

# Get the number of users who reviewed at least 100 in the `Nature`category and
# at least 100 in the `Shopping` category
NOU = curs.execute('SELECT COUNT(DISTINCT "User ID") FROM review \
                   WHERE Nature >= 100 AND Shopping >= 100').fetchall()
print("The number of users who reviewed at least 100 in the `Nature`category \
and at least 100 in the `Shopping` category:\n ", ' '.join(map(str, NOU[0])))


# Get the average number of reviews for each category
AIS = curs.execute('SELECT AVG(Sports) FROM review;').fetchall()
print("The number of reviews for Sports:\n ",\
       ' '.join(map(str, AIS[0])))
AIR = curs.execute('SELECT AVG(Religious) FROM review;').fetchall()
print("The number of reviews for Religious:\n ",\
       ' '.join(map(str, AIR[0])))
AIN = curs.execute('SELECT AVG(Nature) FROM review;').fetchall()
print("The number of reviews for Nature:\n ",\
       ' '.join(map(str, AIN[0])))
AIT = curs.execute('SELECT AVG(Theatre) FROM review;').fetchall()
print("The number of reviews for Theater:\n ",\
       ' '.join(map(str, AIT[0])))
AIH = curs.execute('SELECT AVG(Shopping) FROM review;').fetchall()
print("The number of reviews for Shopping:\n ",\
       ' '.join(map(str, AIH[0])))
AIP = curs.execute('SELECT AVG(Picnic) FROM review;').fetchall()
print("The number of reviews for Picnic:\n ",\
       ' '.join(map(str, AIP[0])))
