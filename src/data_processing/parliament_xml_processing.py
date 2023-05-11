import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
import os
import re
from datetime import datetime
from lxml import etree

import config

localpath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'xml'))
savepath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'xml'))

verbose = config.verbose

def force_merge_id_structure(df):
    # apply padding to insert 0s & convert to float
    # then remove fullstops & trim any letters

    #identify if speech number needs padding & pad where required
    df["merge_id_padded"] = df['merge_id'].str[-2:]
    df["merge_id_padded"] = df["merge_id_padded"].str.replace("\\.", "", regex = True) #special characters need to be escaped '\\'
    df['merge_id_padded'] = np.where(df['merge_id_padded'].str.len() == 1, df['merge_id_padded'].str.pad(width=2, side='left', fillchar='0'), df['merge_id_padded']) 
   
    #split merge id into list, take all elements except last & then append padded speech number
    df["merge_id_split"] = df["merge_id"].str.split('.')
    df["merge_id_updated"] = df["merge_id_split"].str[:-1] #copy out all elements of list except the last
    df["merge_id_updated"] = df["merge_id_updated"].str.join('.')
    df["merge_id_updated"] = df["merge_id_updated"]+"."+df["merge_id_padded"]
    
    # then remove fullstops, trim any letters & convert to float

    df["merge_id"] = df["merge_id_updated"].str.replace(".", "", regex = False) #remove full stops
    df["merge_id"] = df["merge_id"].str.slice(start=1) #strip away letter at start 
    df["merge_id"] = df["merge_id"].astype(float)
    
    #drop temp vars used in adjusting merge_id to float for pd.merge_asof below
    df = df.drop(['merge_id_padded', 'merge_id_split', 'merge_id_updated'], axis=1)
    
    return df    





def save_to_csv(df):
    filename = os.path.join(savepath,f'xml_processed_id_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')
    df.to_csv(filename)
    return filename

def xml_file_list():
    matches = []
    sections = []
    for root, dirnames, filenames in os.walk(localpath):
        for dirname in dirnames:
            if dirname in config.sections:
                for root, dirnames, filenames in os.walk(os.path.join(localpath,dirname)):
                    for filename in filenames:
                        if filename.endswith(('.xml')):
                            match = re.search(r'\d{4}-\d{2}-\d{2}', filename)
                            if match is not None:
                                date = datetime.strptime(match.group(), '%Y-%m-%d')
                                if datetime.strptime(config.date_start, '%d/%m/%Y') <= date <= datetime.strptime(config.date_end,
                                                                                                                '%d/%m/%Y'):
                                    matches.append(os.path.join(root, filename))
    return matches

def get_all_text(xml_file):
    complete_paragraph_text = []
    tree = etree.parse(xml_file)
    for p in tree.xpath("//speech/p"):
        complete_paragraph_text.append(p.xpath("string()"))
    return complete_paragraph_text

def replace_with_full_text_and_clean(paragraph_text,complete_paragraph_text):
    for i in range(0,len(paragraph_text)):
        if paragraph_text[i] is not None:
            result = list(filter(lambda x: x.startswith(paragraph_text[i]), complete_paragraph_text))
            paragraph_text[i] = re.sub(r'[^A-Za-z0-9$£%.,;\s]+','', result[0])
    return paragraph_text

