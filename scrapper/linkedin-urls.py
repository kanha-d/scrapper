
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import shutup; shutup.please()
from fuzzywuzzy import fuzz,process
from webdriver_manager.chrome import ChromeDriverManager

import requests
import bs4
from collections import Counter
import mysql.connector
import re
import pandas as pd

import time
from time import sleep
import io
from scrapper_functions import *

mydb = mysql.connector.connect(
    host="15.206.16.152",
    user="nishtyainfotech_jobaaj",
    database="nishtyainfotech_jobaaj_01jul",
    password="9k,w8IvdPGrL"
)

data_keywords_not_to_have = ["clinical","developer","software","it","staff","operator"]

not_allowed = ["shine.com","iimjobs","hirist.com"]

mycursor = mydb.cursor(buffered=True)

f = open("linkedin.txt", "a")
f2 = open("linkedin-query.txt", "a")

# ######################################


# ######################################

# ######################################
option = Options()
#option.add_argument("--headless")
option.add_argument("--disable-infobars")
option.add_argument("start-maximized")
option.add_argument("--disable-extensions")
# Pass the argument 1 to allow and 2 to block
option.add_experimental_option(
    "prefs", {"profile.default_content_setting_values.notifications": 1}
)

driver = webdriver.Chrome(ChromeDriverManager().install())
action = ActionChains(driver)
driver.maximize_window()


mycursor.execute("select distinct app_type from job_product")

records = mycursor.fetchall()
list1 = []

for rec in records:
    list1.append(rec[0])

 
compUni = pd.read_sql("select id,name from job_companies_new",mydb)

functional_area = {
    "data%20analyst":"12",
    "taxation":"3",
    "accounting":"1",
    "finance":"4",
    "investment%20banking":"5",
    "audit":"2",
    "consulting":"16",
}

skillSet = {
   "finance" : "4",
   "audit" : "3",
   "taxation" : "3,4",
   "accounting" : "1",
   "data%20analyst":"12",
   "investment%20banking":"5",
   "consulting":"16"
   }

f = open("linkedin.txt","a")

# collect all urls
jobs_url = []

url = "https://www.linkedin.com/jobs/search/?currentJobId=3723993973&f_F=cnsl%2Cstra&f_I=11&keywords=consulting&origin=JOB_SEARCH_PAGE_JOB_FILTER&sortBy=R"
driver.get(url)
sleep(2)

try:
    jobsCountText = driver.find_element(By.CLASS_NAME, 'results-context-header__new-jobs').text
    jobsCount = jobsCountText.split()[0][1:].replace(",", "")
    print(jobsCount)
    sleep(3)
except:
    print('Excepiton')

for jobIndex in range(1, int(jobsCount)+1):

    if (jobIndex % 25 == 0):
        driver.execute_script("scroll(0, document.body.scrollHeight);")
        show_button = driver.find_element(By.CLASS_NAME, 'infinite-scroller__show-more-button')
        driver.execute_script("arguments[0].click();", show_button)
        sleep(3)

    elements = driver.find_element(By.CLASS_NAME, 'jobs-search__results-list')

    try:
        job = elements.find_element(By.CSS_SELECTOR, 'li:nth-of-type('+str(jobIndex)+')')
        link = job.find_element(By.TAG_NAME, 'a').get_attribute('href')
        url_key = "in.linkedin"
        
        if url_key in link:
            link = link.replace(url_key,"linkedin")
        
        
        jobs_url.append([16,link])
        if jobIndex > 500: 
            break
            
    except Exception as ex:
        print('Exception in li')
        break
    
    mycursor.execute("select distinct app_type from job_product where status = 'active'")
    records = mycursor.fetchall()
    list1 = []
            
    for rec in records: 
        list1.append(rec[0])

    # collect all data

jobs_arr = []
job_arr = []    

# Jobs count in array
print('jobs count final')
print(len(jobs_url))

# sql_for_skill = "select skill from scrapper_skills where cat in("+skillSet[url[0]]+")"
sql_for_skill = "select skill from scrapper_skills where cat in(16)"
skl = pd.read_sql(sql_for_skill,mydb)

