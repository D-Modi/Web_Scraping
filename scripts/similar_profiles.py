import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import re
import pandas as pd
import random

driver = webdriver.Chrome()

driver.get("https://linkedin.com/home")
#r = random.randint(2, 60)
r = 2
print(r)
time.sleep(r)
print(r)

username = driver.find_element(By.ID, "session_key")
username.send_keys("dhruvimodi57@gmail.com")     #Enter Your email
pword = driver.find_element(By.ID, "session_password")
pword.send_keys("Dhruvi@1")	  #Enter your Password
driver.find_element(By.XPATH, "//button[@type='submit']").click()
#r = random.randint(2, 60)
time.sleep(r)
m = "https://www.linkedin.com/in/rohanjain-2209"
driver.get("https://www.linkedin.com/in/rohanjain-2209/overlay/browsemap-recommendations/")
#r = random.randint(2, 60)
time.sleep(r)
src = driver.page_source
soup = BeautifulSoup(src, 'lxml')
body = soup.body
ld_links = body.find_all('a', href=lambda href: href and href.startswith('https://www.linkedin.com/in/'))
#print(ld_links)
#print(len(ld_links))
ld = set()
for l in ld_links:
    link = l.get("href")
    #print(link)
    #print("########################3")
    link = str(link)
    if link.startswith(m):
        continue
    if link:
        link = re.sub(r"\?.*", "", link)
        ld.add(link)

linkedin = list(ld)
print(len(linkedin))
print(linkedin)
