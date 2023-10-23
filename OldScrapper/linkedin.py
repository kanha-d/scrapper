import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import requests
import bs4
from collections import Counter
import mysql.connector
from datetime import datetime, timedelta, date
import re
import pandas as pd

from time import sleep


mydb = mysql.connector.connect(
    host="15.206.16.152",
    user="nishtyainfotech_jobaaj",
    database="nishtyainfotech_jobaaj",
    password="9k,w8IvdPGrL"
)

mycursor = mydb.cursor(buffered=True)

# ######################################
option = Options()
option.add_argument("--disable-infobars")
option.add_argument("start-maximized")
option.add_argument("--disable-extensions")
# Pass the argument 1 to allow and 2 to block
option.add_experimental_option(
    "prefs", {"profile.default_content_setting_values.notifications": 1}
)
driver = webdriver.Chrome(chrome_options=option, executable_path="./chromedriver.exe")
# ######################################
actions = ActionChains(driver)
driver.maximize_window()


mycursor.execute("select distinct app_type from job_product")

records = mycursor.fetchall()
list1 = []
for rec in records:
    list1.append(rec[0])


skl = pd.read_sql("select skill from scrapper_skills where cat = 2",mydb)


# cat_array = [
#     "data%20analyst",
#     "taxation",
#     "accounting",
#     "finance",
#     "investment%20banking",
#     "audit",
#     "consulting"
# ]

cat_array = [
    "taxation",
]

functional_area = {
    "taxation": "3",
    "Audit+%26+Assurance": "2",
    "Risk+Advisory": "2",
    "Financial+Advisory": "4"
}

skills = {
    "TAX": "2",
    "Audit+%26+Assurance": "2",
    "Risk+Advisory": "2",
    "Financial+Advisory": "4"
}

# functions

def getExp(exp):
    if exp != -1 : 
        expirence = ''
        for k in range(-9, -1):
            expirence+=strr[exp+k]
        expirence.strip()
        digits = '-'.join(filter(str.isdigit, expirence))
        
        digits = digits.split("-")
       
        if len(digits) == 1:
            digits = [digits[0],int(digits[0])+2]
        if len(digits) == 3 :
            digits = [digits[0],digits[1]+''+digits[2]]
        if len(digits) == 4 :
            digits = [digits[0] + '' + digits[1],digits[2]+''+digits[3]]  
        if digits[0] == '1' and int(digits[1]) >= 5 :
            digits = [digits[0]+''+digits[1],10+int(digits[1])+2]
        if digits[0] == '1' and digits[1] == '0' :
            digits = [digits[0]+''+digits[1],10+int(digits[1])+2]   
        if digits[0] > 20 : 
            digits = digits['20','25']
        
    else : 
        if 'Manager' in title :
            digits = ['4','8']
        elif 'AM' in title :
            digits = ['2','4']
        elif 'DM' in title :
            digits = ['3','6']
        elif 'SM' in title :
            digits = ['5','8']    
        elif 'Senior' in title :
            digits = ['4','10']
        else :
            digits = ['0','1']
        
    return digits


def getSkills(desc):
    strr = re.sub("\s\s+", " ", desc.text.lower())
    strr = re.sub("\s\s+", " ", strr)
    my_str = ''


    for i in skl.index:
        skill  =  str(skl['skill'][i])
      
        pat1 = ' ' + re.escape(skill) + r'\n'
        pat2 = ' ' + re.escape(skill) + r' '
        pat3 = ' ' + re.escape(skill) + r','
        pat4 = ' ' + re.escape(skill) + r'/'
        pat5 = ' ' + re.escape(skill) + r' '
        pat6 = '\n' +re.escape(skill) + r'\n'
        pat7 = '\n' +re.escape(skill) + r' '
        pattern = re.compile(pat1 + '|' + pat2 + '|' + pat3 + '|' + pat4 + '|' + pat5 + '|' + pat6 + '|' + pat7)

        if pattern.search(strr) or pattern.search(title.lower()):
            my_str += skill.strip() + ','

        skills = my_str.split(",")
        skills = [*set(skills)]
        newskills = ','.join(str(s) for s in skills)
    return newskills[1:]

