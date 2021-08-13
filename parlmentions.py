import pandas as pd
import os

from functions.data_processing.df_prep import find_ons_mentions
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
            print('Downloading xml files (0/8)')
            download_xml_files()
            print('Processing xml files (1/8)')
            filename = process_xml_files()
        elif config.data_type == 'RDS':
            print('Downloading rds file (1/8)')
            filename = download_rds_file()
    else:
        print('Data downloaded already (1/8)')

    if filename is None:
        filename = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'raw-data', config.data_type, config.csv_filename))

    print("Reading CSV (2/8)" )
    df = pd.read_csv(filename)

    print("Identifying mentions of specified organisations (3/8).")
    df = find_ons_mentions(df, config.organisations)

    # create variables: dates & week numbering, hansard URLs
    print("Creating variables (4/8)")
    df = create_date_variables(df)
    df = create_hansard_url(df)

    
    # extract context around keyword mention
    print("Extracting context around keyword mentions (5/8)")
    df = extract_context(df)

    
    # classify debates by topic
    print("Classifying debates in topics (6/8)")
    df = classify_debates(df)


    #remove unnecessary columns before saving the output
    print("Cleaning output (7/8)")
    df = remove_columns(df)


    #output to csv - drop index
    print("Saving data to CSV (8/8)")
    outputfile = os.path.abspath(
        os.path.join(os.path.dirname(__file__), 'outputs', 'data', f'uk_parl_stats_{os.path.basename(filename)}.csv'))
    df.to_csv(outputfile, index = False)
    print("Done!")
    return
  
# call function
parlmentions()