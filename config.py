## ---- Data options ---- ##

data_type = 'XML' # Specific what type of data. Options: 'RDS' or 'XML'

## ---- Download options ---- ##

download_data = True # Download data or not. Options: True or False

#### For RDS ####
file_size = '1000' # Specify the size of the file. Options: 'All', '1000', '10000', or '100000'

#### For XML ####
archive_update = False #Specify if you wish to use an archive file of already processed XML and only process new data up today's date. Useful for regular updating. Options: True or False
archive_backup = True # Specify whether you wish to make a backup of the archive before appending new data - will create a date+timestamped file in the same folder as the archive. Options: True or False

sections = ['debates'] # Specify
            # sections. Options: ['debates','divisionsonly','future', 'london-mayors-questions', 'lordsdivisionsonly',
            # 'lordspages', 'ni','regmem','sp-motions','sp-new','sp-questions','sp-written','sp','standing','westminhall'
date_start = '27/03/2023' # specify start date of files
date_end = '31/03/2023' # specify end date of files
use_proxies = True # Use proxies or not. Options: True or False.
proxy_list_fp = "secrets/proxies.json"
proxy_try_attempts = 5 # number of times a proxy is attempted before returning an error

## ---- Load options ---- ##

archive_location = "outputs/data/uk_parl_stats.csv" # Provide the path to the archive file.
csv_filename = 'Corp_HouseOfCommons_V2_1000rnd.csv' # If using downloaded file, specify it's name

## ---- Search options ---- ##

organisations = ["UKSA",
                 "UK Statistics Authority",
                 "OSR",
                 "Office for Statistics Regulation",
                 "Office of Statistics Regulation",
                 "ONS",
                 "Office for National Statistics",
                 "Office of National Statistics"]

search_what = 'Agenda' # Search agenda or text or both. Options: Both, Text, Agenda.

#### ---- Optional ---- ####
verbose = True # If you want print outs of statements choose True, if not choose False
