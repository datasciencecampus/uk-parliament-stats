# -*- coding: utf-8 -*-
"""
Created on Tue May 25 15:21:42 2021

@author: corber
"""

# --- Libraries ---
import pandas as pd
import config

# --- Function ---

#Identify mentions of organisations from a csv file
def find_org_mentions (df, keywords):
    org_search_terms = '|'.join(keywords) #group keywords together, use '|' to separate and allow str.contains function to parse as logical OR (function accepts regex pattern)
    df["match"] = df["text"].str.contains(org_search_terms) #create T/F flag in 'match' for any speeches that contain keywords - case sensitive (as otherwise 'ons' will match on a LOT).
    df["match_name"] = df["text"].str.findall(org_search_terms) #return keyword that was mentioned in new column
    df["match_name"] = df["match_name"].str[0] #only keep first search term that was found
    df["match_name"] = df.match_name.fillna('no match') #replace NaN with empty string - needs to be str for use in extract_context func
    return df


#Create date variables

def create_date_variables (df):
    df["date"] = pd.to_datetime(df["date"], dayfirst=True)     #convert date from object to datetime
    df['weekstart'] = df['date'].dt.to_period('W').apply(lambda r: r.start_time) #find date for Monday for each week
    #extract year, weeknumber and date of start of the week from the date field
    df["year"] = df["date"].dt.year
    df["weeknum"] = df["date"].dt.isocalendar().week
    #force two figures in weeknum, e.g. '5' -> '05', so that ordering can be done using week var created below
    df["weeknum"] = df["weeknum"].apply(lambda x: '{0:0>2}'.format(x))
    #create year specific week variable (e.g. 2015-03)
    df["week"] = df["year"].astype(str) + "-" + df["weeknum"].astype(str)
    return df

#Create Hansard URL based on date

def hansard_link_row (row):
    if row["parliament"] == "UK-HouseOfCommons":
        return "https://hansard.parliament.uk/commons/"+row["date"].strftime('%Y-%m-%d')
    else:
        return "https://hansard.parliament.uk/lords/"+row["date"].strftime('%Y-%m-%d')


def create_hansard_url (df):
    #if location = commons then x, elseif location = lords then y etc. <- need to fully implement when pulling in full range of data
    df["hansard_url"] = ""
    df["hansard_url"] = df.apply(lambda row: hansard_link_row(row), axis=1)
    return df


#Extract context from either side of ONS mention

def find_org_names_location (row):
    return row["text"].find(row.match_name)

def context_slicer (row):
    #only return the context for speeches that mention the ONS 
    if row["match"]:
        return row["text"][row["context-start"]:row["context-stop"]]
    else:
        return ""

def extract_context (df):
    df["org_name_location"] = df.apply(lambda row: find_org_names_location(row), axis=1) #find character location of relevant org search term
    #create start/stop character locations for extracting context, cap at 0 & max length of str
    df["context-start"] = df["org_name_location"]-200
    df["context-stop"] = df["org_name_location"]+200
    #if the context start is negative, cap at 0 (don't want to take something from the end of the string!)
    df.loc[df["context-start"] < 0, 'context-start'] = 0
    #if the context stop is beyond the end of the string, cap to max at the length of the string
    df.loc[df["context-stop"] > df["text"].str.len(), 'context-stop'] = df["text"].str.len()
    #apply slicer to string row by row
    df["context"] = df.apply(lambda row: context_slicer(row), axis=1)
    return df


#Drop unnecessary columns

def remove_columns (df, column = 'agenda'):
    # df = df.drop(['Unnamed: 0', 'index', 'merge_id', 'debate_id', 'merge_id_check', '' 'party.facts.id', 'iso3country', 'year', 'weeknum', 'org_name_location', 'context-start', 'context-stop'], axis=1)
    #easier to specify columns to keep - a lot to remove!
    df = df[['date','agenda', 'speech_id', 'speaker', 'text', 'section', 'parliament', 'match', 'match_name', 'week', 'weekstart', 'hansard_url', 'context', f'topic_{column}']]
    return df

# append data to existing CSV data and overwrite the csv specified in config
def join_to_archive(df):
    archive = pd.read_csv(config.archive_location)
    #force date & weekstart to date only to match what is in csv      
    df["date"] = df["date"].dt.strftime('%Y-%m-%d')
    df["weekstart"] = df["weekstart"].dt.strftime('%Y-%m-%d')
    #join dfs together
    dataframes = [archive, df]
    df = pd.concat(dataframes)
    return df