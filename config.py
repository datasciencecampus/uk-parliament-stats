## ---- Data options ---- ##

data_type = 'RDS' # Specific what type of data. Options: 'RDS' or 'XML'

## ---- Download options ---- ##

download_data = True # Download data or not. Options: True or False

#### For RDS ####
file_size = '1000' # Specify the size of the file. Options: 'All', '1000', '10000', or '100000'

#### For XML ####
sections = ['debates',
            'divisionsonly',
            'future',
            'london-mayors-questions',
            'lordsdivisionsonly',
            'lordspages',
            'ni',
            'regmem',
            'sp-motions',
            'sp-new',
            'sp-questions',
            'sp-written',
            'sp',
            'standing',
            'westminhall'] # Specify
            # sections. Options: ['debates','divisionsonly','future', 'london-mayors-questions', 'lordsdivisionsonly',
            # 'lordspages', 'ni','regmem','sp-motions','sp-new','sp-questions','sp-written','sp','standing','westminhall'
date_start = '01/06/2021' # specify start date of files
date_end = '16/06/2021' # specify end date of files
use_proxies = False # Use proxies or not. Options: True or False.

## ---- Load options ---- ##

csv_filename = 'Corp_HouseOfCommons_V2_1000rnd.csv' # If using downloaded file, specify it's name

## ---- Search options ---- ##

organisations = ["ONS",
                 "Office for National Statistics",
                 "Office of National Statistics",
                 "UKSA",
                 "UK Statistics Authority",
                 "OSR",
                 "Office for Statistics Regulation",
                 "Office of Statistics Regulation"]


#### ---- Optional ---- ####
verbose = True # If you want print outs of statements choose True, if not choose False
