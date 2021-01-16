#!/usr/bin/env python

import sqlite3

conn = sqlite3.connect('/fw/sqlite/payload.db')

c = conn.cursor()

c.execute(''' DELETE FROM backlog ''')

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()