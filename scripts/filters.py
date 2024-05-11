# import necessary libraries
import unicodedata
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import re
import numpy as np
import random

# Generate a random number between 1.5 and 3 for sleep time to prevent banning
def ra():
    return random.uniform(1.5, 3.0)

# Converting time spent in a company to months
def text_to_months(part):
    total_months = 0
    part = part.strip()  
    if 'yrs' in part:
        # Extract years
        years = int(part.split('yrs')[0].strip())
        if 'mos' in part.split('yrs')[1]:
            months = int(part.split('yrs')[1].split('mos')[0].strip())
        else:
            months = 0
        total_months = years * 12 + months # Convert years to months and add to total
    elif 'yr' in part:
        # Extract years
        years = int(part.split('yr')[0].strip())
        if 'mos' in part.split('yr')[1]:
            months = int(part.split('yr')[1].split('mos')[0].strip())
        else:
            months = 0
        total_months = years * 12 + months # Convert years to months and add to total
    elif 'mos' in part:
        # Extract months
        months = int(part.split('mos')[0].strip())
        total_months = months  # Add months to total
    return total_months

# normalizing text (european languages)
def normalize(text):
    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8').lower()

#common words which are sometimes not mentioned while mentioning university
words_to_remove = ["university", "of", "and", "institute", "school", "bussiness", "in"] 

# Geting list of colleges from csv file
csv_name = "/home/dhruvi/file_name.csv"
college = pd.read_csv(csv_name)
college.loc[college['Institution'].duplicated(), 'Institution'] = pd.NA
college.dropna(subset=["Institution"], inplace=True)

# Getting company namesn(5.5k companies)
comp_list = "combined_data.csv"
comp_names = pd.read_csv(comp_list)
comp_names.loc[comp_names['company'].duplicated(), 'company'] = pd.NA
comp_names.dropna(subset=["company"], inplace=True)

# Get the last "eligible" person to continu search (like a loop)
link_list = "/home/dhruvi/Eligible.csv"
df = pd.read_csv(link_list)
links_ = df["url"].tolist()
final = links_[len(links_)-2]

# Get all previous searches ( to prevent duplication)
all_check = "/home/dhruvi/All.csv"
all_df = pd.read_csv(all_check)
links_prof = all_df["url"].tolist()
links_prof.append(final)
i = len(links_prof) - 1
print(links_prof[i])
company = comp_names["company"].tolist()
inst = college["Institution"].tolist()

#normalizing and filtering names of colleges and companies before comparision
list_normalized = [normalize(item.lower().replace(" ", "")) for item in inst]
cleaned_list = [re.sub(r'[^\w\s]', '', s) for s in list_normalized]
filtered_strings = [re.sub(r'\([^)]*\)', '', s) for s in cleaned_list]
cleaned_strings = [''.join(word.replace(word_to_remove, '') for word_to_remove in words_to_remove) for word in filtered_strings]

comp_normalized = [normalize(item.lower().replace(" ", "")) for item in company]
cleaned_company = [re.sub(r'[^\w\s]', '', s) for s in comp_normalized]
cleaned_comp = [re.sub(r'\([^)]*\)', '', s) for s in cleaned_company]

driver = webdriver.Chrome()

driver.get("https://linkedin.com/home")
time.sleep(ra())

username = driver.find_element(By.ID, "session_key")
username.send_keys("dhruvimodi57@gmail.com")     #Enter Your email
pword = driver.find_element(By.ID, "session_password")
pword.send_keys("Dhruvi@1")	  #Enter your Password
driver.find_element(By.XPATH, "//button[@type='submit']").click()
time.sleep(ra() + 10)
driver.maximize_window()

potential = pd.DataFrame()
head = ["url", "name", "education", "flag_ed", "graduation year", "flag_grad", "experience", "flag_work", "filter"]
matrix = all_df.values
matrix = matrix[:, -9:]

