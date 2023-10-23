import requests
import bs4
from collections import Counter
import mysql.connector
from datetime import datetime, timedelta, date

cat_array = ["TAX"]

mydb = mysql.connector.connect(host="15.206.16.152", database="nishtyainfotech_ccd",
                               user="nishtyainfotech_ccd", password="G+G-WkSHohEI")

mycursor = mydb.cursor(buffered=True)

mycursor.execute("select distinct app_type from job_product where company_id = 1056")

records = mycursor.fetchall()
list1 = []


for rec in records:
    list1.append(rec[0])


job_role = {
    "TAX": "44",
}

category = {
    "TAX": "1,3,6,7,4",
}

functional_area = {
    "TAX": "3",
}


jobs_arr = []
job_arr = [[]]

try:
    weburl = "https://jobs.citi.com/job/mumbai/tax-specialist/287/43284179520"
    response = requests.get(weburl)
    bs = bs4.BeautifulSoup(response.text, "html.parser")
    jobs = bs.find_all('a', {'class': 'job-link'})
  
    temp = Counter(jobs)
    jobs = [*temp]
    for job in jobs:
        url = 'http://careers.tmf-group.com/'+job.get('href')
        if url not in list1:
            res = requests.get(url)
            bs = bs4.BeautifulSoup(res.text, "html.parser")
            job_data = bs.find('div', {'id': 'job-content'})
            title = job_data.find('h2').text
            desc = job_data.find('div', {'id': 'job-details'})
            location = job_data.find('span', {'class': 'location'}).text
            job_url = url
            desc = str(desc).replace("'", "")
            job_arr = [title.strip(), desc, job_url, location.strip()]
            jobs_arr.append(job_arr)
            print(title)

        else:
            print('Duplicate')

   
except: 
    print('Scarpping Complete!')





if len(jobs_arr) > 0 :
    query = 'INSERT INTO `job_product` (product_name,description,company_id,app_type,location,city,j_role,f_area,category,user_id,status,featured,product_type,country,salary_max,salary_min,free,phone,application_url,emails,gender,as_per_comp,hide_salary,work_pref,view,p_graduate,u_graduate,experience_min,experience_max,c_level,created_at,expire_date,job_type,validity,created_via,upload) VALUES '
    for job in jobs_arr :
        current_date = datetime.now()
        end_date = current_date + timedelta(days=90) # Adding 5 days.
        expire = end_date.strftime("%Y-%m-%d %H:%M:%S")
        query  += "('" +  str(job[0]) + "','" + str(job[1]) + "','1056','"+str(job[2])+"','"+str(job[3])+"','"+str(job[3])+"','"+job_role["TAX"]+"','"+functional_area["TAX"]+"','"+category["TAX"]+"','1','pending','0','4','India','5000000','100000','0','0','0','contact@jobaaj.com','No Preferences','1','1','Work from Office','0','52','40','0','25','20','"+str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+"','"+expire+"','free','90','upload','TMF'),"




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



    
    