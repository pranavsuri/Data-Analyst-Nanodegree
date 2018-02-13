#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Use cElementTree or lxml if too slow
import xml.etree.ElementTree as ET

OSM_FILE = "san-francisco_california.osm"
SAMPLE_FILE = "sample.osm"

def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag.
    """
    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()

with open(SAMPLE_FILE, 'wb') as output:
    output.write(bytes('<?xml version="1.0" encoding="UTF-8"?>\n', 'UTF-8'))
    output.write(bytes('<osm>\n  ', 'UTF-8'))

    # Write every 130th top level element
    for i, element in enumerate(get_element(OSM_FILE)):
        if i % 130 == 0:
            output.write(ET.tostring(element, encoding='utf-8'))

    output.write(bytes('</osm>', 'UTF-8'))