len_i = i
while i < len(links_prof):
    row = []
    print(len(links_prof))
    profile_url = links_prof[i]
    row.append(profile_url)
    i+=1
    driver.get(profile_url)
    time.sleep(ra())

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    body = soup.body
    all_links = body.find_all('a', href=True)
    linkedin_links = [link['href'] for link in all_links if re.match(r'^https://www\.linkedin\.com/in/', link['href'])]
    print("******************************", len(linkedin_links))
  
    flag_univ = False
    flag_grad = False
    flag_comp = False
    flag_post = True

    # Getting name of the person
    top = body.find('div', class_="mt2 relative")
    name = top.find('h1').text
    print(name)
    row.append(name)

    # Getting eduaction qualification
    tg = body.find_all("div", id="education")
    skill = ""
    end_year = 2050         #if not specified
    if len(tg)>=1:
        
        pr = tg[0].parent
        sp_tags = pr.find_all("span", class_="pvs-navigation__text")
        if len(sp_tags) >=1:
            a_t = sp_tags[0].parent
            href_ = a_t.get('href')

            driver.get(str(href_))
            time.sleep(ra())
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
            if len(sk) >1:
                if "Master" in sk[1].text or "Bachelor" in sk[1].text or "MBA" in sk[1].text:

                    string_normalized = normalize(sk[0].text.lower().replace(" ", ""))
                    str_cleaned = re.sub(r'[^\w\s]', '', string_normalized)
                    word = re.sub(r'\([^)]*\)', '', str_cleaned)
                    str_ckeaned = ''.join(word.replace(word_to_remove, '') for word_to_remove in words_to_remove) 
                    if str_ckeaned in cleaned_strings:
                        flag_univ = True
                        print(flag_univ)
                if "Bachelor" in sk[1].text:
                    
                    year_pattern = r'\d{4}'
                    if len(sk) > 2:
                        if "-" in sk[2].text:
                            start_month_year, end_month_year = sk[2].text.split(" - ")
                            
                            start_year = int(re.search(year_pattern, start_month_year).group())
                            end_year = int(re.search(year_pattern, end_month_year).group())
                        else:
                            end_year = int(re.search(year_pattern, sk[2].text).group())
                        print(end_year)
                        if end_year <= 2010:
                            flag_grad = True
                elif "Master" in sk[1].text or "MBA" in sk[1].text:
                    year_pattern = r'\d{4}'
                    
                    if len(sk) > 2:
                        if "-" in sk[2].text:
                            start_month_year, end_month_year = sk[2].text.split(" - ")
                            
                            start_year = int(re.search(year_pattern, start_month_year).group())
                            end_year = int(re.search(year_pattern, end_month_year).group())
                        else:
                            end_year = int(re.search(year_pattern, sk[2].text).group())
                        print(end_year)
                        if end_year <= 2012:
                            flag_grad = True

    print(f"Education: {skill.strip().strip(',')}") 
    row.append(skill)
    row.append(flag_univ)
    row.append(end_year)
    row.append(flag_grad)

    # Getting experience deatils
    tg = body.find_all("div", id="experience")
    experience = ""
    if len(tg)>=1:
        
        pr = tg[0].parent
        sp_tags = pr.find_all("span", class_="pvs-navigation__text")
        if len(sp_tags) >=1:
            a_t = sp_tags[0].parent
            href_ = a_t.get('href')

            driver.get(str(href_))
            time.sleep(ra())
            srca= driver.page_source
            soupa = BeautifulSoup(srca, 'lxml')
            bodya = soupa.body
            man = bodya.find('main', class_="scaffold-layout__main")
            sk_tags = man.find_all("div",{'class': "display-flex flex-row justify-space-between"})
        else:
            sk_tags = pr.find_all("div",{'class': "display-flex flex-row justify-space-between"})

        total = 0
        total_top = 0
        for s in sk_tags:
            sk = s.find_all('span', {'aria-hidden': 'true'})
            for sol in sk:
                print(sol.text)
            
            comp = ""
            if '·' in sk[1].text:
                comp = sk[1].text.split("·")[0].strip()
            if len(sk) > 2 and (" mo" in sk[2].text or " yr" in sk[2].text):
                        if "·" in sk[2].text:
                            years = sk[2].text.split("·")[1].strip()
                        else:
                            years = sk[2].text.strip()
                        tim = text_to_months(years)
    
            elif (" mo" in sk[1].text or " yr" in sk[1].text):
                        
                        if "·" in sk[1].text:
                            years = sk[1].text.split("·")[1].strip()
                        else:
                            years = sk[1].text.strip()
                        tim = text_to_months(years)
     

            # if "Full-Time employee" or worked for more than 2 years (Some profiles dont have "Full Time" or any such similar thing written so assuming no wold remain a intern in a company for mare than 2 years)
            if "Full-time" in sk[1].text or tim > 24:
                    experience += comp + ": "
                    string_normalized_comp = normalize(comp.lower().replace(" ", ""))
                    comp_cleaned = re.sub(r'[^\w\s]', '', string_normalized_comp) 
                    comp_ckeaned = re.sub(r'\([^)]*\)', '', comp_cleaned)
                    post = sk[0].text
                    post_norm = normalize(sk[0].text.lower().replace(" ", ""))
                    if comp_ckeaned in cleaned_comp:
                        flag_comp = True
                        
                        post_clean = re.sub(r'[^\w\s]', '', post_norm)
                        if "ceo" in post_clean or "cto" in post_clean or "cofounder" in post_clean or "president" in post_clean or "intern" in post_clean or "student" in post_clean:
                            flag_post = False

                    experience += post + "; "
                    if len(sk) > 2 and (" mo" in sk[2].text or " yr" in sk[2].text):
                        if "·" in sk[2].text:
                            years = sk[2].text.split("·")[1].strip()
                        else:
                            years = sk[2].text.strip()
                        total += text_to_months(years)
                        if flag_comp:
                            total_top += text_to_months(years)
                    elif (" mo" in sk[1].text or " yr" in sk[1].text):
                        if "·" in sk[1].text:
                            years = sk[1].text.split("·")[1].strip()
                        else:
                            years = sk[1].text.strip()
                        total += text_to_months(years)
                        if flag_comp:
                            total_top += text_to_months(years)     
