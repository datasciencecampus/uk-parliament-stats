# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 14:06:56 2021

@author: corber
"""

import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET


xmlfile = "D:/uk-parliament-stats/raw-data/uk-plt-xml/debates2015-12-17a.xml"
#remember to only bring in *.xml (exclude 'empty.py' from folder)


def adjust_merge_id_to_float (df):
    #identify if speech number needs padding & pad where required
    df["merge_id_padded"] = df['merge_id'].str[-2:]
    df["merge_id_padded"] = df["merge_id_padded"].str.replace("\\.", "", regex = True) #special characters need to be escaped '\\'
    df['merge_id_padded'] = np.where(df['merge_id_padded'].str.len() == 1, df['merge_id_padded'].str.pad(width=2, side='left', fillchar='0'), df['merge_id_padded']) 
   
    #split merge id into list, take all elements except last & then append padded speech number
    df["merge_id_split"] = df["merge_id"].str.split('.')
    df["merge_id_updated"] = df["merge_id_split"].str[:-1] #copy out all elements of list except the last
    df["merge_id_updated"] = df["merge_id_updated"].str.join('.')
    df["merge_id_updated"] = df["merge_id_updated"]+"."+df["merge_id_padded"]
    
    #take update merge_id and extract just the digits (ignore any letters) so we can turn into a float
    df["merge_id"] = df["merge_id_updated"].str.extract(r'(\d+\D\d+)')
    df["merge_id"] = df["merge_id"].astype(float)
    
    #drop temp vars used in adjusting merge_id to float for pd.merge_asof below
    df = df.drop(['merge_id_padded', 'merge_id_split', 'merge_id_updated'], axis=1)
    return df



root_node = ET.parse(xmlfile).getroot()

# extract debate info (id & title)     
debate_id = []
debate_text = []
for tag in root_node.findall('major-heading'):
    debate_id_temp = tag.get('id')
    debate_text_temp = tag.text
    debate_id.append(debate_id_temp)
    debate_text.append(debate_text_temp)
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


# Create dataframes 

## DEBATE

df_debate = pd.DataFrame(data_debate, columns = ['debate_id','debate_text'])
df_debate.sort_values('debate_id', inplace=True) #arrange major & minor headings in order in which they occurred
    #extract merge id as below for speech
df_debate["merge_id"] = df_debate["debate_id"].str.split('\d*-\d*-\d*', n=1)
df_debate["merge_id"] = df_debate["merge_id"].str[1]
    #clean up debate title - remove leading/trailing whitespaces and/or tabs
df_debate["debate_text"] = df_debate["debate_text"].str.strip()


## SPEECH

df_speech = pd.DataFrame(data_speech, columns = ['speech_id','speaker_name'])
#extract string after end of date (e.g. in dev file - 'a.1677.3')
df_speech["merge_id"] = df_speech["speech_id"].str.split('\d*-\d*-\d*', n=1)
df_speech["merge_id"] = df_speech["merge_id"].str[1]


## PARAGRAPH

df_paragraph = pd.DataFrame(data_paragraph, columns = ['paragraph_id','speech'])
#extract string before '/'
df_paragraph["merge_id"] = df_paragraph["paragraph_id"].str.split('/', n=1)
df_paragraph["merge_id"] = df_paragraph["merge_id"].str[0]



# Merge Dataframes - Speech & Paragraph
df = df_speech.merge(df_paragraph, on = "merge_id")

    #concat speech paragraphs together (so we have 1 row per speech)
df.fillna("",inplace=True) #fill None in strings with blank
df_merged_speech = df.groupby('merge_id')['speech'].agg(lambda col: '\n\n'.join(col)) #join speech rows together with 2 newlines

    #join merged speech back into dataset
df_temp = df.drop(columns=['paragraph_id', 'speech']) #remove paragraph_id & speech columns
df_temp = df_temp.drop_duplicates(subset=["merge_id"]) #drop duplicates on remaining rows - so we have 1 row per speech
df_full = df_temp.merge(df_merged_speech, on = "merge_id") #join in full speech 


# Merge Dataframes - Debate & Speech+Paragraph - match speech to nearest (previous) debate id

    #convert merge_id to float in both dataframes
df_debate = adjust_merge_id_to_float(df_debate)
df_full = adjust_merge_id_to_float(df_full)

    #sort both dataframes by merge_id to facilitate merge
df_debate.sort_values(by = "merge_id", inplace=True)
df_full.sort_values(by = "merge_id", inplace=True)

    #merge debate titles with speech dataframe
df_complete = pd.merge_asof(df_full, df_debate, on = "merge_id")

    #extract date from filename and include this in df


#NEXT: 
    # need to extract date from filename and include this in df too  
    # check final output
    # tidy up final output (drop unnecessary vars, sort out var order)
    # test run on a few more files & do some QA
    # modularise & set up process as outlined in comments below

    





# read in XML

# format DF into what I need (col names) - formatting may vary based on lords/answers/commons etc.!!

# run through prep + append functions to add to existing dataset (create df if non-existent)

# move xml to staging folder after processing complete

# clean-up function to delete xml files in staging folder - have this as separate manual step to avoid accidental deletion. Eventually could be built in to be run 1/month?
