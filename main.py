import pandas as pd
import time
from latest_user_agents import get_latest_user_agents, get_random_user_agent
import requests
import json
from collections import OrderedDict
import random
from bs4 import BeautifulSoup                 
#SOUP
import timeit
import re
import statistics as st
import warnings
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.remote_connection import LOGGER
start = timeit.default_timer()

LOGGER.setLevel(logging.WARNING)
options = Options()
options.add_argument("--lang=tr-TR") #Turkish Language now 
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option("excludeSwitches", ['enable-automation'])
options.add_experimental_option('excludeSwitches', ['enable-logging'])
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)
options.add_argument("--disable-web-security")
options.add_argument("--disable-xss-auditor")
options.add_argument("--no-sandbox")
options.add_argument('--disable-gpu') 
options.add_argument("window-size=1280,800")
options.headless = False 
#OPTIONS
userAgent = get_random_user_agent() 
#Variables
warnings.filterwarnings("ignore", category=DeprecationWarning)
userAgent = get_random_user_agent() 

def alsoasked(keyword):
    time.sleep(5) 
    options.add_argument(f'user-agent={userAgent}')
   
    driver = webdriver.Chrome(r'YOURPATH/chromedriver.exe', options=options) #you need to define the path of your chrome driver
    driver.delete_all_cookies()
    driver.get("https://www.google.com")
    search_bar = driver.find_element(By.NAME, "q")
    for char in keyword: 
        start = 0.3 
        stop = 0.4 
        step = 0.2
        precision = 0.1
        f = 1 / precision
        n = random.randrange(start * f, stop * f, step * f) / f
        time.sleep(n)
        search_bar.send_keys(char)
    search_bar.send_keys(Keys.RETURN)
    source = driver.page_source
    soup = BeautifulSoup(source,'lxml')
    resp = soup.find_all("div", class_="LHJvCe")
    
    driver.close
    return resp

def readData():
    df = pd.read_excel("YOURPATH/keywords-and-volumes.xlsx")
    keyword = []
    volume = []
    kgr = []
    for index, row in df.iterrows():
        keyword.append(row[0])
        volume.append(row[1])
        text = alsoasked("allintitle:"+row[0]) 
        parts = [obj.text for obj in text]
        text = ' '.join(parts)
        parts = text.split(' ')
        kgr_value = 0
        print(parts)
        numeric_part = re.search(r'[-+]?\d*\.\d+|\d+', text)
        if numeric_part:
            x = numeric_part.group().replace(".","")
            kgr_value = int(x) / row[1]
        kgr.append(kgr_value)
        print(kgr)
    return keyword, volume, kgr
mydata = readData()
print(mydata)
df = pd.DataFrame({"keyword": mydata[0], "volume": mydata[1], "kgr": mydata[2]})
df.to_excel("result.xlsx", index=False)
