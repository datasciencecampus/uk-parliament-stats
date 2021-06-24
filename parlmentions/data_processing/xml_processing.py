# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 14:06:56 2021

@author: corber
"""

import pandas as pd
import xml.etree.ElementTree as ET


xmlfile = "D:/uk-parliament-stats/raw-data/uk-plt-xml/debates2015-12-17a.xml"
#remember to only bring in *.xml (exclude 'empty.py' from folder)


root_node = ET.parse(xmlfile).getroot()

# extract debate info (id & title)     
debate_id = []
debate_text = []
for tag in root_node.findall('minor-heading'):
    debate_id_temp = tag.get('id')
    debate_text_temp = tag.text
    debate_id.append(debate_id_temp)
    debate_text.append(debate_text_temp)

data_debate = []
for i in range(0,len(debate_id)):
   rows = [debate_id[i],debate_text[i]]
   data_debate.append(rows)

# extract speakername & speech id
speech_id = []
speaker_name = []
for tag in root_node.findall('speech'):
    speech_id_temp = tag.get('id')
    speaker_name_temp = tag.get('speakername')
    speech_id.append(speech_id_temp)
    speaker_name.append(speaker_name_temp)

data_speech = []
for i in range(0,len(speech_id)):
   rows = [speech_id[i],speaker_name[i]]
   data_speech.append(rows)

# extract speech/paragraph info (id & text of paragraph)
paragraph_id = []
paragraph_text = []
for tag in root_node.findall('speech/p'):
    paragraph_id_temp = tag.get('pid')
    paragraph_text_temp = tag.text
    paragraph_id.append(paragraph_id_temp)
    paragraph_text.append(paragraph_text_temp)

data_paragraph = []
for i in range(0,len(paragraph_id)):
   rows = [paragraph_id[i],paragraph_text[i]]
   data_paragraph.append(rows)

##need to extract date from filename and include this in df too  
   

# create dataframes 
df_debate = pd.DataFrame(data_debate, columns = ['debate_id','debate_text'])
print(df_debate)
df_debate.dtypes

df_speech = pd.DataFrame(data_speech, columns = ['speech_id','speaker_name'])
print(df_speech)
df_speech.dtypes


df_paragraph = pd.DataFrame(data_paragraph, columns = ['paragraph_id','speech'])
print(df_paragraph)
df_paragraph.dtypes
    





# read in XML

# format DF into what I need (col names) - formatting may vary based on lords/answers/commons etc.!!

# run through prep + append functions to add to existing dataset (create df if non-existent)

# move xml to staging folder after processing complete

# clean-up function to delete xml files in staging folder - have this as separate manual step to avoid accidental deletion. Eventually could be built in to be run 1/month?



