# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 14:17:20 2021

@author: corber

"""


# --- Libraries ---
from parlmentions.functions.df_prep import find_ons_mentions
from parlmentions.functions.df_prep import create_date_variables
from parlmentions.functions.df_prep import context_slicer

# --- Variables ---

#parliament speech data
inputfile = "raw-data/commonsdebates_2015_2019-utf8.csv"

#keywords to search for in speeches
keywords = ["ONS","Office for National Statistics", "Office of National Statistics", "UKSA", "UK Statistics Authority", "OSR", "Office for Statistics Regulation", "Office of Statistics Regulation"]


# --- Data Prep ---

# create dataframe
df = find_ons_mentions(inputfile, keywords)


# -- Dates & Week numbering
df = create_date_variables(df)


# -- Extract context around keyword mention

#find character location of key word
df["keyword_location"] = df["text"].str.find("Office for National Statistics")

#create start/stop character locations for extracting context, cap at 0 & max length of str
df["context-start"] = df["keyword_location"]-200
df["context-stop"] = df["keyword_location"]+200

df.loc[df["context-start"] < 0, 'context-start'] = 0
df.loc[df["context-stop"] > df["text"].str.len(), 'context-stop'] = df["text"].str.len()

#slice string based on start/stop values to extract context
df["context"] = df.apply(lambda row: context_slicer(row), axis=1)






    
