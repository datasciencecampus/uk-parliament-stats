import pandas as pd
import os

from src.data_processing.df_prep import find_org_mentions
from src.data_processing.df_prep import create_date_variables
from src.data_processing.df_prep import create_hansard_url
from src.data_processing.df_prep import extract_context
from src.data_processing.df_prep import remove_columns
from src.data_processing.df_prep import join_to_archive
from src.model_rules.topic_classification import classify_debates
from src.data_download.parliament_xml_download import update_dates
from src.data_download.parliament_xml_download import download_xml_files
from src.data_download.parliament_rds_download import download_rds_file
from src.data_processing.parliament_xml_processing import process_xml_files
from src.other.config_checker import config_checker

import config

localpath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'xml'))

# function to call all processing functions to create processed csv for use in dashboard
def parlmentions(localpath):

    filename = None

    config_checker(config)

    if config.download_data is True:
        if config.data_type == 'XML' and config.archive_update == False:
            print('Downloading xml files [0/8]')
            download_xml_files(localpath)
            print('Processing xml files [1/8]')
            filename = process_xml_files()
        elif config.data_type == 'XML' and config.archive_update == True:
            print('Using archive file -- reading, backing up, and using to update start & end dates...')
            config.date_start, config.date_end = update_dates() #overwrite config date range 
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
            os.path.join(os.path.dirname(__file__), 'data', config.data_type, config.csv_filename))

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
    
    #remove unnecessary columns before saving the output
    print("Cleaning output [7/8]")
    if config.search_what == 'Both':
        df = remove_columns(df, column = 'both')
    elif config.search_what == 'Text':
        df = remove_columns(df, column = 'text')        
    elif config.search_what == 'Agenda':
        df = remove_columns(df, column = 'agenda')


    #output to csv - drop index
    print("Saving data to CSV [8/8]")
    if config.archive_update == True:
        df = join_to_archive(df)
        df.to_csv(config.archive_location, index = False)  
    elif config.archive_update == False:
        outputfile = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'outputs', 'data', f'uk_parl_stats_{os.path.basename(filename)}'))
        df.to_csv(outputfile, index = False)
    print("Done!")
    return
  
# call function
parlmentions(localpath)