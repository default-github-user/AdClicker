#pylint:disable=C0103
#pylint:disable=W0622
#pylint:disable=W0611
#pylint:disable=W0404
import os
import time
import random


# For MultiProcess
from multiprocessing.dummy import Pool

# Logging and Arg
from sys import exit, argv
import logging
import requests
import urllib.parse
import time
from datetime import datetime


# py_proxy
#from proxy import Proxy

# Import selenium modules
from selenium import webdriver

# For Element Selection
from selenium.webdriver.common.by import By

# For Waiting for Elements
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# User Agent 


# For Proxy Grabber
from bs4 import BeautifulSoup
import requests
import lxml



# Data and Variables Here

driver_path = os.environ.get('CHROMEDRIVER_PATH')
binary_path = os.environ.get('GOOGLE_CHROME_BIN')
driver_UA = """Mozilla/5.0 (Series40; Nokia200/11.56; Profile/MIDP-2.1 Configuration/CLDC-1.1) Gecko/20100401 S40OviBrowser/2.0.1.62.6"""

# Configs Here
thread_count = os.getenv("THREAD_COUNT", 4)
page_url = os.getenv("PAGE_URL","https://za.gl/")

# page_urls = os.environ.get("PAGE_URLS")
# urls_file = os.environ.get("URLS_FILE")
# if page_urls==None:
#     if not "http" in urls_file:
#         if os.path.exists("./" + urls_file):
#             page_urls = open("./" + urls_file, "r").read()
#     else:
#         r = requests.get(urls_file)
#         page_urls = r.text()













def adress_proxy():
    target_url = 'https://www.ip-adress.com/proxy-list'
    result = requests.get(target_url)
    soup = BeautifulSoup(result.text, "lxml")
    pars_result = soup.find('tbody').find_all('tr')
    proxy_list = []
    for elem in pars_result:
        elem = elem.get_text().split()[:2]
        if elem[1] != 'transparent':
            proxy_list.append(elem[0])
    return proxy_list

def check_proxy(proxy):
    proxy = 'http://' + proxy
    time.sleep(1)
    try:
        result = requests.get('http://ip-api.com/json', proxies={'http': proxy}, timeout=2)
        if result.status_code == 200:
            try:
                if result.json()['status'] == 'success':
                    return True
            except IndexError:
                return False
        else:
            return False
    except requests.exceptions.ConnectionError:
        return False
    except requests.exceptions.ReadTimeout:
        return False
    except requests.exceptions.ChunkedEncodingError:
        return False
    except requests.exceptions.TooManyRedirects:
        return False



def click_adds(page_url, proxy, driver_UA):
    # Create a Proxy Config
    time.sleep(random.choice(range(20,2000)))
    print("[#] Using New Proxy: " + proxy)
    options = webdriver.ChromeOptions()
    options.binary_location = binary_path
    options.add_argument('headless')
    options.add_argument('--proxy-server=' + proxy)
    options.add_argument("user-agent=" + driver_UA)
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument("--blink-settings=imagesEnabled=false")
    #options.add_argument("default_content_settings.images=2")
    options.add_argument('--disable-logging')
    desired_cap = options.to_capabilities()
    # Load Page
    print("[#] Loading Page...")
    pbrowser = webdriver.Chrome(executable_path=driver_path,desired_capabilities=desired_cap,service_log_path="chromedriver_logs.log")
    #pbrowser.maximize_window()
    pbrowser.get(page_url)
    print("[#] Success... "+"\n"+"[i] Page Title: "+ pbrowser.title )
    sleep_timer = random.choice(range(2,20))
    print('[#] Waiting {sleep_timer} seconds')
    time.sleep(sleep_timer)
    try:
        print("[#] Searching Button...")
        WebDriverWait(pbrowser, 120).until(EC.element_to_be_clickable((By.CLASS_NAME, "btn btn-success btn-lg get-link")))
        print("[#] Clicking Button...")
        WebDriverWait(pbrowser, 20).until(EC.url_changes)
        print("[#] Click Ok...")
    except Exception as e:
        print("[!] Error in Clicking Button: " + str(e))
    pbrowser.quit()









    
    




    


def main():
    """
    Program
    """
    print("[#] Starting...")
    print("[#] Fetching Proxies...")
    proxy_list = adress_proxy()
    working_proxies = []
    for proxy in proxy_list:
        if check_proxy(proxy)==True:
            working_proxies.append(proxy)
    print("[#] Found " + str(len(working_proxies)) + " working proxies.")
    # new_proxy = working_proxies[0]
    proxy_counter = 0
    ua = UserAgent()
    with Pool(thread_count) as worker:
        print("[#] Starting Click Bot " + str(proxy_counter)  + " with Proxy: " + str(working_proxies[proxy_counter]))
        worker.map(click_adds, page_url, working_proxies[proxy_counter], ua.random)
        worker.close()
        proxy_counter += 1
        worker.join()
    # OK