def parse_file(xmlfile):

    root_node = ET.parse(xmlfile).getroot()

    # get date from file
    match = re.search(r'\d{4}-\d{2}-\d{2}', xmlfile)
    date = datetime.strptime(match.group(), '%Y-%m-%d').strftime('%d/%m/%Y')

    # extract debate info (id & title)
    debate_id = []
    debate_text = []
    for tag in root_node.findall('major-heading'):
        debate_id_temp = tag.get('id')
        debate_text_temp = tag.text.replace('\n','')
        debate_id.append(debate_id_temp)
        debate_text.append(debate_text_temp)
    for tag in root_node.findall('minor-heading'):
        debate_id_temp = tag.get('id')
        debate_text_temp = tag.text.replace('\n','')
        debate_id.append(debate_id_temp)
        debate_text.append(debate_text_temp)

    data_debate = []
    for i in range(0,len(debate_id)):
       rows = [debate_id[i],str(debate_text[i])]
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

    complete_paragraph_text = get_all_text(xmlfile)

    paragraph_text = replace_with_full_text_and_clean(paragraph_text, complete_paragraph_text)

    data_paragraph = []
    for i in range(0,len(paragraph_id)):
       rows = [paragraph_id[i],str(paragraph_text[i])]
       data_paragraph.append(rows)

    ## create dataframes
    df_debate = pd.DataFrame(data_debate, columns = ['debate_id','agenda'])
    df_debate.sort_values('debate_id', inplace=True) #arrange major & minor headings in order in which they occurred
    df_debate["merge_id"] = df_debate["debate_id"].str.split('\d*-\d*-\d*', n=1)  #extract merge id as below for speech
    df_debate["merge_id"] = df_debate["merge_id"].str[1]
    df_debate = force_merge_id_structure(df_debate)


    df_speech = pd.DataFrame(data_speech, columns = ['speech_id','speaker'], dtype='string')
    df_speech["merge_id"] = df_speech["speech_id"].str.split('\d*-\d*-\d*', n=1)
    df_speech["merge_id"] = df_speech["merge_id"].str[1]
    # df_debate["agenda"] = df_debate["agenda"].str.strip() #clean up debate title - remove leading/trailing whitespaces and/or tabs
    df_speech = force_merge_id_structure(df_speech)
    # df_speech["merge_id"] = df_speech["merge_id"].astype('string')
    # df_speech['merge_id'] = df_speech.merge_id.str[0:1] + df_speech.merge_id.str[2:] #remove first fullstop

    df_paragraph = pd.DataFrame(data_paragraph, columns = ['paragraph_id','text'], dtype='string')
    df_paragraph["merge_id"] = df_paragraph["paragraph_id"].str.split('/', n=1)
    df_paragraph["merge_id"] = df_paragraph["merge_id"].str[0].astype('string')
    df_paragraph = force_merge_id_structure(df_paragraph)


    df = df_speech.merge(df_paragraph, on = "merge_id") #combine speech & paragraph dfs
    df.fillna("",inplace=True) #fill None in strings with blank

    df_merged_speech = df.groupby('merge_id')['text'].agg(lambda col: '\n\n'.join(col)) #join speech rows together with 2 newlines

    #join merged speech back into dataset
    df_temp = df.drop(columns=['paragraph_id', 'text']) #remove paragraph_id & speech columns
    df_temp = df_temp.drop_duplicates(subset=["merge_id"]) #drop duplicates on remaining rows - so we have 1 row per speech
    df_full = df_temp.merge(df_merged_speech, on = "merge_id") #join in full speech



    # sort both dataframes by merge_id to facilitate merge
    df_debate.sort_values(by = "merge_id", inplace=True)
    df_full.sort_values(by = "merge_id", inplace=True)
    df_complete = pd.merge_asof(df_full, df_debate, on = "merge_id") #merge debate titles with speech dataframe
    df_complete['date'] = date
    df_complete['section'] = os.path.basename(os.path.dirname(xmlfile))
    df_complete['parliament'] = np.where(df_complete.section == 'debates', 'UK-HouseOfCommons', 'Other')
    return df_complete

def create_dataframe():
    df = pd.DataFrame(columns=['speech_id','speaker','merge_id','text','debate_id','agenda',
                               'merge_id_check','merge_id_test','merge_id_split','testing','date','section','parliament'])
    xml_files = xml_file_list()
    # xml_files = ['D:\\uk-parliament-stats\\data\\xml\\debates\\debates2015-12-17a.xml']
    count = 1
    for xml_file in xml_files:
        if verbose == True:
            print(f"parsing {xml_file} ({count}/{len(xml_files)})")
        df = pd.concat([df,parse_file(xml_file)], axis=0, join='outer')
        count += 1
    return df


def process_xml_files():
    df = create_dataframe()
    df = df.reset_index()
    filename = save_to_csv(df)
    return filename

# lordswms, lordswrans doesn't work as pargraph structure doesnt have merge id in p
# clean-up function to delete xml files in staging folder - have this as separate manual step to avoid accidental deletion. Eventually could be built in to be run 1/month?
# tidy up final output (drop unnecessary vars, sort out var order, remove tab/whitespace from start of debate_text)