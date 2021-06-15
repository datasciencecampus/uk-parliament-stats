# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 13:47:16 2021

@author: corber
"""

# Libraries

import pandas as pd
from parlmentions.data_processing.keywords import keywords as keywords
from parlmentions.functions.df_prep import find_ons_mentions
from parlmentions.functions.df_prep import create_date_variables
from parlmentions.functions.df_prep import extract_context
from parlmentions.functions.df_prep import remove_columns
from parlmentions.model_rules.topic_classification import classify_debates

#Variables

rawdatafile = "raw-data/commonsdebates_2015_2019-utf8.csv"

# function to call all processing functions to create processed csv for use in dashboard
def create_historical_data (inputfile, keywords=keywords, outputfile = "outputs/data/uk_parl_stats.csv"):
    # create dataframe from csv
    print("0/7 - Reading CSV..." )
    df = pd.read_csv(inputfile)
    print("1/7 - Read CSV in")
    
    # tag speeches with ONS mentions in dataframe
    df = find_ons_mentions(df, keywords)
    print("2/7 - Identified mentions of ONS")

    # create dates & week numbering
    df = create_date_variables(df)
    print("3/7 - Created date variables")
    
    # extract context around keyword mention
    df = extract_context(df)
    print("4/7 - Extracted context around mention")
    
    # classify debates by topic
    df = classify_debates(df)
    print("5/7 - Classified debates")

    #remove unnecessary columns before saving the output
    df = remove_columns(df)
    print("6/7 - Removed unnecessary columns")

    #output to csv - drop index
    df.to_csv(outputfile, index = False)
    print("7/7 - Output data to CSV - Complete")
    return
  
# call function
create_historical_data(inputfile = rawdatafile)