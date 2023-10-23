from selenium import webdriver
from time import sleep
import requests
import bs4
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from collections import Counter
import mysql.connector
from datetime import datetime,timedelta,date
import pandas as pd
import re


options = Options()
  
options.headless = True
  
driver = webdriver.Chrome(options=options)

cat_array = ["Data%20Science"]

mydb = mysql.connector.connect(host = "15.206.16.152", database= "nishtyainfotech_jobaaj", user = "nishtyainfotech_jobaaj", password = "9k,w8IvdPGrL")  
#mydb = mysql.connector.connect(host = "15.206.16.152", database= "nishtyainfotech_ccd", user = "nishtyainfotech_ccd", password = "YGdz270RlQeN")  
mycursor = mydb.cursor(buffered=True)

mycursor.execute("select distinct app_type from job_product where company_id = 763")

records = mycursor.fetchall()
list1 = []

# for rec in records: 
#     list1.append(rec[0])




def getExp(exp,strr):
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
    
def getSkills(desc,skl,title):
    strr = re.sub("\s+", " ", desc.text.lower())
    my_str = ''

    patterns = []
    pattern_start = r'(?:\s|^)'
    pattern_end = r'(?:[,./\s]|$)'
    for skill in skl['skill']:
        patterns.append(re.compile(pattern_start + re.escape(skill) + pattern_end))

    my_str = ''
    for pattern in patterns:
        if pattern.search(strr) or pattern.search(title.lower()):
            matched_skill = pattern.pattern[len(pattern_start):-len(pattern_end)].strip().replace('\\', '')
            my_str += matched_skill + ','
                            
    return  my_str[:-1] 


catValues = {
   "Data%20Science" : "Data Science",
}

functional_area = {
   "Data%20Science":"12",
}

skillSet = {
   "Data%20Science":"12",
}

  

jobs_arr = []
job_arr = [[]]

for cat in cat_array: 
    limit = 0

    main_url = "https://jobs.citi.com/search-jobs/{}/India/287/1/2/1269750/22/79/50/2"
    main_url = main_url.format(cat)

    sq = "select distinct skill from scrapper_skills where cat in("+skillSet[cat]+")"
    skl = pd.read_sql(sq,mydb)

    while True :
        driver.get(main_url)
        jobs = driver.find_element(By.ID,'search-results-list')
        job_arr = jobs.find_elements(By.TAG_NAME,'li')
        
            
        for job in job_arr :
            limit += 1
            try:
                url = job.find_element(By.TAG_NAME,'a').get_property('href')
                if url not in list1 :
                    res = requests.get(url)
                    bs = bs4.BeautifulSoup(res.text, "html.parser")
                    try :
                        job_data = bs.find('section', {'class': 'job-description'})

                        title = job_data.find('h1').text
                        
                        location = job_data.find_all('span', {'class': 'job-info__item'})[1]
                        desc = job_data.find('span', {'class': 'job-description2'})
                        job_url = url

                        
                        try :
                            strr = re.sub("\s+", " ", desc.text.lower())
                            try : 
                                exp = strr.find("year")
                                digits = getExp(exp,strr)        
                            except : 
                                exp = strr.find("year",strr.find("year")+1)
                                digits = getExp(exp,strr)

                        except Exception as ex :
                            # print(ex)       
                            print('Exception from Exp')

                        skills = getSkills(desc,skl,title)+","+ catValues[cat].lower()
                        

                        desc = str(desc).replace("'", "")
                        title = title.strip()
                        location = str(location.text).replace("Location(s)", "")
                        job_exp = [int(digits[0]),int(digits[1])]

                        job_skeleton = [title,desc,job_url,location,functional_area[cat],skills,job_exp]
                        jobs_arr.append(job_skeleton)

                        print(url)
                        print(title)
                        print('skills : ',end =" ")
                        print(skills) 
                        print('Exp : ',end =" ")
                        print(digits) 
                        print('Functional Area  : ',end =" ")
                        print(str(functional_area[cat]))
                        # print(re.sub("\s+"," ",desc.text.lower()))

                        f = open("citi.txt", "a")
                        f.write(url+"\n")
                        f.write(title+"\n")
                        f.write("skills: " + skills+"\n")
                        f.write("Exp : " + str(job_exp)+"\n")
                        f.write("Functional : " + str(functional_area[cat])+"\n\n")
                        f.write("\n")

                        sleep(2)
                    except : 
                        continue
                else :
                    print('duplicate')    
            except Exception as er:
                print(er)

        if(limit>=25):
            break


        try: 
            next_btn = driver.find_element(By.CLASS_NAME,'next')
            sleep(1)
            wait(driver,20).until(EC.element_to_be_clickable(next_btn))
            driver.execute_script("arguments[0].click()",next_btn)
            sleep(3)
        except Exception as err:
            print('+++++++++++++++++++++')
            print(err)
            break

        # if len(jobs_arr) > 0 :
        #         query = 'INSERT INTO `job_product` (product_name,description,company_id,app_type,location,city,j_role,f_area,category,user_id,status,featured,product_type,country,salary_max,salary_min,free,phone,application_url,emails,gender,as_per_comp,hide_salary,work_pref,view,p_graduate,u_graduate,experience_min,experience_max,c_level,created_at,expire_date,job_type,validity,created_via,upload) VALUES '
        #         for job_s in jobs_arr :
        #             #print(job)
        #             current_date = datetime.now()
        #             end_date = current_date + timedelta(days=90) # Adding 5 days.
        #             expire = end_date.strftime("%Y-%m-%d %H:%M:%S")
        #             query  += "('" +  str(job_s[0]) + "','" + str(job_s[1]) + "','763','"+str(job_s[2])+"','"+str(job_s[3])+"','"+str(job_s[3])+"','','"+functional_area[cat]+"','"+category[cat]+"','1','active','0','4','India','5000000','100000','0','0','0','contact@jobaaj.com','No Preferences','1','1','Work from Office','0','52','40','0','25','20','"+str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+"','"+expire+"','free','90','upload','Citi'),"
            
            
        #         query = query[:-1]
        #         mycursor.execute(query)
        #         print('----------------------------------------------')
        #         query = ''
        #         job_arr = []
        #         jobs_arr = []
        #         mydb.commit()

  

# close browser after our manipulations
driver.close()






# jobs = bs.find('section',{'id':'search-results-list'}).find_all('li')





    
    