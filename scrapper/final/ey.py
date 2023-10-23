import requests
import pandas as pd
import bs4
from collections import Counter
import mysql.connector
from datetime import datetime,timedelta,date
import re
from bs4 import BeautifulSoup

from scrapper_functions import *

comp_id = 762
upload = 'EY'
db = mysql.connector.connect(host = "15.206.16.152", database= "nishtyainfotech_jobaaj", user = "nishtyainfotech_jobaaj", password = "9k,w8IvdPGrL")  
cursor = db.cursor(buffered=True)

list1 = []
# pass company id to fetch all app_type
list1 = fetch_app_type(cursor,comp_id)


cat_array = ["TAX","Assurance","Consulting","All","Strategy+and+Transactions","CBS-Finance-Data","CBS-Finance-Treasury","CBS-Finance-Accounting","CBS-Legal"]
# cat_array = ["Consulting"]

cat_inner = {
    "TAX":"",
    "Assurance":"Audit",
    "Consulting":"Audit",
    "All":"",
    "Strategy+and+Transactions":"Investment Banking",
}

catValues = {
   "TAX" : "TAX",
   "Assurance" : "Internal Audit",
   "Consulting" : "Consulting",
   "All" : "All",
   "Strategy+and+Transactions":"Strategy and Transactions",

   "CBS-Finance-Data":"Data",
   "CBS-Finance-Treasury":"Treasury",
   "CBS-Finance-Accounting":"Accounting",

   "CBS-Legal":"Legal",
}

functional_area = {
   "TAX" : "3",
   "Assurance" : "2",
   "Consulting" : "2",
   "All" : "11",
   "Strategy+and+Transactions":"5",

   "CBS-Finance-Data":"12",
   "CBS-Finance-Treasury":"10",
   "CBS-Finance-Accounting":"1",

   "CBS-Legal":"14",
}

skillSet = {
   "TAX" : "3,4",
   "Assurance" : "2",
   "Consulting" : "2",
   "All" : "11",
   "Strategy+and+Transactions":"5,4",
   
   "CBS-Finance-Data":"12",
   "CBS-Finance-Treasury":"10",
   "CBS-Finance-Accounting":"1",

   "CBS-Legal":"14",
}

# check in title
tax_keywords_to_remove = [".net","acr","tdo","payroll","pas","finance","accounting","hrt","talent","ttt","ems","r2r","sl","technology","operation","law","experience","bts_","ops","go","delivery"]
audit_keywords_to_remove = ["architect","sustainability","financial","staff","tmt","actuarial"]
consulting_keywords_to_remove = ["staff","cyber","technology","technical","cns"]
all_keywords_to_remove = ["bt_fs"]
strategy_keywords_to_remove = ["ia","tse","project"]
CBSlegal_keywords_to_add = ["lawyer","law","legal","contract","contracting"]


for cat in cat_array :
    count = 0 
    i = 0
    limit = 0

    jobs_arr = []
    job_arr = [[]]

    sq = "select distinct skill from scrapper_skills where cat in("+skillSet[cat]+")"
    skl = pd.read_sql(sq,db)

    while True : 
        try :
            forCBS = cat.split("-")
            if(len(forCBS)>0 and len(forCBS)==3):
                template = "https://careers.ey.com/ey/search/?q={}&optionsFacetsDD_country=IN&optionsFacetsDD_customfield1={}&startrow={}"
                weburl = template.format(forCBS[1],forCBS[0],count)
            elif(len(forCBS)>0 and len(forCBS)==2):
                template = "https://careers.ey.com/ey/search/?q={}&optionsFacetsDD_country=IN&optionsFacetsDD_customfield1={}&startrow={}"
                weburl = template.format(forCBS[1],forCBS[0],count)
            else:
                if cat_inner[cat]=="":
                    template = "https://careers.ey.com/search/?optionsFacetsDD_country=IN&optionsFacetsDD_customfield1={}&startrow={}"
                    weburl = template.format(cat,count)
                else:
                    template = "https://careers.ey.com/ey/search/?q={}&optionsFacetsDD_country=IN&optionsFacetsDD_customfield1={}&startrow={}"
                    weburl = template.format(cat_inner[cat],cat,count)

            response = requests.get(weburl)
            bs = bs4.BeautifulSoup(response.text,"html.parser")
            jobs = bs.find_all('a','jobTitle-link')

            if len(jobs)==0 : 
                break

            temp = Counter(jobs)
            jobs = [*temp]
        

            for job in jobs: 
                limit += 1 
                url = 'https://careers.ey.com'+job.get('href')
                if url not in list1:
                    res = requests.get(url)
                    try:
                        bs = bs4.BeautifulSoup(res.text,"html.parser")
                        title = bs.find('div',{'class' :'fontalign-left'}).text

                        if cat=="TAX" and any(keyword in title.lower() for keyword in tax_keywords_to_remove):
                            continue

                        elif (cat=="Assurance" and 
                            (
                                not any(keyword in title.lower() for keyword in ["assurance", "compliance"]) or 
                                (
                                    any(keyword in title.lower() for keyword in ["assurance", "compliance"]) and 
                                    any(keyword in title.lower() for keyword in audit_keywords_to_remove)
                                )
                            )):
                                continue

                        elif (cat=="Consulting" and 
                            (
                                not any(keyword in title.lower() for keyword in ["risk", "audit"]) or 
                                (
                                    any(keyword in title.lower() for keyword in ["risk", "audit"]) and 
                                    any(keyword in title.lower() for keyword in consulting_keywords_to_remove)
                                )
                            )):
                                continue

                        elif cat=="All" and not any(keyword in title.lower() for keyword in all_keywords_to_remove):
                            continue

                        elif cat=="Strategy+and+Transactions" and any(keyword in title.lower() for keyword in strategy_keywords_to_remove):
                            continue

                        elif cat=="CBS-Finance-Data" and not any(keyword in title.lower() for keyword in ["data"]):
                            continue

                        elif cat=="CBS-Finance-Treasury" and not any(keyword in title.lower() for keyword in ["treasury"]):
                            continue

                        elif cat=="CBS-Finance-Accounting":
                            if any(keyword in title.lower() for keyword in ["accounting"]) and any(keyword in title.lower() for keyword in ["operations"]):
                                continue
                            elif any(keyword in title.lower() for keyword in ["operations"]):
                                continue
                            elif not any(keyword in title.lower() for keyword in ["accounting"]):
                                continue

                        elif cat=="CBS-Legal" and not any(keyword in title.lower() for keyword in CBSlegal_keywords_to_add):
                            continue


                        location = bs.find('span',{'data-careersite-propertyid' :'city'}).text
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

                        # f = open("ey.txt", "a")
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
        except Exception as ex: 
            print('Scrapping Complete!')
            break
        # break

    # store fetched jobs
    store_jobs(db,cursor,jobs_arr,comp_id,upload)


cursor.close()
db.close()
exit()



    
    