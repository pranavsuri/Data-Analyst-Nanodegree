#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This code is part of the Udacity quizes throughout the course.

The task is to use the iterative parsing to process the map file and
find out not only what tags are there, but also how many, to get the
feeling on how much of which data you can expect to have in the map.
I fill out the count_tags function. It returns a dictionary with the
tag name as the key and number of times this tag can be encountered in
the map as value.
"""

import xml.etree.cElementTree as ET
import pprint

# Change the path with the location of your OSM file
OSMFILE = 'sample.osm'

def count_tags(filename):
    tags= {}
    for event, elem in ET.iterparse(filename):
        if elem.tag not in tags.keys():
            tags[elem.tag] = 1
        else:
            tags[elem.tag] += 1

    pprint.pprint(tags)

count_tags(OSMFILE)