# some dont have year of graduation mentioned, so assumnig if a person has more than 6 yesrs of full time experience in a top company he has decent money.
        if total_top > 70:
            flag_grad = True                   
                        
         
    print(f"Experience: {experience.strip().strip(',')}") 
    row.append(experience)
    row.append(flag_comp)
    row.append(0)
    
    if flag_grad and flag_post: 
        if flag_univ or flag_comp:
            print(True)
            row[-1] = 1
            
            for link in linkedin_links:
                print(link)
                text = re.sub(r'\?.*', '', link)
                num_slashes = text.count('/')
                if num_slashes == 4:
                    print(text)
                    if text not in links_prof:
                        links_prof.append(text)
                        
    if i != len_i + 1:
        matrix = np.vstack([matrix, row])
        print(matrix.shape)
        all = pd.DataFrame(matrix, columns=head)
        print(all.shape)
        all.to_csv("/home/dhruvi/All.csv", index=0)
        potential = all[all['filter'] == 1]
        potential.to_csv("/home/dhruvi/Eligible.csv")

  # Preventing banning.
    if i > len_i + 40:
        driver.quit()
        time.sleep(ra())

        driver = webdriver.Chrome()
        driver.get("https://linkedin.com/home")
        time.sleep(ra())     

        username = driver.find_element(By.ID, "session_key")
        username.send_keys("dhruvimodi57@gmail.com")     #Enter Your email
        pword = driver.find_element(By.ID, "session_password")
        pword.send_keys("Dhruvi@1")	  #Enter your Password
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(ra())
        driver.maximize_window()
        len_i = i
