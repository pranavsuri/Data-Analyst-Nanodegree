"""This code is part of the final project.
After auditing is complete the next step is to prepare the data to be inserted into a SQL database.
To do so, I will parse the elements in the OSM XML file, transforming them from document format to
tabular format, thus making it possible to write to .csv files.  These csv files can then easily be
imported to a SQL database as tables.
"""

# Initial Imports
import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET
from audit import *  #Imports all the functions from audit.py file
import cerberus
import schema

# The directory where the OSM file is located.
OSM_PATH = 'san-francisco_california.osm'

# The directory where the created CSV files will be located
NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

# The SQL schema that is defined in schema.py file.
# Both files need to be in the same directory.
SCHEMA = schema.schema

# Regular expression pattern to find problematic characters in value attributes.
problem_chars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

#Regular expression pattern to find different types of streets in street names.
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

# The list of street types that we want to have.
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square",
            "Lane", "Road", "Trail", "Parkway", "Commons"]

# The list of dictionaries, containing street types
# that need to be changed to match the 'expected' list.
mapping = { "St": "Street", "St.": "Street", "street": "Street",
            "Ave": "Avenue", "Ave.": "Avenue", "AVE": "Avenue,",
            "avenue": "Avenue", "Rd.": "Road", "Rd": "Road", "road": "Road",
            "Blvd": "Boulevard", "Blvd.": "Boulevard", "Blvd,": "Boulevard",
            "boulevard": "Boulevard", "broadway": "Broadway",
            "square": "Square", "square": "Square", "Sq": "Square",
            "way": "Way",
            "Dr.": "Drive", "Dr": "Drive",
            "ct": "Court", "Ct": "Court", "court": "Court",
            "cres": "Crescent", "Cres": "Crescent", "Ctr": "Center",
            "Hwy": "Highway", "hwy": "Highway",
            "Ln": "Lane", "Ln.": "Lane",
            "parkway": "Parkway" }

# The columns in the CSV files. The same columns need to be created for the database.
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']

