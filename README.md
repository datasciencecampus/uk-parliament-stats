# uk-parliament-stats
Identifying frequency and sentiment of mentions of UKSA/ONS and our statistics in the UK Parliament (2015-2021)

## Project Structure

### config.py

Configuration file for pipeline.

### /raw-data 

Where the download files are saved.

### /outputs

Where the output files are saved.

### /user-engagement

Files used in user/stakeholder engagement.

### /functions

Functions to download, parse and analyse the data.

### /functions/pipeline.py

Pipeline file used to call other functions

#### /functions/data_download/parliament_xml_download.py

Python script for downloading XML files of Hansard from https://www.theyworkforyou.com/pwdata/scrapedxml/. 

#### /functions/data_download/parliament_rds_download.py

Python script for downloading RDS file as a CSV.

#### /functions/data_processing/parliament_xml_processing.py

Python script for processing the downloaded XML files. 


## Workflow

The process has been modularised so that the user can either download the historic RDS file or download data in XML format for specific dates. The user can then process this data, save the processed data as a CSV and then analyse.

- Data download:
    - Choose `download_data = True` in config.py
    - To get historic 2015-2019 Commons Debates file from: https://dataverse.harvard.edu/file.xhtml?persistentId=doi:10.7910/DVN/L4OAKN/W2SVMF&version=1.0 and choose `data_type = 'RDS'` in config.py 
    - Or to download XML data choose `data_type = 'XML'` and specific the other parameters `date_start`, `date_end`, `sections`
- Data processing:
    - To create the CSV file from the data by `choose process_data = True` in config.py
    - To load a saved CSV file specify the filename in `csv_filename` in config.py
- The created or pre-saved CSV file is then loaded
- The data is then analysed 

