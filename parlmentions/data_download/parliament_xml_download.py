# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 13:30:41 2021

@author: corber

set_ons_proxies function by Mitchell Edmunds@ONS
"""

#libraries
import pandas as pd
import requests
from requests.exceptions import ProxyError
import time
import os.path
from parlmentions.functions.ons_network import set_ons_proxies

#variables
localpath = 'raw-data/uk-plt-xml/' #set local path for desired download location - default is within project
hansardlinks_xlsx = "raw-data/hansard-link-prep.xlsx" #list of files to download


#read in hansard xlsx & pull into dataframe - append sheetname as additional column
hansardlinks_sheetnames = pd.read_excel(hansardlinks_xlsx, sheet_name=None)
all_dfs = []

for tab_name, df in hansardlinks_sheetnames.items():
    df['type'] = tab_name
    all_dfs.append(df)
hansardlinks = pd.concat(all_dfs, ignore_index=True)

#download XML files
totalfilestodownload = len(hansardlinks)
downloadcounter = 1

while downloadcounter <= totalfilestodownload:
    for index, row in hansardlinks.iterrows():
        try:
            print("Item " + str(downloadcounter) + " ["+row['filename']+"] of " + str(totalfilestodownload))
            if os.path.isfile(localpath+row['filename']) == True:
               print("file already exists - skipping to next file\n")
               downloadcounter = downloadcounter + 1
            else:
                proxies = set_ons_proxies(ssl=True) #find working proxy 
                print("downloading item " + str(downloadcounter) + " of " + str(totalfilestodownload))
                myfile = requests.get(row['url'], proxies=proxies, verify=True)
                open(localpath+row['filename'], 'wb').write(myfile.content)
                print("downloaded file from: "+ row['url'] + "\n to: " + localpath + row['filename']+'\n')
                downloadcounter = downloadcounter + 1
                time.sleep(15) #waits 15sec - to avoid rate limiting
        except ProxyError:
            print("<<< No proxies worked - waiting 60 seconds then re-trying >>>")
            time.sleep(60) #wait 60sec - then re-try
