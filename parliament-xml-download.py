# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 13:30:41 2021

@author: corber

set_ons_proxies function by Mitchell Edmunds@ONS
"""

#libraries
import pandas as pd
import requests
import time

#set ONS proxy function

def set_ons_proxies(ssl=False):
    """
    The ONS uses two proxy servers, this function finds the right
    one and saves them in a dictionary for requests.
    
    Parameters
    ----------
    ssl: filepath to the CA certificate for SSL verification
    
    """
    # Try each proxy in the following order.
    proxy_list = [
        "http://10.173.135.52:8080",
        "http://CR1-PSG-DMZ-VIP:8080",
        "http://CR2-PSG-DMZ-VIP:8080",
    ]

    test_url = "https://www.ons.gov.uk/"
    stop_at = len(proxy_list)-1    
    
    for i, proxy in enumerate(proxy_list):
        proxies = {'http': proxy, 'https': proxy}
        
        if i != stop_at:
            try:
                requests.get(test_url, proxies=proxies, verify=ssl)
                break
            except requests.exceptions.ProxyError:
                print(f"Proxy {proxy} not working. Changing to {proxy_list[i+1]}.")
        else:
            try:
                requests.get(test_url, proxies=proxies, verify=ssl)
            except requests.exceptions.ProxyError:
                raise requests.exceptions.ProxyError(
                    "None of the provided proxies work. Check for new proxy settings."
                )

    return proxies


#input data
hansardlinks_xlsx = "data/hansard-link-prep.xlsx"

#read in hansard xlsx & pull into dataframe - append sheetname as additional column
hansardlinks_sheetnames = pd.read_excel(hansardlinks_xlsx, sheet_name=None)

all_dfs = []
for tab_name, df in hansardlinks_sheetnames.items():
    df['type'] = tab_name
    all_dfs.append(df)
hansardlinks = pd.concat(all_dfs, ignore_index=True)

#cut down hansardlinks to approx half of files to be downloaded
testdownload = hansardlinks.head(3500) 


#download relevant URLs

totalfilestodownload = len(testdownload)
downloadcounter = 1

proxies = set_ons_proxies(ssl=True)

for index, row in testdownload.iterrows():
    print("downloading item " + str(downloadcounter) + " of " + str(totalfilestodownload))
    myfile = requests.get(row['url'], proxies=proxies, verify=True)
    open('c:/users/corber/downloads/uk-plt-xml/'+row['filename'], 'wb').write(myfile.content)
    print("downloaded file from: "+ row['url'] + "to: c:/users/corber/downloads/uk-plt-xml/" + row['filename'])
    downloadcounter = downloadcounter + 1
    time.sleep(15) #waits 15sec - to avoid rate limiting
