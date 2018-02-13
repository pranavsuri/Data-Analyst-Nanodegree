'''
This code is done as part of Udacity quizes throughout the course.

Before I process the data and add it into a database, I checked the
"k" value for each "<tag>" and see if there are any potential problems.

Udacity lecturer has provided 3 regular expressions to check for certain patterns
in the tags. As we saw in the quiz earlier, we would like to change the data
model and expand the "addr:street" type of keys to a dictionary like this:
{"address": {"street": "Some value"}}
So, we have to see if we have such tags, and if we have any tags with
problematic characters.

I completed the function 'key_type', such that I have a count of each of
four tag categories in a dictionary:
  "lower", for tags that contain only lowercase letters and are valid,
  "lower_colon", for otherwise valid tags with a colon in their names,
  "problemchars", for tags with problematic characters, and
  "other", for other tags that do not fall into the other three categories.
'''

# Initial imports
import xml.etree.cElementTree as ET
import pprint
import re

# Change this with the path of your OSM file
OSMFILE = 'san-francisco_california_sample.osm'

# Regular expressions to catch the patterns in 'k' attribute of tags
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

# Iterate through tag and find patterns that match the regular expressions.
# Add them to a dictionary.
def key_type(element, keys):
    if element.tag == "tag":
        for tag in element.iter('tag'): # Iterating through the tag element in the XML file
            k = element.attrib['k'] # Looking for the tag attribute 'k' which contains the keys
            if re.search(lower, k):
                keys['lower'] += 1
            elif re.search(lower_colon, k):
                keys['lower_colon'] += 1
            elif re.search(problemchars, k):
                keys['problemchars'] += 1
            else:
                keys['other'] += 1
    return keys

def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    pprint.pprint(keys)

# Uncomment the next line to call the function and see the output.
# process_map(OSMFILE)
