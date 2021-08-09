# -*- coding: utf-8 -*-
"""
Created on Mon Aug  9 13:30:13 2021

@author: corber
"""

import re

txtfile = "//NDATA9/corber$/Desktop/debates2015-12-17a.txt"
xmloutput = "//NDATA9/corber$/Desktop/debates2015-12-17a.xml"



#open xml & save as .txt

#input -> provided
#get filename from input path (i.e. strip file type and location)
#output = outputlocation + filename + xml





#open .txt
with open(txtfile) as f:
    lines = f.readlines()

#find/replace
updated_list = []
for line in lines:
    line_updated = re.sub(r'<phrase.*?">', '', line) #delete phrase opening tags
    line_updated = re.sub(r'</phrase>', '', line_updated) #delete phrase closing tag
    updated_list.append(line_updated)
    
#join list into one str
textoutput = "".join(updated_list)

# save as .xml
output = open(xmloutput, "w")
output.write(textoutput) #output has Windows CR LF not Unix LF, is this a problem?


