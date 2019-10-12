# We import sqlite so that we can use it in python
import sqlite3
import re

# Create connection
import sqlite3 as sq
sl_conn = sq.connect('northwind_small.sqlite3')
sl_conn

# Open up a cursor (cursors allow one to go row by row through the data)
sl_curs = sl_conn.cursor()

# What are the ten most expensive items (per unit price) in the database?
sl_curs.execute("""SELECT(ProductName)
                FROM Product
                ORDER BY UnitPrice DESC LIMIT 10;""")
# Fetchall to display the output of the above
print ('The ten most expensive items (per unit price) in the database ')
l = sl_curs.fetchall()
width = 1
format = ('%%-%ds' % width) * len(l[0])
print ('\n'.join(format % tuple(t) for t in l))
print ('\n')

# What is the average age of an employee at the time of their hiring? (Hint: a
# lot of arithmetic works with dates.)
sl_curs.execute("SELECT AVG(HireDate - BirthDate) FROM Employee;")
# Fetchall to display the output of the above
print ('The average age of an employee at the time of their hiring  = ',
       re.sub('[^A-Za-z0-9]+', ' ', str(sl_curs.fetchall())), '\n')

# How does the average age of employee at hire vary by city?
sl_curs.execute("""SELECT City, AVG(HireDate - BirthDate) AS HireAge
                FROM Employee
                GROUP BY City
                ORDER BY HireAge DESC;""")
print ('How average employee age at the time of their hiring varies by city')
l = sl_curs.fetchall()
width = max(len(e) for t in l for e in t[:-1]) + 1
format = ('%%-%ds' % width) * len(l[0])
print ('\n'.join(format % tuple(t) for t in l))
print ('\n')

# What are the ten most expensive items (per unit price) in the database *and*
# their suppliers?
# Need to join product and supplier tables based upon Id
sl_curs.execute("""SELECT ProductName, CompanyName
                FROM Product
                JOIN Supplier ON Product.SupplierId = Supplier.Id
                ORDER BY UnitPrice DESC LIMIT 10;""")
# Fetchall to display the output of the above
print ('The ten most expensive items in the database and their suppliers')
l = sl_curs.fetchall()
width = max(len(e) for t in l for e in t[:-1]) + 1
format = ('%%-%ds' % width) * len(l[0])
print ('\n'.join(format % tuple(t) for t in l))
print ('\n')

# What is the largest category (by number of unique products in it)?
sl_curs.execute("""SELECT Category.CategoryName,
                COUNT(DISTINCT Product.Id) AS ProductQuantity
                FROM Category, Product
                WHERE Category.Id = Product.CategoryId
                GROUP BY Product.CategoryId
                ORDER BY ProductQuantity DESC LIMIT 1;""")
# Fetchall to display the output of the above
print ('The largest category (by number of unique products in it  = ',
       re.sub('[^A-Za-z0-9]+', ' ', str(sl_curs.fetchall())), '\n')

# Who's the employee with the most territories? Use `TerritoryId`
# (not name, region, or other fields) as the unique identifier for territories.
sl_curs.execute("""SELECT Employee.FirstName, Employee.LastName,
                 COUNT(EmployeeTerritory.TerritoryId) As EmployeeArea
                 FROM Employee, EmployeeTerritory
                 WHERE Employee.Id = EmployeeTerritory.EmployeeId
                 GROUP BY EmployeeTerritory.EmployeeId
                 ORDER BY EmployeeArea DESC LIMIT 1;""")
# Fetchall to display the output of the above
print ('The employee with the most territories  = ',
       re.sub('[^A-Za-z0-9]+', ' ', str(sl_curs.fetchall())), '\n')
