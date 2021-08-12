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
from parlmentions.data_processing.keywords import keywords as keywords

# --- Variables ---

#parliament speech data
inputfile = "raw-data/commonsdebates_2015_2019-utf8.csv"

# --- Data Prep ---

# create dataframe
df = pd.read_csv(inputfile)

# tag speeches with ONS mentions (defined in keywords.py) in dataframe
df = find_ons_mentions(df, keywords)

# create dates & week numbering
df = create_date_variables(df)

# extract context around keyword mention
df = extract_context(df)






    
