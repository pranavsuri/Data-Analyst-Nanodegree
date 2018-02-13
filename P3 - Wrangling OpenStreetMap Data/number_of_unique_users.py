
'''
This code is done as part of Udacity quizes throughout the course.

I find out how many unique users
have contributed to the map in this particular area!

The function process_map returns a set of unique user IDs ("uid")

'''
# Initial imports
import xml.etree.cElementTree as ET
import pprint
import re

# Change this with the path of your OSM file
OSMFILE = 'sample.osm'

# Parsing the OSM and returning the 'uid' for node and way tags
def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        if element.tag == 'node' or element.tag == 'way' or element.tag == 'relation':
                userid = element.attrib['uid']
                users.add(userid)

    print(len(users))

# Uncomment this section to see the output from calling the function
# process_map(OSMFILE)
