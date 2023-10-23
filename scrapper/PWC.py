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
upload = 'PWC'
mydb = mysql.connector.connect(host = "15.206.16.152", database= "nishtyainfotech_jobaaj", user = "nishtyainfotech_jobaaj", password = "9k,w8IvdPGrL")  
mycursor = mydb.cursor(buffered=True)

cat_array = [
    "Finance"
]
# "%5B79340"

# mycursor.execute("select distinct app_type from job_product where company_id = 780")

# records = mycursor.fetchall()
# list1 = []

# for rec in records: 
#     list1.append(rec[0])

list1 = []

functional_area = {
    "Finance":"5"
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
    "Finance":"5",
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

            webUrl = f"https://www.pwc.in/careers/experienced-jobs/results.html?wdcountry=IND|BGD&wdjobsite=Global_Experienced_Careers&flds=jobreqid,title,location,los,specialism,industry,apply,jobsite,iso"
            response = requests.get(webUrl)
            bs = BeautifulSoup(response.text,"html.parser")

            table_body = bs.find('tbody')

            rows = table_body.find_all('tr')
                
            for row in rows:
                link = row.find('a', href=True)
                if link:
                    link_url = link['href']
                
                url = link_url
                if 1==1:
                
                    res = requests.get(url)
                    bs = BeautifulSoup(res.text,'html.parser')
                    parsed_content = html.fromstring(res.content)

                    print(url)
                    # title = bs.find('h2',{'class':'banner__text__title banner__text__title--0'}).text
                    # data = bs.find_all('div',{'class' : 'article__content__view__field__value'})
                    # desc_d = bs.find('div',{'id' : 'main-panel'})
                    # desc = html.etree.tostring(element, encoding='unicode')

                    # loc = ''
                    # skills = ''
                    # digits = ''

                    # if data :
                    #     loc = data[1].text.strip()
                    #     print(url)
                    #     digits = find_experience(desc_d,title)
                    #     print(digits)
                    #     skills =  get_skills(desc_d,skl,title)

                    # desc = str(desc).replace("'","")

                    # title = str(title.strip()).replace("'","")
                    # location = str(loc.strip()).replace("'","")
                    # job_exp = [int(digits[0]),int(digits[1])]

                    # if loc.strip() != '':
                    #  job_arr = [title,desc,url,loc.strip(),functional_area[cat],skills,job_exp]
                    #  jobs_array.append(job_arr)
                    # sleep(2)
                else : 
                    print("duplicate")
                
            count = count + 10
                
        except Exception as ex :
            print(ex)
            break
            print ("exception")

    # store_jobs(mydb,mycursor,jobs_array,comp_id,upload)
