from time import sleep
import requests
from bs4 import BeautifulSoup
from collections import Counter
import re
import pandas as pd
from datetime import date,timedelta,datetime
import mysql.connector
import shutup; shutup.please()
from lxml import html

from scrapper_functions import *

comp_id = 780
upload = 'HSBC'
mydb = mysql.connector.connect(host = "15.206.16.152", database= "nishtyainfotech_jobaaj", user = "nishtyainfotech_jobaaj", password = "9k,w8IvdPGrL")  
mycursor = mydb.cursor(buffered=True)

cat_array = [
    "%5B79332",
    "%5B79321",
    "%5B79322",
    "%5B79329",
    "%5B79338",
    
]
# "%5B79340"

mycursor.execute("select distinct app_type from job_product where company_id = 780")

records = mycursor.fetchall()
list1 = []

for rec in records: 
    list1.append(rec[0])

list1 = []
    
functional_area = {
    "%5B79332":"5",
    "%5B79321":"11",
    "%5B79322":"2",
    "%5B79329":"4",
    "%5B79338":"14",
    "%5B79340":"17"
}

functional_area_text = {
    "%5B79332":"Investment Banking",
    "%5B79321":"Asset",
    "%5B79322":"Audit",
    "%5B79329":"Finance",
    "%5B79338":"Risk",
    "%5B79340":"Strategy"
}

skillSet = {
    "%5B79332":"5",
    "%5B79321":"11",
    "%5B79322":"2",
    "%5B79329":"4",
    "%5B79338":"14",
    "%5B79340":"4"
}



skillSet_text = {
   "Investment" : "4",
   "Asset" : "2",
   "audit" : "3",
   "Finance" : "1",
   "Risk":"12",
   "Strategy":"5"
}

for cat in cat_array :
    count = 0
    i=0
    
    job_array =[]
    jobs_array = [[]]
    
    while count < 50 :
        try : 
            sql_for_skill = "select skill from scrapper_skills where cat in("+skillSet[cat]+")"
            skl = pd.read_sql(sql_for_skill,mydb)

            webUrl = f"https://mycareer.hsbc.com/en_GB/external/SearchJobs/?1017=%5B67213%5D&1017_format=812&1020={cat}%5D&1020_format=815&listFilterMode=1&pipelineRecordsPerPage={count}&#anchor__search-jobs"
            response = requests.get(webUrl)
            bs = BeautifulSoup(response.text,"html.parser")
            
            jobs = bs.find_all('a','link link--chevron')
       
            if len == 0 :
                break
            
            temp =  Counter(jobs)
            jobs = [*temp]
            hrefs = [link['href'] for link in jobs]
    
            for i,job in enumerate(hrefs, start=1) : 
                
                url = job
                if url not in list1 and url != 'https://mycareer.hsbc.com/en_GB/talentcommunity' and url != 'https://mycareer.hsbc.com/jobrecommendations/':
                    
                    res = requests.get(url)
                    bs = BeautifulSoup(res.text,'html.parser')
                    parsed_content = html.fromstring(res.content)
                    element = parsed_content.xpath('//*[@id="main-panel"]/div/div[1]/section[1]/div')[0]

                    title = bs.find('h2',{'class':'banner__text__title banner__text__title--0'}).text
                    data = bs.find_all('div',{'class' : 'article__content__view__field__value'})
                    desc_d = bs.find('div',{'id' : 'main-panel'})
                    desc = html.etree.tostring(element, encoding='unicode')

                    loc = ''
                    skills = ''
                    digits = ''

                    if data :
                        loc = data[1].text.strip()
                        print(url)
                        digits = find_experience(desc_d,title)
                        print(digits)
                        skills =  get_skills(desc_d,skl,title)

                    desc = str(desc).replace("'","")

                    title = str(title.strip()).replace("'","")
                    location = str(loc.strip()).replace("'","")
                    job_exp = [int(digits[0]),int(digits[1])]

                    if loc.strip() != '':
                     job_arr = [title,desc,url,loc.strip(),functional_area[cat],skills,job_exp]
                     jobs_array.append(job_arr)
                    sleep(2)
                else : 
                    print("duplicate")
                
            count = count + 10
                
        except Exception as ex :
            print(ex)
            break
            print ("exception")

    store_jobs(mydb,mycursor,jobs_array,comp_id,upload)
