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

cat_array = ["Business Analysis","Compliance and Control","Data Science","Decision Management","Finance","Financial Reporting","Risk Management","Risk, Audit and Compliance"]

mydb = mysql.connector.connect(host = "15.206.16.152", database= "nishtyainfotech_ccd", user = "nishtyainfotech_ccd", password = "YGdz270RlQeN")  
mycursor = mydb.cursor(buffered=True)

category = {
    cat_array[0] : "7,8,6,3,2",
    cat_array[1] : "1,2,3,4,6,7",
    cat_array[2] : "6,8",
    cat_array[3] : "8,6",
    cat_array[4] : "1,2,3,4,6,7",
    cat_array[5] : "6,7",
    cat_array[6] : "1,2,3,4,6,7",
    cat_array[7] : "1,2,3,4,6,7",
}

functional_area = {
    cat_array[0] : "4",
    cat_array[1] : "2",
    cat_array[2] : "12",
    cat_array[3] : "16",
    cat_array[4] : "4",
    cat_array[5] : "4",
    cat_array[6] : "6",
    cat_array[7] : "2",
}



#mydb = mysql.connector.connect(host = "15.206.16.152", database= "nishtyainfotech_jobaaj", user = "nishtyainfotech_jobaaj", password = "9k,w8IvdPGrL")  

  
options = Options()
  
options.headless = True
  
driver = webdriver.Chrome(options=options)
  


jobs_arr = []
job_arr = [[]]

for cat in cat_array: 
    main_url = "https://jobs.citi.com/search-jobs/{}/India/287/1/2/1269750/22/79/50/2"
    main_url = main_url.format(cat)
    while True :
      
        driver.get(main_url)
        jobs = driver.find_element(By.ID,'search-results-list')
        job_arr = jobs.find_elements(By.TAG_NAME,'li')
        mycursor.execute("select distinct app_type from job_product where company_id = 763")
        records = mycursor.fetchall()
        list1 = []
        for rec in records: 
            list1.append(rec[0])
            
        print(list1)
        
        for job in job_arr :
            try:
                url = job.find_element(By.TAG_NAME,'a').get_property('href')
                if url not in list1 :
                    res = requests.get(url)
                    bs = bs4.BeautifulSoup(res.text, "html.parser")
                    try :
                        job_data = bs.find('section', {'class': 'job-description'})
                        title = job_data.find('h1').text
                        desc = job_data.find('span', {'class': 'job-description2'})
                        location = job_data.find_all('span', {'class': 'job-info__item'})[1]
                        job_url = url
                        location = str(location.text).replace("Location(s)", "")
                        desc = str(desc).replace("'", "")
                        job_skeleton = [title.strip(), desc, job_url, location.strip()]
                        jobs_arr.append(job_skeleton)
                        #print(title)
                        print(url)
                        sleep(2)
                    except : 
                     continue
                else :
                  print('duplicate')    
            except Exception as er:
                print(er)
            print()


        # try: 
        #     next_btn = driver.find_element(By.CLASS_NAME,'next')
        #     sleep(1)
        #     wait(driver,10).until(EC.element_to_be_clickable(next_btn))
        #     driver.execute_script("arguments[0].click()",next_btn)
        #     sleep(3)
        # except Exception as err:
        #     print(err)
        #     break

        if len(jobs_arr) > 0 :
                query = 'INSERT INTO `job_product` (product_name,description,company_id,app_type,location,city,j_role,f_area,category,user_id,status,featured,product_type,country,salary_max,salary_min,free,phone,application_url,emails,gender,as_per_comp,hide_salary,work_pref,view,p_graduate,u_graduate,experience_min,experience_max,c_level,created_at,expire_date,job_type,validity,created_via,upload) VALUES '
                for job_s in jobs_arr :
                    #print(job)
                    current_date = datetime.now()
                    end_date = current_date + timedelta(days=90) # Adding 5 days.
                    expire = end_date.strftime("%Y-%m-%d %H:%M:%S")
                    query  += "('" +  str(job_s[0]) + "','" + str(job_s[1]) + "','763','"+str(job_s[2])+"','"+str(job_s[3])+"','"+str(job_s[3])+"','','"+functional_area[cat]+"','"+category[cat]+"','1','active','0','4','India','5000000','100000','0','0','0','contact@jobaaj.com','No Preferences','1','1','Work from Office','0','52','40','0','25','20','"+str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+"','"+expire+"','free','90','upload','Citi'),"
            
            
                query = query[:-1]
                #print(query)
                mycursor.execute(query)
                print('----------------------------------------------')
                query = ''
                mydb.commit()


  
# close browser after our manipulations
driver.close()






# jobs = bs.find('section',{'id':'search-results-list'}).find_all('li')





    
    