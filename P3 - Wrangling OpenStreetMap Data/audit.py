import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "san-francisco_california.osm"

"""This regular expression matches letters without any white space with zero to one '.'
Extract a string which might or might not have the '.' character in it."""
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

# List of expected street types.
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square",
            "Lane", "Road", "Trail", "Parkway", "Commons"]

def audit_street_type(street_types, street_name):
    """This function will get the list of street types and using the regular expression,
    compare them to the expected list. If they do not match the names in the expected list,
    it adds it to the street_types dictionary.

	Args:
	- street_types: list of dictionaries containing different street types.
		The key in the dictionary is the type of street (e.g. avenue, street),
		and the values are names of streets (e.g. Park avenue, 5th street).

	- street_name: name of the street (i.e. tag.attrib['v']). This name is
		passed to this function from the audit_name function.
	"""
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def is_street_name(elem):
    """This unction will get the elements in the file (i.e. the tag element) and
    return the attributes in that element for which their key is equal to 'addr:street'.
    """
    return (elem.attrib['k'] == "addr:street")

def audit_street(osmfile):
    """This function uses iterative parsing to go through the XML file,
    parse node and way elements, and iterate through their tag element.
    It will then call the 'audit_street_type' function to add the value attribute
    of the tag (i.e. the street name) to it.

    Arg:
	- osmfile: reads the OpenStreetMap data

	Return:
	- returns the list of dictionaries containing list of street types with their
	corresponding street name.
    """
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)

    # Parses the XML file.
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        # Iterate through the 'tag' element of node and way elements.
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types

street_types = audit_street(OSMFILE)
pprint.pprint(dict(street_types))

# The list of dictionaries, containing street types that need to be changed
# to match the expected list.
mapping = { "St": "Street",
            "St.": "Street",
            "street": "Street",
            "Ave": "Avenue",
            "Ave.": "Avenue",
            "AVE": "Avenue,",
            "avenue": "Avenue",
            "Rd.": "Road",
            "Rd": "Road",
            "road": "Road",
            "Blvd": "Boulevard",
            "Blvd.": "Boulevard",
            "Blvd,": "Boulevard",
            "boulevard": "Boulevard",
            "broadway": "Broadway",
            "square": "Square",
            "way": "Way",
            "Dr.": "Drive",
            "Dr": "Drive",
            "ct": "Court",
            "Ct": "Court",
            "court": "Court",
            "Sq": "Square",
            "square": "Square",
            "cres": "Crescent",
            "Cres": "Crescent",
            "Ctr": "Center",
            "Hwy": "Highway",
            "hwy": "Highway",
            "Ln": "Lane",
            "Ln.": "Lane",
            "parkway": "Parkway"
            }

def update_name(name, mapping):
    """This function takes the street name and split it at the space character.
    In case, it finds a string that matches any key in the mapping, it replaces it with
    the format that has been specified for it.

    e.g. When the function finds 'Blvd' in "Newark Blvd", it goes through mapping and maps
    it to 'Boulevard', and the final street name will come out as 'Newark Boulevard'.

    Args:
	-name: The street name coming from tag.attrib['v'] attribute. This
		parameter is defined in shape_element function from shaping_csv.py file.

	-mapping: Is the list of mapping created while auditing the street names
		in audit_street_type function

	Return:
	- output: The list of corrected street names.

        Example 5th street is separated
		to '5th' and 'street', and each is compared to mapping. For 'street' the
		mapping expects it to change to 'Street'. Function changes it to 'Street'
		and adds '5th Street' to the output list.
    """
    output = list()
    parts = name.split(" ")
    for part in parts:
        if part in mapping:
            output.append(mapping[part])
        else:
            output.append(part)
    return " ".join(output)

# Printing the changes made in street names.
for st_type, ways in street_types.items():
        for name in ways:
            better_name = update_name(name, mapping)
            print(name, "→", better_name)

OSMFILE = 'sample.osm'

def dicti(data, item):
    """This function creates a dictionary postcodes can be held.
    The dictionary key will be the postcode itself and the dictionary value
    will be the number of times that postcode was repeated throughout the map."""
    data[item] += 1

def get_postcode(elem):
    """This function takes the 'tag' element as an input and
    return the elements for which the keys are equal to 'addr:postcode'"""
    return (elem.attrib['k'] == "addr:postcode")

def audit(osmfile):
    """This function parses the XML file and iterates through node and
    way elements. It extracts the value attribute (i.e. the postcode) and
    add it to the 'dicti' dictionary.

	Arg:
	- osmfile: reads the OpenStreetMap data

	Return:
	- data: a dictionary containing postcodes and the number of times they have been
	repeated throughout the data. (Example: {'94122', '94122', '94122', '94611'} will
	give dicti{['94122']=3, ['94611']=1}.
    """
    osm_file = open(osmfile, "r")
    data = defaultdict(int)
    # Parsing the XML file
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        # Iterating through node and way elements.
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if get_postcode(tag):
                    dicti(data, tag.attrib['v'])
    return data

postcodes = audit(OSMFILE)
pprint.pprint(dict(postcodes))

def update_postcode(digit):
    """Makes use of different conditions in the function to match the
    postcodes in the 3 categories that can be found for postal codes.

    Arg:
	- digit: The postcode coming from tag.attrib['v'] attribute. This
	parameter is defined in shape_element function from shaping_csv.py file.

	Return:
	- Output: Return a list of corrected postcodes
    """
    output = list()

    first_category = re.compile(r'^\D*(\d{5}$)', re.IGNORECASE)
    second_category = re.compile('^(\d{5})-\d{4}$')
    third_category = re.compile('^\d{6}$')

    if re.search(first_category, digit):
        new_digit = re.search(first_category, digit).group(1)
        output.append(new_digit)

    elif re.search(second_category, digit):
        new_digit = re.search(second_category, digit).group(1)
        output.append(new_digit)

    elif re.search(third_category, digit):
        third_output = third_category.search(digit)
        new_digit = '00000'
        output.append('00000')

    # This condition matches the third category for any other types.
    elif digit == 'CA' or len(digit) < 5:
        new_digit = '00000'
        output.append(new_digit)

    return ', '.join(str(x) for x in output)

for postcode, nums in postcodes.items():
    better_code = update_postcode(postcode)
    print(postcode, "→", better_code)
