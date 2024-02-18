import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time


driver = webdriver.Chrome()

driver.get("https://linkedin.com/home")
time.sleep(2)

username = driver.find_element(By.ID, "session_key")
username.send_keys("dhruvimodi57@gmail.com") 
pword = driver.find_element(By.ID, "session_password")
pword.send_keys("Dhruvi@1")	  #Enter your Password
driver.find_element(By.XPATH, "//button[@type='submit']").click()
time.sleep(75)

Head = [["Name", "Current Position", "Skills", "Linkedin URL"]]
num = 1
while len(Head) <= 100:
    profile_url = f"https://www.linkedin.com/search/results/people/?keywords=software%20developer&origin=CLUSTER_EXPANSION&page={num}&sid=RXv"
    driver.get(profile_url)
    src = driver.page_source
    soup = BeautifulSoup(src, 'lxml')
    body = soup.body
    num += 1

    ext = body.find_all("div", class_ = "mb1")
    for i in ext:
        row = ["", "", "", ""]
    
        a_tag = i.find('a')
        href_attribute = a_tag.get('href')
        print(f"Linkedin URL: {href_attribute}")
        row[3] =href_attribute

        s_tag = i.find('span', {'aria-hidden': 'true'})
        print(f"Name: {s_tag.text}")
        row[0] = s_tag.text

        curr_tag = i.find_next_sibling()
        curr = curr_tag.text.strip()
        if not curr.startswith("Current"):
            curr = i.find('div', class_='entity-result__primary-subtitle t-14 t-black t-normal').text
        curr = curr.replace('Current: ', '').strip()
        print("Current:=", curr)
        row[1] = curr.strip(',')

        driver.get(str(href_attribute))
        time.sleep(2)
        src1= driver.page_source
        soup1 = BeautifulSoup(src1, 'lxml')
        body1 = soup1.body
        tg = body1.find_all("div", id="skills")
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
                sk = s.find('span', {'aria-hidden': 'true'})
                skill += sk.text + ", "
            print(f"sKills: {skill.strip().strip(',')}") 
        row[2] = skill.strip().strip(',')
        Head.append(row)

        if (len(Head)) >= 101:
            break


csv_file_path = 'Linkedin.csv'
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(Head)

print("Done!")
        
