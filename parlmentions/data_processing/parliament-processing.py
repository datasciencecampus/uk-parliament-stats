# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 14:17:20 2021

@author: corber

"""


# --- Libraries ---
import pandas as pd
from parlmentions.functions.df_prep import find_ons_mentions
from parlmentions.functions.df_prep import create_date_variables
from parlmentions.functions.df_prep import extract_context

# --- Variables ---

#parliament speech data
inputfile = "raw-data/commonsdebates_2015_2019-utf8.csv"

#keywords to search for in speeches
keywords = ["ONS","Office for National Statistics", "Office of National Statistics", "UKSA", "UK Statistics Authority", "OSR", "Office for Statistics Regulation", "Office of Statistics Regulation"]


# --- Data Prep ---

# create dataframe
df = pd.read_csv(inputfile)

# tag speeches with ONS mentions in dataframe
df = find_ons_mentions(inputfile, keywords)

# create dates & week numbering
df = create_date_variables(df)

# extract context around keyword mention
df = extract_context(df)






    
