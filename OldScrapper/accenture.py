import requests
import pandas as pd
import bs4
from collections import Counter
import mysql.connector
from datetime import datetime,timedelta,date

cat_array = ["TAX","Assurance","Consulting","Finance"]


mydb = mysql.connector.connect(host = "15.206.16.152", database= "nishtyainfotech_ccd", user = "nishtyainfotech_ccd", password = "G+G-WkSHohEI")  

mycursor = mydb.cursor(buffered=True)

mycursor.execute("select distinct app_type from job_product where company_id = 762")

records = mycursor.fetchall()
list1 = []


for rec in records: 
    list1.append(rec[0])



job_role = {
    "TAX" : "44",
    "Assurance" : "7",
    "Consulting" : "59",
    "Strategy+and+Transactions" : "32"
}

category = {
    "TAX" : "1,3,6,7,4",
    "Assurance" : "1,2,3,4,6,7,8",
    "Consulting" : "6,7,8",
    "Strategy+and+Transactions" : "2,3,5,6,7,8",
}

functional_area = {
    "TAX" : "3",
    "Assurance" : "4",
    "Consulting" : "4",
    "Strategy+and+Transactions" : "9",
}




for cat in cat_array :
        count = 0 
        i = 0

        jobs_arr = []
        job_arr = [[]]
        while True: 
            try :
                template = "https://www.accenture.com/in-en/careers/jobsearch?jk={}&sb=0&vw=0&is_rj=0&pg={}"
                weburl = template.format(cat,count)
                response = requests.get(weburl)
                bs = bs4.BeautifulSoup(response.text,"html.parser")
                jobs = bs.find_all('a','jobTitle-link')

            
                if len(jobs)==0 : 
                    break

                temp = Counter(jobs)
                jobs = [*temp]
            

                for job in jobs: 
                    url = 'https://careers.ey.com'+job.get('href')
                    if url not in list1:
                        res = requests.get(url)
                        bs = bs4.BeautifulSoup(res.text,"html.parser")
                        title = bs.find('div',{'class' :'fontalign-left'}).text
                        location = bs.find('span',{'data-careersite-propertyid' :'city'}).text
                        posted = bs.find('span',{'data-careersite-propertyid' :'date'}).text
                        desc = bs.find('span',{'class' :'jobdescription'})
                        job_url = url
                        i=i+1
                        desc = str(desc).replace("'","")
                        job_arr = [title.strip(),desc,job_url,location.strip()]
                        jobs_arr.append(job_arr)
                        print(title)
                        print(count)
                    
                    
                    else :
                        print('Duplicate')
                    
                count = count+25
            except: 
                print('Scarpping Complete!')
                break





        if len(jobs_arr) > 0 :
            query = 'INSERT INTO `job_product` (product_name,description,company_id,app_type,location,city,j_role,f_area,category,user_id,status,featured,product_type,country,salary_max,salary_min,free,phone,application_url,emails,gender,as_per_comp,hide_salary,work_pref,view,p_graduate,u_graduate,experience_min,experience_max,c_level,created_at,expire_date,job_type,validity,created_via,upload) VALUES '
            for job in jobs_arr :
                #print(job)
                current_date = datetime.now()
                end_date = current_date + timedelta(days=90) # Adding 5 days.
                expire = end_date.strftime("%Y-%m-%d %H:%M:%S")
                query  += "('" +  str(job[0]) + "','" + str(job[1]) + "','762','"+str(job[2])+"','"+str(job[3])+"','"+str(job[3])+"','"+job_role[cat]+"','"+functional_area[cat]+"','"+category[cat]+"','1','pending','0','4','India','5000000','100000','0','0','0','contact@jobaaj.com','No Preferences','1','1','Work from Office','0','52','40','0','25','20','"+str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+"','"+expire+"','free','90','upload','EY'),"
        



        
            query = query[:-1]
            print(query)
            mycursor.execute(query)
            query = ''
            mydb.commit()

        else :
            print('No Records!')



    


mycursor.close()
mydb.close()
exit()



    
    