# We import sqlite so that we can use it in python
import sqlite3
import re

# Create connection
import sqlite3 as sq
sl_conn = sq.connect('demo_data.sqlite3')
sl_conn

# Open up a cursor (cursors allow one to go row by row through the data)
sl_curs = sl_conn.cursor()

sl_curs.execute("CREATE TABLE demo (s VARCHAR(5), x INT, y INT);")

# Input row 1
sl_curs.execute("INSERT INTO demo(s, x, y) VALUES ('g', 3, 9)")

# Input row 2
sl_curs.execute("INSERT INTO demo(s, x, y) VALUES ('v', 5, 7)")

# Input row 3
sl_curs.execute("INSERT INTO demo(s, x, y) VALUES ('f', 8, 7)")

sl_conn.commit()

# We check to make sure that the above worked as expected
sl_curs.execute('SELECT * FROM demo;')

# Fetchall to display the output of the above
print('Contents of the newly created data table')
print(sl_curs.fetchall(), '\n')

# We check the number of rows in the demo table
sl_curs.execute('SELECT COUNT(*) FROM demo;')

# Fetchall to display the output of the above
print ('The number of rows in the newly created data table  = ',
       re.sub('[^A-Za-z0-9]+', '', str(sl_curs.fetchall())), '\n')

# We find the number of rows in the demo table where both x & y are at least 5
sl_curs.execute('SELECT COUNT(*) FROM demo WHERE x >= 5 AND y >= 5;')

# Fetchall to display the output of the above
print('The number of rows in the new data table where x >= 5 & y >= 5: ',
      re.sub('[^A-Za-z0-9]+', '', str(sl_curs.fetchall())), '\n')

# We find the number of unique values of y
sl_curs.execute('SELECT COUNT(DISTINCT y) FROM demo;')

# Fetchall to display the output of the above
print ('The number of unique values of y = ',
       re.sub('[^A-Za-z0-9]+', '', str(sl_curs.fetchall())), '\n')
