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
from datetime import datetime,timedelta
from selenium.webdriver.common.keys import Keys


mydb = mysql.connector.connect(host = "15.206.16.152", database= "nishtyainfotech_ccd", user = "nishtyainfotech_ccd", password = "G+G-WkSHohEI")  

mycursor = mydb.cursor(buffered=True)

mycursor.execute("select distinct app_type from job_product where company_id = 284136")

records = mycursor.fetchall()

list1 = []

for rec in records: 
    list1.append(rec[0])


job_role = {
    "Tax" : "44",
}

category = {
    "Tax" : "1,3,6,7,4",
}

functional_area = {
    "Tax" : "3",
}

options = Options()
  
# options.headless = True
  
driver = webdriver.Chrome(options=options)
  

cat_array = ["Tax"]


main_url = "https://jpmc.fa.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1001/requisitions?keyword={}&location=Singapore"
main_url = main_url.format('treasury')

jobs_arr = []
job_arr = [[]]

driver.get(main_url)




for cat in cat_array: 
    val = 0
    while True: 
        jobs =   wait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "joblist-grid")))
        if val == 0:
           val = int(driver.find_element(By.CLASS_NAME,'search-results-title-job-count').text)

        if val <= len(job_arr) :
            print('Lopp has Break')
            break  
            
        html = driver.find_element(By.TAG_NAME,'html')
        html.send_keys(Keys.PAGE_DOWN)
        print(val)
        # driver.execute_script("window.scrollTo("+str(s)+",1000)")
        # s = s+25
        job_arr.append(jobs.find_elements(By.TAG_NAME,'li'))
        print(len(job_arr))
        try : 
            next_btn = driver.find_element(By.CLASS_NAME,'search-results-load-more-btn')
            sleep(4)
            wait(driver,10).until(EC.element_to_be_clickable(next_btn))
            driver.execute_script("arguments[0].click()",next_btn)
        except : 
            print('')

    print('ENDED')

    job_arr = jobs.find_elements(By.TAG_NAME,'li')
    print(len(job_arr))

    jobs_list = []
    for job in job_arr :
        try:
            job_single = []
            url = job.find_element(By.TAG_NAME,'a')
            wait(driver,10).until(EC.element_to_be_clickable(url))
           
            try : 
                element = driver.find_element(By.CLASS_NAME,'oj-dialog')
                driver.execute_script("""var element = arguments[0];element.parentNode.removeChild(element);""",element)
            except : 
                print('not found')

            driver.execute_script("arguments[0].click()",url)
            single_job = wait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "job-elements-wrapper")))
            title = single_job.find_element(By.TAG_NAME,'h2').text
            location = single_job.find_element(By.CLASS_NAME,'primary-location').text
            desc = str(driver.find_element(By.CLASS_NAME,'details').get_attribute("innerHTML"))
            job_url = url.get_property('href')
            title = str(title).replace("'", "")
            location = str(location).replace("'", "")
            job_single = [title.strip(), desc, job_url, location.strip()]
            jobs_list.append(job_single)
            print(title)
            sleep(3)
        except Exception as er:
            print(er)
        print()


    if len(jobs_list) > 0 :
            query = 'INSERT INTO `job_product` (product_name,description,company_id,app_type,location,city,j_role,f_area,category,user_id,status,featured,product_type,country,salary_max,salary_min,free,phone,application_url,emails,gender,as_per_comp,hide_salary,work_pref,view,p_graduate,u_graduate,experience_min,experience_max,c_level,created_at,expire_date,job_type,validity,created_via,upload) VALUES '
            for job_s in jobs_list :
                #print(job)
                current_date = datetime.now()
                end_date = current_date + timedelta(days=90) # Adding 5 days.
                expire = end_date.strftime("%Y-%m-%d %H:%M:%S")
                query  += "('" +  str(job_s[0]) + "','" + str(job_s[1]) + "','284136','"+str(job_s[2])+"','"+str(job_s[3])+"','"+str(job_s[3])+"','"+job_role[cat]+"','"+functional_area[cat]+"','"+category[cat]+"','1','active','0','4','India','5000000','100000','0','0','0','contact@jobaaj.com','No Preferences','1','1','Work from Office','0','52','40','0','25','20','"+str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+"','"+expire+"','free','90','upload','jpmorgen'),"

        

            query = query[:-1]
            print(query)
            mycursor.execute(query)
            query = ''
            mydb.commit()



    # close browser after our manipulations
    driver.close()






# jobs = bs.find('section',{'id':'search-results-list'}).find_all('li')





    
    