# -*- coding: utf-8 -*-
"""
Created on Tue May 25 15:21:42 2021

@author: corber
"""

# --- Libraries ---
import pandas as pd

# --- Function ---

#Identify mentions of ONS from a csv file 
def find_ons_mentions (df, keywords):
    ons_search_terms = '|'.join(keywords) #group keywords together, use '|' to separate and allow str.contains function to parse as logical OR (function accepts regex pattern)
    df["match"] = df["text"].str.contains(ons_search_terms) #create T/F flag in 'match' for any speeches that contain keywords - case sensitive (as otherwise 'ons' will match on a LOT).
    df["match_name"] = df["text"].str.findall(ons_search_terms) #return keyword that was mentioned in new column
    df["match_name"] = df["match_name"].str[0] #only keep first search term that was found
    df["match_name"] = df.match_name.fillna('no match') #replace NaN with empty string - needs to be str for use in extract_context func
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

def find_ons_names_location (row):
    return row["text"].find(row.match_name)

def context_slicer (row):
    #only return the context for speeches that mention the ONS 
    if row["match"]:
        return row["text"][row["context-start"]:row["context-stop"]]
    else:
        return ""

def extract_context (df):
    df["ons_name_location"] = df.apply(lambda row: find_ons_names_location(row), axis=1) #find character location of relevant ons search term
    #create start/stop character locations for extracting context, cap at 0 & max length of str
    df["context-start"] = df["ons_name_location"]-200
    df["context-stop"] = df["ons_name_location"]+200
    #if the context start is negative, cap at 0 (don't want to take something from the end of the string!)
    df.loc[df["context-start"] < 0, 'context-start'] = 0
    #if the context stop is beyond the end of the string, cap to max at the length of the string
    df.loc[df["context-stop"] > df["text"].str.len(), 'context-stop'] = df["text"].str.len()
    #apply slicer to string row by row
    df["context"] = df.apply(lambda row: context_slicer(row), axis=1)
    return df


#Drop unnecessary columns

def remove_columns (df):
    df = df.drop(['party.facts.id', 'iso3country', 'year', 'weeknum', 'ons_name_location', 'context-start', 'context-stop'], axis=1)
    return df