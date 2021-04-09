# uk-parliament-stats
Identifying frequency and sentiment of mentions of UKSA/ONS and our statistics in the UK Parliament (2015-2021)

## Project Structure

### /data 

Various data files used in the project

### /user-engagement

Files used in user/stakeholder engagement.

### parliament-frequency-analysis.py

Python script that does some basic frequency calculations of mentions of UKSA/ONS in our dataset.

### parliament-xml-download.py

Python script for downloading XML files of Hansard from https://www.theyworkforyou.com/pwdata/scrapedxml/

### rds-preparation.R

R script for some quick data prep on the data source used for project prototype. Output from this still needs some manual amending to fix encoding to utf-8 (see 'Workflow' section below).

## Workflow

- Get 2015-2019 Commons Debates file from: https://dataverse.harvard.edu/file.xhtml?persistentId=doi:10.7910/DVN/L4OAKN/W2SVMF&version=1.0
- Run this through rds-preparation.R
- Open CSV output produced by rds-preparation.R in Notepad, save as, switch encoding to 'UTF-8', save in desired location [this step is required because original encoding isn't support by python]
- Use parliament-frequency-analysis.py to read in the UTF-8 version of the csv & perform analysis 

Future plans: parliament-xml-download.py will be used to provide full data from 2015-2021 (& onwards if prototype moves into production)


