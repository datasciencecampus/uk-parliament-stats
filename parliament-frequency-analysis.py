# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 14:17:20 2021

@author: corber
"""

#libraries
import pandas as pd


#variables
inputfile = "D:/uk-parliament-data/commonsdebates_2015_2019-utf8.csv"
keywords = ["ONS","Office for National Statistics", "Office of National Statistics", "UKSA", "UK Statistics Authority"]

#analysis
df = pd.read_csv(inputfile)

#group keywords together, use '|' to separate and allow str.contains function to parse as logical OR
keywords_combined = '|'.join(keywords)

#create T/F flag in 'match' for any speeches that contain keywords, NOT case sensitive.
df["match"] = df["text"].str.contains(keywords_combined, case=False)

#filter df to only contain rows with mentions
matchedrows = df[df["match"] == True]

##setup keyword list
## does case matter? check for this in comparison function description
##search speeches for keyword - flag if speech contains item in list (what if >1 item in single speech?)
##group by week 
##sum count flag in week
##expand: take 50 words before & after keyword location in text -> 'context' var

##tf-idf for topic -> do this within each debate?