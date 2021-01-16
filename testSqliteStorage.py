#!/usr/bin/env python

import sqlite3

conn = sqlite3.connect('/home/himanshu/scripts/example.db')

c = conn.cursor()

c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='stocks' ''')

if c.fetchone()[0] < 1:    
    # Create table
    c.execute('''CREATE TABLE stocks
                ( date text, trans text, symbol text, qty real, price real)''')

# Insert a row of data
c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

c.execute("SELECT MIN(rowid) FROM stocks")
rowid = c.fetchone()[0]
print(rowid)
c.execute("DELETE FROM stocks where rowid =?", (rowid,))

for row in c.execute("SELECT rowid,* FROM stocks"):
    print(row)

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()