# collect all urls
jobs_url = ['https://www.linkedin.com/jobs/view/3549018593/?eBP=JOB_SEARCH_ORGANIC&recommendedFlavor=ACTIVELY_HIRING_COMPANY&refId=joZO%2BZjU1MHtxd40xlvzww%3D%3D&trackingId=KbAp8QgjTtZJTeYDjjF8oQ%3D%3D&trk=flagship3_search_srp_jobs','taxation']
# for cat_value in cat_array:

#     url = "https://www.linkedin.com/jobs/search/?f_TPR=r86400&keywords=" + cat_value + "&location=India&start=0"
#     driver.get(url)
#     sleep(10)

#     jobsCountText = driver.find_element(By.CLASS_NAME, 'results-context-header__new-jobs').text
#     jobsCount = jobsCountText.split()[0][1:].replace(",", "")
#     print(jobsCount)
#     sleep(3)

#     for jobIndex in range(1, int(jobsCount)+1):

#         if (jobIndex % 25 == 0):
#             driver.execute_script("scroll(0, document.body.scrollHeight);")
#             show_button = driver.find_element(By.CLASS_NAME, 'infinite-scroller__show-more-button')
#             driver.execute_script("arguments[0].click();", show_button)
#             sleep(15)

#         elements = driver.find_element(By.CLASS_NAME, 'jobs-search__results-list')

#         try:
#             job = elements.find_element(By.CSS_SELECTOR, 'li:nth-of-type('+str(jobIndex)+')')
#             link = job.find_element(By.TAG_NAME, 'a').get_attribute('href')
#             jobs_url.append([cat_value,link])
#             print(link , str(jobIndex))
#         except:
#             print('Exception in li')
#             break
        
# driver.close()       

print(len(jobs_url))

# collect all data
jobs_arr = []
job_arr = []

for url in jobs_url:

    res = requests.get('https://www.linkedin.com/jobs/view/3549018593/?eBP=JOB_SEARCH_ORGANIC&recommendedFlavor=ACTIVELY_HIRING_COMPANY&refId=joZO%2BZjU1MHtxd40xlvzww%3D%3D&trackingId=KbAp8QgjTtZJTeYDjjF8oQ%3D%3D&trk=flagship3_search_srp_jobs')
    bs = bs4.BeautifulSoup(res.text,"html.parser")
    try:
        post_url = bs.find('a',{'class':'sign-up-modal__company_webiste'})
        new_url = post_url.get('href')
        job_link = requests.get(new_url)

        job_url = job_link.url
        title = bs.find('h1',{'class' :'top-card-layout__title'}).text
        location = bs.find('span',{'class' :'topcard__flavor--bullet'}).text
        company = bs.find('a',{'data-tracking-control-name' :'public_jobs_topcard-org-name'}).text
        desc = bs.find('div',{'class' :'show-more-less-html__markup'})

        try :
            strr = re.sub("\s\s+", " ", desc.text.lower())
            strr = re.sub("\s\s+", " ", strr)
            

            try : 
                exp = strr.find("year")
                digits = getExp(exp)        
            except : 
                exp = strr.find("year",strr.find("year")+1)
                digits = getExp(exp)               
        except Exception as ex :
            print('Exception from Exp')

        job_exp = [int(digits[0]),int(digits[1])]
        skills = getSkills(desc)

        job_url = job_url.strip()
        title = title.strip()
        location = location.strip()
        company = company.strip()
        desc = desc.strip()

        f = open("linkedin.txt", "a")
        f.write("linkedin URL: "+url["1"]+"\n")
        f.write("External URL: "+job_url+"\n")
        f.write("Title: "+title+"\n")
        f.write("location: " + location+"\n")
        f.write("skills: " + skills+"\n")
        f.write("Exp : " + str(job_exp)+"\n")
        f.write("Functional : " + str(functional_area[url[0]])+"\n")
        f.write("\n\n")
        f.close()
        break

    except:
        print('Internal Link')
        continue

    job_arr = [title,job_url,location,skills,job_exp,functional_area[url[0]]]
    jobs_arr.append(job_arr)
    print(job_arr)
print(jobs_arr)


