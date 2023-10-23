import requests
import bs4
from collections import Counter
import mysql.connector
from datetime import datetime,timedelta,date
import re
import pandas as pd

from scrapper_functions import *

comp_id=909
upload = 'Deloitte'
# mydb = mysql.connector.connect(host = "localhost", database= "mydb13", user = "root", password = "")  
db = mysql.connector.connect(host = "15.206.16.152", database= "nishtyainfotech_jobaaj", user = "nishtyainfotech_jobaaj", password = "9k,w8IvdPGrL")  
cursor = db.cursor(buffered=True)

list1 = []
# pass company id to fetch all app_type
list1 = fetch_app_type(cursor,comp_id)



cat_array = ["TAX","Audit+%26+Assurance","Financial+Advisory","Risk+Advisory"]
# cat_array = ["Audit+%26+Assurance"]

catValues = {
   "TAX" : "TAX",
   "Audit+%26+Assurance" : "Audit & Assurance,A&A",
   "Risk+Advisory" : "Risk Advisory",
   "Financial+Advisory" : "Financial Advisory"
}

functional_area = {
   "TAX" : "3",
   "Audit+%26+Assurance" : "2",
   "Risk+Advisory" : "2",   
   "Financial+Advisory" : "4"
}


skillSet = {
   "TAX" : "3,4",
   "Audit+%26+Assurance" : "2",
   "Financial+Advisory" : "4",
   "Risk+Advisory" : "2",
}



for cat in cat_array :
    count = 0 
    i = 0
    limit = 0

    jobs_arr = []
    job_arr = [[]]
    sq = "select distinct skill from scrapper_skills where cat in("+skillSet[cat]+")"
    skl = pd.read_sql(sq,db)

    while True  :
        try :
            template = "https://jobsindia.deloitte.com/search/?q=&locationsearch=india&optionsFacetsDD_customfield2={}&startrow={}"
            weburl = template.format(cat,count)
            response = requests.get(weburl)
            bs = bs4.BeautifulSoup(response.text,"html.parser")
            jobs = bs.find_all('a','jobTitle-link')
        
            if len(jobs)==0 : 
                break

            temp = Counter(jobs)
            jobs = [*temp]
        

            for job in jobs: 
                # limit += 1 
                url = 'https://jobsindia.deloitte.com/'+job.get('href')
                if url not in list1:
                    res = requests.get(url)
                    try :
                        bs = bs4.BeautifulSoup(res.text,"html.parser")
                        title = bs.find('span',{'data-careersite-propertyid' :'title'}).text
                        
                        if cat=="Risk+Advisory" and not any(keyword in title.lower() for keyword in ["internal audit"]):
                            continue

                        if cat=="Risk+Advisory" and any(keyword in title.lower() for keyword in ["aic","r&ls","cyber","digital"]):
                            continue

                        if cat=="TAX" and any(keyword in title.lower() for keyword in ["technology","fp&a","f&a"]):
                            continue
                        
                        if cat=="Financial+Advisory" and "forensic" in title.lower():
                            continue

                        location = bs.find('span',{'data-careersite-propertyid' :'city'}).text
                        #posted = bs.find('span',{'data-careersite-propertyid' :'date'}).text
                        desc = bs.find('span',{'class' :'jobdescription'})
                        job_url = url

                        digits = find_experience(desc,title)
                        skills = get_skills(desc,skl,title)+","+ catValues[cat].lower()
                        skills = remove_duplicates(skills)

                        desc = str(desc).replace("'","")
                        title = str(title).replace("'","").strip()
                        location = str(location).replace("'","").strip()
                        job_exp = [int(digits[0]),int(digits[1])]
                        
                        job_arr = [title,desc,job_url,location,functional_area[cat],skills,job_exp]
                        jobs_arr.append(job_arr)
                        

                        # print(url)
                        # print(title)
                        # print('skills : ',end =" ")
                        # print(skills) 
                        # print('Exp : ',end =" ")
                        # print(digits) 
                        # print('Functional Area  : ',end =" ")
                        # print(str(functional_area[cat]))
                        # # print(re.sub("\s+"," ",desc.text.lower()))

                        # f = open("deloitte.txt", "a")
                        # f.write(url+"\n")
                        # f.write(title+"\n")
                        # f.write("skills: " + skills+"\n")
                        # f.write("Exp : " + str(job_exp)+"\n")
                        # f.write("Functional : " + str(functional_area[cat])+"\n\n")
                        # f.write("\n")
                        # f.close()
                    except: 
                        continue
                else :
                    print('Duplicate')

                # if(limit>=25):
                # break
            count = count+25
        except: 
            print('Scrapping Complete!')
            break

        # if(limit>=25):
        # break


    # store fetched jobs
    store_jobs(db,cursor,jobs_arr,comp_id,upload)


cursor.close()
db.close()
exit()




