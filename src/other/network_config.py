# -*- coding: utf-8 -*-
"""
Created on Thu May 27 15:54:48 2021

@author: corber

set_ons_proxies function by Mitchell Edmunds@ONS
"""

import requests
import json

#set ONS proxy function


def set_proxies(proxy_list_fp, ssl=False):
    """
    Organisations often use proxy servers, this function finds the right
    one from a list and saves them in a dictionary for requests.
    
    Parameters
    ----------
    proxy_list_fp: filepath to json containing proxy options
    ssl: filepath to the CA certificate for SSL verification

    """
    # Try each proxy in the following order.
    with open(proxy_list_fp, 'r') as f:
        proxy_list = json.load(f)

    test_url = "https://www.google.co.uk/"
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