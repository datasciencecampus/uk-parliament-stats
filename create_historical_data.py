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
    print("2/7 - Identifying mentions of ONS...")
    df = find_ons_mentions(df, keywords)

    # create dates & week numbering
    print("3/7 - Creating date variables...")
    df = create_date_variables(df)

    
    # extract context around keyword mention
    print("4/7 - Extracting context around mention...")
    df = extract_context(df)

    
    # classify debates by topic
    print("5/7 - Classifying debates...")
    df = classify_debates(df)


    #remove unnecessary columns before saving the output
    print("6/7 - Removing unnecessary columns...")
    df = remove_columns(df)


    #output to csv - drop index
    print("7/7 - Saving data to CSV...")
    df.to_csv(outputfile, index = False)
    print("Done!")
    return
  
# call function
create_historical_data(inputfile = rawdatafile)