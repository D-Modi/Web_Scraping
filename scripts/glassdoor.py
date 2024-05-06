from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd
import random

n = 26
j = 10
while n < 51:
    comp = []
    
    driver = webdriver.Chrome()
    for num in range(n,51):
        #driver = webdriver.Chrome()
        driver.get(f"https://www.glassdoor.co.in/Explore/browse-companies.htm?overall_rating_low=3.5&page={num}&filterType=RATING_COMP_AND_BENEFITS")
        random_decimal = random.uniform(0, 2)
        time.sleep(random_decimal)

        src = driver.page_source
        soup = BeautifulSoup(src, 'lxml')
        body = soup.body

        ideal = body.find_all("h2", {'data-test': 'employer-short-name'})
        
        if len(ideal) == 0:
            j = j + 1
            print("###########################################")
            print(j)
            n = num
            driver.close()
            break

        for i in ideal:
            comp.append(i.text)

        #driver.close()
        data = pd.DataFrame()
        data["company"] = comp
        
        data.to_csv(f'company_name_{j}.csv', index=False)
    n = num
    j +=1
