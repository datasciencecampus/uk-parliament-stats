# -*- coding: utf-8 -*-
"""
Created on Thu May 27 15:54:48 2021

@author: corber

set_ons_proxies function by Mitchell Edmunds@ONS
"""

import requests

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