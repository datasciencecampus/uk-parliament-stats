# -*- coding: utf-8 -*-
"""
Created on Tue May 25 15:21:42 2021

@author: corber
"""

# --- Libraries ---
import pandas as pd

# --- Function ---

#Identify mentions of ONS from a csv file 
def find_ons_mentions (inputfile, keywords):
    df = pd.read_csv(inputfile)
    keywords_combined = '|'.join(keywords) #group keywords together, use '|' to separate and allow str.contains function to parse as logical OR (function accepts regex pattern)
    df["match"] = df["text"].str.contains(keywords_combined) #create T/F flag in 'match' for any speeches that contain keywords - case sensitive (as otherwise 'ons' will match on a LOT).
    return df


#Create date variables

def create_date_variables (df):
    df["date"] = pd.to_datetime(df["date"])     #convert date from object to datetime
    df['weekstart'] = df['date'].dt.to_period('W').apply(lambda r: r.start_time) #find date for Monday for each week
    #extract year, weeknumber and date of start of the week from the date field
    df["year"] = df["date"].dt.year
    df["weeknum"] = df["date"].dt.week
    #force two figures in weeknum, e.g. '5' -> '05', so that ordering can be done using week var created below
    df["weeknum"] = df["weeknum"].apply(lambda x: '{0:0>2}'.format(x))
    #create year specific week variable (e.g. 2015-03)
    df["week"] = df["year"].astype(str) + "-" + df["weeknum"].astype(str)
    return df

#Extract context from either side of ONS mention

def context_slicer (row):
    return row["text"][row["context-start"]:row["context-stop"]]