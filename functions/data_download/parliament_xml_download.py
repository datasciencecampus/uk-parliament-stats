import requests
from requests.exceptions import ProxyError
import time
import os.path
from datetime import datetime
from datetime import timedelta
from bs4 import BeautifulSoup
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from functions.other.ons_network import set_ons_proxies
import config
import pandas as pd

localpath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'raw-data', 'xml'))
verbose = config.verbose

def check_if_folders_exist(config):
    for section in config.sections:
        check_folder = os.path.isdir(os.path.join(localpath, section))
        if not check_folder:
            os.makedirs(os.path.join(localpath, section))


def get_download_links(config):
    download_urls = []
    section_list = []
    for section in config.sections:
        section_url = 'https://www.theyworkforyou.com/pwdata/scrapedxml/' + section        
        if config.use_proxies == True:
            try:
                proxies = set_ons_proxies(ssl=True)
                page = requests.get(section_url, proxies=proxies, verify=False)
            except ProxyError:
                print("<<< No proxies worked - waiting 60 seconds then re-trying >>>")
                time.sleep(60)
        else:
            try:
                page = requests.get(section_url, verify=False)
            except ProxyError:
                print("<<< No proxies worked - waiting 60 seconds then re-trying >>>")
                time.sleep(60)
     
        data = page.text
        soup = BeautifulSoup(data, features="lxml")
        for link in soup.find_all('a'):
            match = re.search(r'\d{4}-\d{2}-\d{2}', link.text)
            if match is not None:
                date = datetime.strptime(match.group(), '%Y-%m-%d')
                if datetime.strptime(config.date_start, '%d/%m/%Y') <= date <= datetime.strptime(config.date_end,
                                                                                                '%d/%m/%Y'):
                    download_urls.append(
                        'https://www.theyworkforyou.com/pwdata/scrapedxml/' + section + '/' + link.text)
                    section_list.append(section)

    return download_urls, section_list

def download(download_urls):
    sleep_time = 30
    total_files = len(download_urls)
    count = 1
    for download_url in download_urls:

        filename = os.path.join(localpath, download_url.split('/')[-2], download_url.split('/')[-1])

        if os.path.isfile(filename) is False:
            if config.use_proxies == True:
                try:
                    proxies = set_ons_proxies(ssl=True)
                    xml_file = requests.get(download_url, proxies=proxies, verify=True)
                except ProxyError:
                    print("<<< No proxies worked - waiting 60 seconds then re-trying >>>")
                    time.sleep(60)
            else:
                try:
                    xml_file = requests.get(download_url, verify=False)
                except ProxyError:
                    print("<<< proxy error - waiting 60 seconds then re-trying >>>")
                    time.sleep(60)
            open(filename, 'wb').write(xml_file.content)
            if verbose == True:
                print(f"downloaded file from: {download_url} \n to: {filename} ({count}/{total_files})")
            time.sleep(sleep_time)

        else:
            if verbose == True:
                print(f"{filename} already exists ({count}/{total_files})")
        count += 1

def download_xml_files():
    check_if_folders_exist(config)
    download_urls, section_list = get_download_links(config)
    download(download_urls)




def update_dates():
   
# - open csv specified in config
    archive = pd.read_csv(config.archive_location)

# - make backup copy with datetime stamp to folder
    if config.archive_backup == True:
        archive.to_csv("D:/uk-parliament-stats/outputs/data/uk_parl_stats-backup.csv", index = False) # need to split up file path into parts, add date/timestamp + join back up
    else:
        pass

    # - find max date in csv & save this as variable
    latest_date = datetime.strptime(archive["date"].max(), '%Y-%m-%d') + timedelta(days=1)
    # - overwrite config.date_start with max value + 1 day
    updated_date_start = latest_date.strftime('%d/%m/%Y') #convert back to string & match format used in config file
    # update config.date_end with current date
    updated_date_end = datetime.today().strftime('%d/%m/%Y')
    return (updated_date_start, updated_date_end)