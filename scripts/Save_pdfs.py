
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import re

driver = webdriver.Chrome()

driver.get("https://linkedin.com/home")
time.sleep(2)

username = driver.find_element(By.ID, "session_key")
username.send_keys("dhruvimodi57@gmail.com")     #Enter Your email
pword = driver.find_element(By.ID, "session_password")
pword.send_keys("Dhruvi@1")	  #Enter your Password
driver.find_element(By.XPATH, "//button[@type='submit']").click()
time.sleep(25)
driver.maximize_window()

links_prof = ["https://www.linkedin.com/in/aishwarya-ramakrishnan/"]
i = 0
while i < len(links_prof):
    profile_url = links_prof[i]
    i+=1
    driver.get(profile_url)
    time.sleep(1)

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    all_links = soup.find_all('a', href=True)
    body = soup.body
    linkedin_links = [link['href'] for link in all_links if re.match(r'^https://www\.linkedin\.com/in/', link['href'])]

    flag = False
    tg = body.find_all("div", id="education")
    skill = ""
    if len(tg)>=1:
        
        pr = tg[0].parent
        sp_tags = pr.find_all("span", class_="pvs-navigation__text")
        if len(sp_tags) >=1:
            a_t = sp_tags[0].parent
            href_ = a_t.get('href')

            driver.get(str(href_))
            time.sleep(2)
            srca= driver.page_source
            soupa = BeautifulSoup(srca, 'lxml')
            bodya = soupa.body
            man = bodya.find('main', class_="scaffold-layout__main")
            sk_tags = man.find_all("div",{'class': "display-flex flex-row justify-space-between"})
        else:
            sk_tags = pr.find_all("div",{'class': "display-flex flex-row justify-space-between"})

        for s in sk_tags:
            sk = s.find_all('span', {'aria-hidden': 'true'})
            for sol in sk:
                print(sol.text)
            skill += sk[0].text + ", "
            if "Harvard" in sk[0].text:
                flag = True
        print(f"Education: {skill.strip().strip(',')}") 

    if flag == True:
        driver.get(profile_url)
        time.sleep(5)

        tal = body.find_all('button', { 'aria-label' : "More actions"})
        print(tal[-1])
        par = tal[-1].find_parent()
        print(par)
        id_val = par['id']
        print(id_val)
        dri = driver.find_element(By.ID, id_val)
        dri.click()
        time.sleep(1)
        # dri = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="More actions"]')
        # parent_element = dri.find_element(By.XPATH, "..")
        # parent_element.click()
        # time.sleep(1)

        tag = body.find_all('div', { 'aria-label' : "Save to PDF"})
        id_value = tag[-1]['id']
        print(id_value)
        dri = driver.find_element(By.ID, id_value)
        dri.click()
        time.sleep(1)

    
    # Print or store the filtered links
        for link in linkedin_links:
            #print(link)
            text = re.sub(r'\?.*', '', link)
            num_slashes = text.count('/')
            if num_slashes == 4:
                print(text)
                if text not in links_prof:
                    links_prof.append(text)

    
        time.sleep(5)
