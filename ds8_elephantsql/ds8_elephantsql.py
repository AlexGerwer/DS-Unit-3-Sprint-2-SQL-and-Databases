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
Work with SQLite3 connection and cursor with rpg_db.sqlite3
"""

# Set up SQLite3 connection and cursor
import sqlite3
sl_conn = sqlite3.connect('rpg_db.sqlite3')
sl_curs = sl_conn.cursor()

# Execute some SQLite3 queries
# Get the number of rows in the charactercreator_character table
NRC = sl_curs.execute('SELECT COUNT(*) FROM charactercreator_character').fetchall()
print ('The number of rows in the charactercreator_character table =', ' '.join(map(str, NRC[0])), '\n')
# Get the number of distinct names in the charactercreator_character
NCN = sl_curs.execute('SELECT COUNT(DISTINCT name) FROM charactercreator_character').fetchall()
print ('The number of distinct names in the charactercreator_character table =', ' '.join(map(str, NCN[0])), '\n')
# Get entire characters table
characters = sl_curs.execute('SELECT * from charactercreator_character;').fetchall()
# Print first row of characters table
print('The first row of the characters table:')
print(characters[0])
print('\n')
# Print last row of characters table
print('The last row of the characters table:')
print(characters[-1])
print('\n')
# Print length of characters table
print('The number of rows in the charactercreator_character table =',len(characters),'\n')

# Get schema of charactercreator_character table to get data types in SQLite3
table_schema = sl_curs.execute('PRAGMA table_info(charactercreator_character);').fetchall()
print('The schema of charactercreator_character table:')
for x in table_schema:
    print(x[0], x[1], x[2], x[3], x[4], x[5])
print('\n')

"""
Working in postgres now, using the schema from above, transform the table
schema/data types for use with progres and ElephantSQL
"""
# Make new empty create_character_table
create_character_table = """
  CREATE TABLE charactercreator_character (
    character_id SERIAL PRIMARY KEY,
    name VARCHAR(30),
    level INT,
    exp INT,
    hp INT,
    strength INT,
    intelligence INT,
    dexterity INT,
    wisdom INT
  );
"""
pg_curs.execute(create_character_table)

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
str(characters[0][1:])

# Construct a way in which to put the first row in the new table
example_insert = """
INSERT INTO charactercreator_character
(name, level, exp, hp, strength, intelligence, dexterity, wisdom)
VALUES """ + str(characters[0][1:]) + ';'
print(example_insert, '\n')

# Using the code above and a for loop, load the entire new table
for character in characters:
  insert_character = """
    INSERT INTO charactercreator_character
    (name, level, exp, hp, strength, intelligence, dexterity, wisdom)
    VALUES """ + str(character[1:]) + ';'
  pg_curs.execute(insert_character)

# Checking to see if the new table loaded properly
pg_curs.execute('SELECT * FROM charactercreator_character;')
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
pg_curs.execute('SELECT * FROM charactercreator_character;')
pg_characters = pg_curs.fetchall()

# Compare the first two rows in both tables
print('The first row of the old table:',characters[0])
print('The first row of the new table:',pg_characters[0])

# Compare all rows in both tables
for character, pg_character in zip(characters, pg_characters):
  assert character == pg_character

# Close the postgres connection and commit the postres cursor
pg_curs.close()
pg_conn.commit()
