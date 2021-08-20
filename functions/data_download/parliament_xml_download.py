import requests
from requests.exceptions import ProxyError
import time
import os.path
from datetime import datetime
from bs4 import BeautifulSoup
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from functions.other.ons_network import set_ons_proxies
import config

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
                if datetime.strptime(config.date_start, '%d/%m/%Y') < date <= datetime.strptime(config.date_end,
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
                print(f"{filename} all ready exists ({count}/{total_files})")
        count += 1

def download_xml_files():
    check_if_folders_exist(config)
    download_urls, section_list = get_download_links(config)
    download(download_urls)
