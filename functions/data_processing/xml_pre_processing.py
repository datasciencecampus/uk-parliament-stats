# -*- coding: utf-8 -*-
"""
Created on Mon Aug  9 13:30:13 2021

@author: corber
"""

import re

xmlinput = "D:/uk-parliament-stats/raw-data/uk-plt-xml/debates2015-12-17a.xml"
outputlocation = "D:/uk-parliament-stats/raw-data/uk-plt-xml/processed/"


#open xml
with open(xmlinput, "r") as f:
    lines = f.readlines()

#find/replace
updated_list = []
for line in lines:
    line_updated = re.sub(r'<phrase.*?">', '', line) #delete phrase opening tags
    line_updated = re.sub(r'</phrase>', '', line_updated) #delete phrase closing tag
    updated_list.append(line_updated)
    
#join list together into one str
textoutput = "".join(updated_list)


#create output path
filename = re.sub(r'.*?xml/','',xmlinput) #delete path
xmloutput = outputlocation+filename


#save out to new location
with open(xmloutput, "w") as o:
    o.write(textoutput) #output has Windows CR LF not Unix LF, is this a problem? -> might be causing issue with mdash not being inserted?




