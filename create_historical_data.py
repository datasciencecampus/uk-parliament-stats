# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 13:47:16 2021

@author: corber
"""

# Libraries

import pandas as pd
from parlmentions.functions.df_prep import find_ons_mentions
from parlmentions.functions.df_prep import create_date_variables
from parlmentions.functions.df_prep import extract_context
from parlmentions.data_processing.parliament_processing import keywords
from parlmentions.model_rules.topic_classification import classify_debates

# function to call all processing functions to create processed csv for use in dashboard

def create_historical_data (inputfile, outputfile = "outputs/data/uk_parl_stats.csv"):
    # create dataframe from csv
    df = pd.read_csv(inputfile)
    print("1/6 - Read CSV in")
    
    # tag speeches with ONS mentions in dataframe
    df = find_ons_mentions(inputfile, keywords)
    print("2/6 - Identified mentions of ONS")

    # create dates & week numbering
    df = create_date_variables(df)
    print("3/6 - Created date variables")
    
    # extract context around keyword mention
    df = extract_context(df)
    print("4/6 - Extracted context around mention")
    
    # classify debates by topic
    df = classify_debates(df)
    print("5/6 - Classified debates")

    df.to_csv(outputfile)
    print("6/6 - Output data to CSV - Complete")
    return
    
    
    
    
# call function
create_historical_data(inputfile = "raw-data/commonsdebates_2015_2019-utf8.csv")