i = 0
for url in jobs_url :
        if i == 20:
            break
        i+=1
        if url not in list1 :   
            try:
                res = requests.get(url[1])
                bs = bs4.BeautifulSoup(res.text,"html.parser")
                try:
                    cat = url[0]
                    try : 
                     title = bs.find('h1',{'class' :'top-card-layout__title'}).text
                    except:
                     title = bs.find('h1',{'class' :'jobs-unified-top-card__job-title'}).text
                    
                    custom_exp = [0,15]
                    try : 
                        first_span_tag = bs.find('ul', class_='description__job-criteria-list').find('span')
                        
                        if first_span_tag:
                            span_exp = first_span_tag.get_text(strip=True)
                            if span_exp.startswith("Internship"):
                                custom_exp = [0,1]
                            elif span_exp.startswith(("Executive", "Associate")):
                                custom_exp = [2,5]
                            elif span_exp.startswith("Entry level") :
                                custom_exp = [0,2]  
                            elif span_exp.startswith("Mid-Senior level") :
                                custom_exp = [5,10]       
                            elif span_exp.startswith("Director"):
                                custom_exp = [10,15]   
                            else :
                                custom_exp = [0,15]  
                        else:
                            print("Span tag not found.")    
                    except:
                        print("Span tag not found.")   
                    
                    title = title.strip().replace("'", "")
                    temp_title = title.strip().replace("'", "").lower()
                    print(title)


                    try:
                        post_url = bs.find('a',{'class':'sign-up-modal__company_webiste'})
                        new_url = post_url.get('href')
                        job_link = requests.get(new_url)

                        job_url = job_link.url
                        job_url = job_url.strip().replace("'", "")
                        if any(keyword in job_url for keyword in not_allowed):
                            continue
                    except :
                        job_url = ''

                    location = bs.find('span',{'class' :'topcard__flavor--bullet'}).text
                    try:
                        company = bs.find('a',{'data-tracking-control-name' :'public_jobs_topcard-org-name'}).text
                    except :
                        company = bs.find('span',{'class' :'topcard__flavor'}).text

                    desc = bs.find('div',{'class' :'show-more-less-html__markup'})
                
                    try:
                        job_exp = find_experience(desc,title)
                    except Exception as ex:
                        job_exp = custom_exp

                    if len(job_exp) == 0 or str(job_exp[1]) >= '15':
                        job_exp = custom_exp

                    skills = get_skills(desc,skl,title)
                
                    desc = str(desc).strip().replace("'", "")
                    location = location.strip().replace("'", "")
                    company = company.strip().replace("'", "")
                    
                    # f.write("External URL: "+job_url+"\n")
                    # f.write("Title: "+title+"\n")
                    # f.write("linkedin URL: "+url[1]+"\n")
                    # f.write("location: " + location+"\n")
                    # f.write("skills: " + skills+"\n")
                    # f.write("Exp : " + str(job_exp)+"\n")
                
                    # f.write("\n\n")

                except Exception as ex:
                    print('\n')
                    continue
            except Exception as ex:
                continue
            temp_job_arr = [title,desc,job_url,company,location,skills,job_exp,functional_area["consulting"]]
            jobs_arr.append(temp_job_arr)
 
    
job_url_dict = {}
unique_job_arr = []

print(len(jobs_arr))

for job in jobs_arr:
    job_url = job[2]
    if job_url not in job_url_dict:
     job_url_dict[job_url] = True
     unique_job_arr.append(job)


jobs_arr = unique_job_arr
jobsDf = pd.DataFrame(jobs_arr)
THRESHOLD = 10
best_match = \
    jobsDf[3].apply(lambda x: process.extractOne(x, compUni['name'],
                                                    score_cutoff=THRESHOLD))
i = 0
for found, score, matchrow in best_match:
                if score > 80:
                    jobs_arr[i][3]=compUni['id'][matchrow]
                i+=1

query = 'INSERT INTO `job_product` (product_name,description,company_id,app_type,location,city,f_area,user_id,status,featured,product_type,country,salary_max,salary_min,free,phone,application_url,emails,gender,as_per_comp,hide_salary,work_pref,view,p_graduate,u_graduate,experience_min,experience_max,c_level,created_at,expire_date,job_type,validity,created_via,upload,skills) VALUES '
current_date = datetime.now()
end_date = current_date + timedelta(days=120) # Adding 5 days.
created_at = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
expire = end_date.strftime("%Y-%m-%d %H:%M:%S")
created_at_company = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

if len(jobs_arr) > 0 :
    for job in jobs_arr : 
        company = type(job[3]).__name__
        # print(company)
        if company != 'int64' :
            company_query="INSERT INTO job_companies_new (user_id,name,status,created_at) VALUES(1,'"+str(job[3])+"','1','"+created_at_company+"')"
            mycursor.execute(company_query)
            mydb.commit()
            compUni.add(str(job[3]))
            job[3] = mycursor.lastrowid
        
        query  += "('" +  str(job[0]) + "','" + str(job[1]) + "','"+str(job[3])+"','"+str(job[2])+"','"+str(job[4])+"','"+str(job[4])+"','"+str(job[7])+"','1','active','0','4','India','5000000','100000','0','0','0','contact@jobaaj.com','No Preferences','1','1','Work from Office','0','52','40','"+str(job[6][0])+"','"+str(job[6][1])+"','20','"+created_at+"','"+expire+"','free','90','upload','linkedin','"+str(job[5])+"'),"
            
    
    query = query[:-1]
    # print(query)
    mycursor.execute(query)
    # # query = "INSERT INTO `job_indexapi` (job_id,api_status) SELECT id,1 FROM `job_product` WHERE `created_via`='upload' and upload='linkedin' ORDER BY `id` DESC LIMIT "+str(mycursor.rowcount)
    mydb.commit()  
    # query = ''
          



f.close()
f2.close()
driver.close()       
