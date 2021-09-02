import pandas as pd
import os

from functions.data_processing.df_prep import find_org_mentions
from functions.data_processing.df_prep import create_date_variables
from functions.data_processing.df_prep import create_hansard_url
from functions.data_processing.df_prep import extract_context
from functions.data_processing.df_prep import remove_columns
from functions.model_rules.topic_classification import classify_debates
from functions.data_download.parliament_xml_download import download_xml_files
from functions.data_download.parliament_rds_download import download_rds_file
from functions.data_processing.parliament_xml_processing import process_xml_files
from functions.other.config_checker import config_checker

import config


# function to call all processing functions to create processed csv for use in dashboard
def parlmentions():

    filename = None

    config_checker()

    if config.download_data is True:
        if config.data_type == 'XML':
            print('Downloading xml files [0/8]')
            download_xml_files()
            print('Processing xml files [1/8]')
            filename = process_xml_files()
        elif config.data_type == 'RDS':
            print('Downloading rds file [1/8]')
            filename = download_rds_file()
    else:
        print('Data downloaded already [1/8]')

    if filename is None:
        filename = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'raw-data', config.data_type, config.csv_filename))

    print("Reading CSV [2/8]" )
    df = pd.read_csv(filename)

    print("Identifying mentions of specified organisations [3/8].")
    df = find_org_mentions(df, config.organisations)

    # create variables: dates & week numbering, hansard URLs
    print("Creating variables [4/8]")
    df = create_date_variables(df)
    df = create_hansard_url(df)

    
    # extract context around keyword mention
    print("Extracting context around keyword mentions [5/8]")
    df = extract_context(df)

    
    # classify debates from agenda title, text or both
    if config.search_what == 'Both':
        print("Classifying debates from agenda title and text, please wait, this may take a while... [6/8]")
        df = classify_debates(df, column = 'agenda')
        df = classify_debates(df, column = 'text')
    elif config.search_what == 'Text':
        print("Classifying debates from text, please wait, this may take a while... [6/8]")
        df = classify_debates(df, column='text')
    elif config.search_what == 'Agenda':
        print("Classifying debates from agenda [6/8]")
        df = classify_debates(df, column='agenda')

    print("Cleaning output [7/8]")
    if config.search_what == 'Both':
        df = remove_columns(df, column = 'both')
    elif config.search_what == 'Text':
        df = remove_columns(df, column = 'text')        
    elif config.search_what == 'Agenda':
        df = remove_columns(df, column = 'agenda')


    #output to csv - drop index
    print("Saving data to CSV [8/8]")
    outputfile = os.path.abspath(
        os.path.join(os.path.dirname(__file__), 'outputs', 'data', f'uk_parl_stats_{os.path.basename(filename)}'))
    df.to_csv(outputfile, index = False)
    print("Done!")
    return
  
# call function
parlmentions()