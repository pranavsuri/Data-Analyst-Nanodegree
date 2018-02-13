'''This code is part of the final project.
After I have audited and cleaned the data and transfered everything into table
in my database, I can start running queries on it.
'''

import sqlite3
import csv
from pprint import pprint

# Put the path to your sqlite database.
# If no database is available, a new one will be created.
sqlite_file = 'openstreetmap_sf_db.sqlite'

# Connecting to the database.
conn = sqlite3.connect(sqlite_file)
cur = conn.cursor()

# Number of Nodes
def number_of_nodes():
    output = cur.execute('SELECT COUNT(*) FROM nodes')
    return output.fetchone()[0]
print('Number of nodes: \n' , number_of_nodes())

# Number of Ways
def number_of_ways():
    output = cur.execute('SELECT COUNT(*) FROM ways')
    return output.fetchone()[0]
print('Number of ways: \n', number_of_ways())

# Number of Unique Users
def number_of_unique_users():
    output = cur.execute('SELECT COUNT(DISTINCT e.uid) FROM \
                         (SELECT uid FROM nodes UNION ALL SELECT uid FROM ways) e')
    return output.fetchone()[0]
print('Number of unique users: \n' , number_of_unique_users())

# Most Contributing Users
def most_contributing_users():
    output = cur.execute('SELECT e.user, COUNT(*) as num FROM \
                         (SELECT user FROM nodes UNION ALL SELECT user FROM ways) e \
                         GROUP BY e.user \
                         ORDER BY num DESC \
                         LIMIT 10 ')
    print("Most contributing users: \n")
    pprint(output.fetchall())
    return None
print('Most contributing users: \n', most_contributing_users())

# Number of Users Who Contributed Once
def number_of_users_contributed_once():
    output = cur.execute('SELECT COUNT(*) FROM \
                             (SELECT e.user, COUNT(*) as num FROM \
                                 (SELECT user FROM nodes UNION ALL SELECT user FROM ways) e \
                                  GROUP BY e.user \
                                  HAVING num = 1) u')
    return output.fetchone()[0]
print('Number of users who have contributed once: \n', number_of_users_contributed_once())

# Top 10 Cuisines in San Francisco
query = "SELECT value, COUNT(*) as num FROM nodes_tags \
            WHERE key=\"b'amenity'\" \
            GROUP BY value \
            ORDER BY num DESC \
            LIMIT 20"

# Top 10 Amenities in San Francisco
def top_ten_amenities_in_sf():
    output = cur.execute(query)
    pprint(output.fetchall())
    return None

print('Top 10 Amenities:\n')
top_ten_amenities_in_sf()

# Top 10 Cuisines in San Francisco
query = "SELECT value, COUNT(*) as num FROM ways_tags \
            WHERE key=\"b'cuisine'\" \
            GROUP BY value \
            ORDER BY num DESC \
            LIMIT 10"

def cuisines_in_sf():
    output = cur.execute(query)
    pprint(output.fetchall())
    return None

print('Top 10 Cuisines in San Francisco:\n')
cuisines_in_sf()

# Different Types of Shops
query = "SELECT value, COUNT(*) as num FROM nodes_tags \
            WHERE key=\"b'shop'\" \
            GROUP BY value \
            ORDER BY num DESC \
            LIMIT 10"

def shops_in_sf():
    output = cur.execute(query)
    pprint(output.fetchall())
    return None

print('Different types of shops:\n')
shops_in_sf()

# Popular Cafes in San Francisco
def most_popular_cafes():
    output = cur.execute('SELECT nodes_tags.value, COUNT(*) as num \
                          FROM nodes_tags \
                            JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value="coffee_shop") AS cafes \
                            ON nodes_tags.id = cafes.id \
                            WHERE nodes_tags.key="name"\
                            GROUP BY nodes_tags.value \
                            ORDER BY num DESC \
                            LIMIT 10' ) # Remove this limit to see the complete list of postcodes
    pprint(output.fetchall())
    return output.fetchall()

print('Most popular cafes in San Francisco: \n')
most_popular_cafes()
