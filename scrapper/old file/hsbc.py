import requests
from bs4 import BeautifulSoup
from collections import Counter
import re
import pandas as pd
from datetime import date,timedelta,datetime
import mysql.connector


# mydb = mysql.connector.connect(
#     host="",
#     username="",
#     password="",
# )

# skl = pd.read('SELECT * from job_skills' + mydb)

# response = requests.get("https://ey.com")

# print(response.text)

# i=0

# set={}

# while i != 10 :
#     set[i]=1
    
#     i=i+1
    
# print (set)

# print("next line")

# bs= BeautifulSoup(response.text, "html.parser")

# cont= bs.findAll('a')

# for cont in cont:
    # print(cont)

# for cont in cont :
    # links= cont.select('.twitter')
    
    # print(links)


# print(cont)


req_array = ["Assurance","Consulting","Strategy+and+Transactions","TAX"]

# mydb = mysql.connector.connect(
#     host = "localhost",
#     database = "mydb1",
#     user = "root",
#     password = ""
# )

# mycursor = mydb.cursor(buffered=True)

# mycursor.execute("select distinct app_type from job_product where company_id = 762")

# records = mycursor.fetchall()
# list1 = []

# skl = pd.read_sql("select * from job_skills", mydb)

# for rec in records: 
#     list1.append(rec[0])


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
            response = requests(weburl)
            bs = BeautifulSoup(response.text,"html.parser")
            jobs = bs.find_all('a','link link--chevron')
            
            # print(bs)
            if len == 0 :
                break
            
            # temp =  Counter(jobs)
            # jobs = [*temp]
            
            # for job in jobs : 
            #     url = 'https://mycareer.hsbc.com' + jobs.get('href')
            #     if url not in list1 :
            #         res = requests.get(url)
            #         bs = BeautifulSoup(res.text,'html.parser').text
            #         title = bs.find('h2',{'class':'banner__text__title banner__text__title--0'}).text
            #         location = bs.find('div',{'class' : 'article__content__view__field__value'}).text
            #         posted = bs.find('div',{'class','article__content__view__field__value'}).text
            #         desc = bs.find('div',{'class','article__content__view__field__value'})
            #         job_url = url
            #         i=i+1
            #         j=0
                    
            #         print(title)
            #         desc = str(desc).replace("'","")
            #         desc = str(desc).replace("'","")
            #         title = str(title).replace("'","")
            #         location = str(location).replace("'","")
            #         job_arr = [title.strip,desc,job_url,location.strip()]
                    
            #     else : 
            #         print("duplicate")
                
            count = count + 10
                
        except Exception as ex :
            print(ex)
            break
                
        
            print ("exception")

