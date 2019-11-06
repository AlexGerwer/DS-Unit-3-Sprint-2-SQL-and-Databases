"""
Set up postres and ElephantSQL connection and cusor
"""
# Install postgres
import os
os.system('pip install psycopg2-binary')
import psycopg2

# Get postgres directory
print ('The postgres directory')
postgres_dir = dir(psycopg2)
h = len(postgres_dir)
for i in range(h):
    print(postgres_dir[i])
print('\n')

# Get postgres help
# help(psycopg2.connect)

# Connect to ElephantSQL
dbname = 'pdunltuz'
user = 'pdunltuz'
password = 'sLRUx7A_cLCsLnmR-IWP4sBGDciKu8wD'
host = 'salt.db.elephantsql.com'
pg_conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
pg_curs = pg_conn.cursor()

"""
Work with SQLite3 connection and cursor with titanic.csv
"""
# Loading Titanic data
import pandas as pd
import io
pd.set_option('display.max_columns', 500)
df_titanic = pd.read_csv('titanic.csv')
print ('titanic.csv first five rows:')
print(df_titanic.head(),'\n')

# Create connection
import sqlite3
sl_conn = sqlite3.connect('titanic.sqlite3')

# Create review table
try:
    df_titanic.to_sql('titanic', sl_conn)
except:
    pass

# Set up SQLite3 cursor
sl_curs = sl_conn.cursor()

# Execute some SQLite3 queries
# Get the number of rows in the charactercreator_character table
NRC = sl_curs.execute('SELECT COUNT(*) FROM titanic').fetchall()
print ('The number of rows in the titanic table =', ' '.join(map(str, NRC[0])), '\n')
# Get the number of distinct names in the charactercreator_character
NCN = sl_curs.execute('SELECT COUNT(DISTINCT name) FROM titanic').fetchall()
print ('The number of distinct names in the titanic table =', ' '.join(map(str, NCN[0])), '\n')
# Get entire characters table
passengers = sl_curs.execute('SELECT * from titanic;').fetchall()
# Print first row of passengers table
print('The first row of the passengers table:')
print(passengers[0])
print('\n')
# Print last row of passengers table
print('The last row of the passengers table:')
print(passengers[-1])
print('\n')
# Print length of passengers table
print('The number of rows in the titanic table =',len(passengers),'\n')

# Get schema of titanic table to get data types in SQLite3
table_schema = sl_curs.execute('PRAGMA table_info(titanic);').fetchall()
print('The schema of titanic table:')
for x in table_schema:
    print(x[0], x[1], x[2], x[3], x[4], x[5])
print('\n')

"""
Working in postgres now, using the schema from above, transform the table
schema/data types for use with progres and ElephantSQL
"""
# Make new empty create_character_table
create_passengers_table = """
  CREATE TABLE passengers(
    index SERIAL PRIMARY KEY,
    Survived INT,
    Pclass INT,
    Name VARCHAR(120),
    Sex VARCHAR(30),
    Age REAL,
    SiblingsSpousesAboard INT,
    ParentsChildrenAboard INT,
    Fare REAL
  );
"""
pg_curs.execute(create_passengers_table)

# Confirm presence of new empty create_character_table table in postgres
# Run table query in postgres as a check
# looking for newly created table…seen in fourth line of output
show_tables = """
SELECT *
FROM pg_catalog.pg_tables
WHERE schemaname != 'pg_catalog'
AND schemaname != 'information_chema';
"""
pg_curs.execute(show_tables)
display_tables = pg_curs.fetchall()
print ('The new set of tables:')
for x in display_tables:
    print(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7])
print('\n')

# Chop off first number (postres does its own indexing) and turn into string
str(passengers[0][1:])

# Construct a way in which to put the first row in the new table
example_insert = """
INSERT INTO passengers(Survived, Pclass, Name, Sex, Age,
                       SiblingsSpousesAboard, ParentsChildrenAboard,
                       Fare)
VALUES """ + str(passengers[0][1:]) + ';'
print(example_insert, '\n')

# Using the code above and a for loop, load the entire new table
for passenger in passengers:
    insert_passenger = f'''
        INSERT INTO passengers(
            Survived, Pclass, Name, Sex, Age,
            SiblingsSpousesAboard, ParentsChildrenAboard,
            Fare
        )
        VALUES (
        {passenger[1]}, {passenger[2]}, '{str(passenger[3]).replace("'", "''")}',
        '{passenger[4]}', {passenger[5]}, {passenger[6]}, {passenger[7]}, {passenger[8]}
        );'''
    pg_curs.execute(insert_passenger)

# Checking to see if the new table loaded properly
pg_curs.execute('SELECT * FROM passengers LIMIT 10;')
new_table_display = pg_curs.fetchall()
print ('Checking the loading of the new table:')
for x in new_table_display:
    print(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8])
print('\n')

# Close the postgres connection and commit the postres cursor
pg_curs.close()
pg_conn.commit()

# Reopen the postgres cursor
pg_curs = pg_conn.cursor()
pg_curs.execute('SELECT * FROM passengers;')
pg_passengers = pg_curs.fetchall()

# Compare the first two rows in both tables
print('The first row of the old table:',passengers[0])
print('The first row of the new table:',pg_passengers[0])

# Compare all rows in both tables
for passenger, pg_passenger in zip(passengers, pg_passengers):
    assert passenger == pg_passenger

# Close the postgres connection and commit the postres cursor
pg_curs.close()
pg_conn.commit()
