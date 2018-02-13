'''This code is part of the final project.
It creats SQL tables for nodes_tags, ways, ways_nodes, ways_tags and nodes.
'''

import sqlite3
import csv
from pprint import pprint

# Put the path to your sqlite database.
# If no database is available, a new one will be created.
sqlite_file = 'openstreetmap_sf_db.sqlite'

# Connecting to the database
conn = sqlite3.connect(sqlite_file)
cur = conn.cursor()

# Making sure a table that already exists does not get created.
cur.execute('DROP TABLE IF EXISTS nodes')
conn.commit()

# Creating the nodes_tags table.
cur.execute('''
    CREATE TABLE nodes_tags(id INTEGER, key TEXT, value TEXT, type TEXT)
''')
conn.commit()

with open('nodes_tags.csv', 'r') as f:
    dr = csv.DictReader(f)
    in_db = [(i["b'id'"], i["b'key'"], i["b'value'"], i["b'type'"]) for i in dr]

# Insert the data.
cur.executemany('INSERT INTO nodes_tags(id, key, value, type) VALUES(?, ?, ?, ?);', in_db)
conn.commit()

# Creating the ways table.
cur.execute('''
    CREATE TABLE ways(id VARCHAR PRIMARY KEY, user TEXT, uid INTEGER, \
    version VARCHAR, changeset INTEGER, timestamp DATETIME)
''')
conn.commit()

with open('ways.csv', 'r') as f:
    dr = csv.DictReader(f)
    in_db = [(i["b'id'"], i["b'user'"], i["b'uid'"], i["b'version'"], \
    i["b'changeset'"], i["b'timestamp'"]) for i in dr]

# Insert the data.
cur.executemany('INSERT INTO ways(id, user, uid, version, changeset, timestamp) VALUES(?, ?, ?, ?, ?, ?);', in_db)
conn.commit()

# Creating the ways_nodes table.
cur.execute('''
    CREATE TABLE ways_nodes(id INTEGER, node_id INTEGER, position INTEGER)
''')
conn.commit()

with open('ways_nodes.csv', 'r') as f:
    dr = csv.DictReader(f)
    in_db = [(i["b'id'"], i["b'node_id'"], i["b'position'"]) for i in dr]

# Insert the data.
cur.executemany('INSERT INTO ways_nodes(id, node_id, position) VALUES(?, ?, ?);', in_db)
conn.commit()

# Creating the ways_tags table.
cur.execute('''
    CREATE TABLE ways_tags(id INTEGER , key TEXT, value TEXT, type TEXT)
''')
conn.commit()

with open('ways_tags.csv', 'r') as f:
    dr = csv.DictReader(f)
    in_db = [(i["b'id'"], i["b'key'"], i["b'value'"], i["b'type'"]) for i in dr]

# Insert the data
cur.executemany('INSERT INTO ways_tags(id, key, value, type) VALUES(?, ?, ?, ?);', in_db)
conn.commit()

# Creating the nodes table.
cur.execute('''
            CREATE TABLE IF NOT EXISTS nodes(id VARCHAR PRIMARY KEY, lat REAL,
            lon REAL, user TEXT, uid INTEGER, version TEXT, changeset INTEGER, timestamp DATE)
        ''')
conn.commit()

with open('nodes.csv', 'r') as f:
    dr = csv.DictReader(f)
    in_db = [(i["b'id'"], i["b'lat'"], i["b'lon'"], i["b'user'"], \
            i["b'uid'"], i["b'version'"], i["b'changeset'"], i["b'timestamp'"]) for i in dr]

# Insert the data.
cur.executemany("INSERT INTO nodes(id, lat, lon, user, uid, version, changeset, timestamp) \
                VALUES (?, ?, ?, ?,?, ?, ?, ?);", in_db)
conn.commit()
