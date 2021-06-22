# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 14:06:56 2021

@author: corber
"""

import pandas as pd
import xml.etree.ElementTree as ET


xmlfile = "D:/uk-parliament-stats/raw-data/uk-plt-xml/debates2015-12-17a.xml"
#remember to only bring in *.xml (exclude 'empty.py' from folder)



xml_data = open(xmlfile, 'r').read()  # Read file
root = ET.XML(xml_data)  # Parse XML



data = []
datatemp =[]
cols = []
for i, child in enumerate(root):
    if child.attrib.get(nospeaker, default=None) == "true": #NOT WORKING ATM -- skip anything not attached to a speaker UNLESS it's a MAJOR HEADING (debate title)
        continue
    else:
        for i, subchild in enumerate(child):
            datatemp.append(subchild.text)
        datatemp = list(filter(None.__ne__, datatemp))
        datatemp = '\n'.join(datatemp)
        data.append(datatemp)
        #grab two attrib - id & person_id for saving as columns
        cols.append(child.attrib)
        datatemp = []

df = pd.DataFrame(data)






# read in XML

# format DF into what I need (col names) - formatting may vary based on lords/answers/commons etc.!!

# run through prep + append functions to add to existing dataset (create df if non-existent)

# move xml to staging folder after processing complete

# clean-up function to delete xml files in staging folder - have this as separate manual step to avoid accidental deletion. Eventually could be built in to be run 1/month?