def shape_element(element):
    """ A function to Shape each element into several data structures.

    Args:
    - param element: 'Node' and'way' tags that are passed to this function from
    the get_element function; mainly called by process_map function.

    The function goes through node and way elements, defining the values for
    nodes, nodes_ways, ways, ways_tags, and ways_nodes dictionaties.

    The "node" field holds a dictionary of the following top level node
    attributes: id, user, uid, version, lat, lon, timestamp, changeset.

    The "ways" fields hold a dictionary of the following top level node
    attributes: id, users, uid, versiob, timestamp, changeset.

    The "node_tags" and "way_tags"field holds a list of dictionaries, one per
    secondary tag. Secondary tags are child tags of node which have the tag
    name/type: "tag". Each dictionary has the following fields from the secondary
    tag attributes:
    - id: the top level node id attribute value
    - key: the full tag "k" attribute value if no colon is present or the
        characters after the colon if one is.
    - value: the tag "v" attribute value
    - type: either the characters before the colon in the tag "k" value
        or "regular" if a colon is not present.
    For the value field, I call updates_name and update_postcode functions to
    clean problematic street names or postcodes. I call these functions on both
    node and way elements.

    Return:
    The following dictionaries will be returned:
    - node
    - node_tags
    - way
    - way_nodes
    - way_tags
    """
    node_attribs = {}   # Handle the attributes in node element
    way_attribs = {}    # Handle the attributes in way element
    way_nodes = []      # Handle the 'nd' tag in the way element
    tags = []           # Handle secondary tags the same way for both node and way elements

    # Handling node elements.
    if element.tag == 'node':
        for item in NODE_FIELDS:
            # If the 'uid' field was empty "9999999" is set as 'uid'.
            try:
                node_attribs[item] = element.attrib[item]
            except:
                node_attribs[item] = "9999999"

        # Iterating through the 'tag' tags in the node element.
        for tg in element.iter('tag'):
            #Ignoring values that contain problematic characters.
            if not problem_chars.search(tg.attrib['k']):
                tag_dict_node = {}
                tag_dict_node['id'] = element.attrib['id']

                # Calling the update_name function to clean up problematic
                # street names based on audit.py file.
                if is_street_name(tg):
                    better_name = update_name(tg.attrib['v'], mapping)
                    tag_dict_node['value'] = better_name

                # Calling the update_postcode function to clean up problematic
                # postcodes based on audit.py file.
                elif get_postcode(tg):
                    better_postcode = update_postcode(tg.attrib['v'])
                    tag_dict_node['value'] = better_postcode

                # For other values that are not street names or postcodes.
                else:
                    tag_dict_node['value'] = tg.attrib['v']

                if ':' not in tg.attrib['k']:
                    tag_dict_node['key'] = tg.attrib['k']
                    tag_dict_node['type'] = 'regular'
                # Dividing words before and after a colon ':'
                else:
                    character_before_colon = re.findall('^[a-zA-Z]*:', tg.attrib['k'])
                    character_after_colon = re.findall(':[a-zA-Z_]+' , tg.attrib['k'])
                    if len(character_after_colon) != 0: #If the key was an empty field
                        tag_dict_node['key'] = character_after_colon[0][1:]
                    else:
                        tag_dict_node['key'] = 'regular'

                    if len(character_before_colon) != 0: #If the type was an empty field
                        tag_dict_node['type'] = character_before_colon[0][: -1]
                    else:
                        tag_dict_node['type'] = 'regular'
                tags.append(tag_dict_node)

        return {'node': node_attribs, 'node_tags': tags}

    # Handling way elements.
    elif element.tag == 'way':
        for item in WAY_FIELDS:
            # If the 'uid' field was empty "9999999" is set as 'uid'.
            try:
                way_attribs[item] = element.attrib[item]
            except:
                way_attribs[item] = "9999999"

        # Iterating through 'tag' tags in way element.
        for tg in element.iter('tag'):
            if not problem_chars.search(tg.attrib['k']):
                tag_dict_way = {}
                tag_dict_way['id'] = element.attrib['id']

                # Calling the update_name function to clean up problematic
                # street names based on audit.py file.
                if is_street_name(tg):
                    better_name_way = update_name(tg.attrib['v'], mapping)
                    tag_dict_way['value'] = better_name_way

                # Calling the update_postcode function to clean up problematic
                # postcodes based on audit.py file.
                if get_postcode(tg):
                    better_postcode_way = update_postcode(tg.attrib['v'])
                    tag_dict_way['value'] = better_postcode_way

                # For other values that are not street names or postcodes.
                else:
                    tag_dict_way['value'] = tg.attrib['v']

                if ':' not in tg.attrib['k']:
                    tag_dict_way['key'] = tg.attrib['k']
                    tag_dict_way['type'] = 'regular'
                #Dividing words before and after a colon ':'
                else:
                    character_before_colon = re.findall('^[a-zA-Z]*:', tg.attrib['k'])
                    character_after_colon = re.findall(':[a-zA-Z_]+', tg.attrib['k'])

                    if len(character_after_colon) == 1:
                        tag_dict_way['key'] = character_after_colon[0][1:]
                    if len(character_after_colon) > 1:
                        tag_dict_way['key'] = character_after_colon[0][1: ] + character_after_colon[1]

                    if len(character_before_colon) != 0: #If the type was an empty field
                        tag_dict_way['type'] = character_before_colon[0][: -1]
                    else:
                        tag_dict_way['type'] = 'regular'

                tags.append(tag_dict_way)

        # Iterating through 'nd' tags in way element.
        count = 0
        for tg in element.iter('nd'):
            tag_dict_nd = {}
            tag_dict_nd['id'] = element.attrib['id']
            tag_dict_nd['node_id'] = tg.attrib['ref']
            tag_dict_nd['position'] = count
            count += 1

            way_nodes.append(tag_dict_nd)

        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}

# Helper functions.
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""
    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()

# Validating that during creation of CSV files the fields are all in accordance with
# the columns that should be in the CSV files.
def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.items())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)

        raise Exception(message_string.format(field, error_string))

class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""
    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, str) else v) for k, v in row.items()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

# Creating CSV Files.
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file, \
         codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
         codecs.open(WAYS_PATH, 'w') as ways_file, \
         codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
         codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        count = 1
        for element in get_element(file_in, tags=('node', 'way')):
            # Setting a counter to show how many rows the code has processed.
            if count % 10000 == 0:
                print (count)
            count += 1
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])

if __name__ == '__main__':
    # Note: If the validation is set to True,
    # the process takes much longer than when it is set to False.
    process_map(OSM_PATH, validate=False)
