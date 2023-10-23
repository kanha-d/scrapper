import requests
from bs4 import BeautifulSoup
from collections import Counter
import re
import pandas as pd
from datetime import date,timedelta,datetime
import mysql.connector

mydb = mysql.connector.connect(host = "15.206.16.152", database= "nishtyainfotech_jobaaj", user = "nishtyainfotech_jobaaj", password = "9k,w8IvdPGrL")  
mycursor = mydb.cursor(buffered=True)


# skl = pd.read('SELECT * from job_skills' + mydb)

req_array = ["Assurance","Consulting","Strategy+and+Transactions","TAX"]

mycursor.execute("select distinct app_type from job_product where company_id = 762")

records = mycursor.fetchall()
list1 = []

skl = pd.read_sql("select * from job_skills", mydb)

for rec in records: 
    list1.append(rec[0])

list1 = []

category = {
    "Assurance" : "1,2,3,4,5,6,7,8",
    "consulting" : "6,7,8",
    "Strategy+and+Transactions" : "2,3,4,5,6,7,8",
    "TAX" : "3"
}

functional_area = {
    "Assurance" : "2",
    "Consulting" : "16",
    "Strategy+and+Transactions" : "5",
    "TAX" : "3"
}

for req in req_array :
    count = 0
    i=0
    
    job_array =[]
    jobs_array = [[]]
    
    while True :
        try : 
            template = "https://mycareer.hsbc.com/en_GB/external/SearchJobs/?1017=%5B67213%5D&1017_format=812&listFilterMode=1&pipelineOffset={}"
            weburl = template.format(count)
            response = requests.get(weburl)
            bs = BeautifulSoup(response.text,"html.parser")
            
            jobs = bs.find_all('a','link link--chevron')
       
            if len == 0 :
                break
            
            temp =  Counter(jobs)
            jobs = [*temp]
            hrefs = [link['href'] for link in jobs]
    
            for i,job in enumerate(hrefs, start=1) : 
                
                url = job
                if 1==1 :
                  
                    res = requests.get(url)
                    bs = BeautifulSoup(res.text,'html.parser')

                    title = bs.find('h2',{'class':'banner__text__title banner__text__title--0'}).text
                    location = bs.find_all('div',{'class' : 'article__content__view__field__value'})
                    loc = location[1].text.strip()

                    print(title)
                    print(loc)
                    # desc = bs.find('div',{'class','article__content__view__field__value'})
                    # job_url = url
                    # i=i+1
                    # j=0
                    
                   
                    # desc = str(desc).replace("'","")
                    # desc = str(desc).replace("'","")

                    f = open("hsbc.txt", "a")
                    f.write(url+"\n")
                    f.write(title+"\n")
                    # f.write(location+"\n")
                    # f.write("skills: " + skills+"\n")
                    # f.write("Exp : " + str(job_exp)+"\n")
                    # f.write("Functional : " + str(functional_area[cat])+"\n")
                    f.write("\n")
            
                    # title = str(title).replace("'","")
                    # location = str(location).replace("'","")
                    # job_arr = [title.strip,desc,job_url,location.strip()]
                    
                else : 
                    print("duplicate")
                
            count = count + 10
                
        except Exception as ex :
            print(ex)
            break
            print ("exception")

