from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from collections import Counter
import mysql.connector
from datetime import datetime,timedelta
from selenium.webdriver.common.keys import Keys

cat_array = ["Account Servicing","Accounting/Finance/Audit/Risk","Asset Management","Credit","Compliance","Investment Banking","Legal","Product Management","Real Estate Finance","Sales/Trading/Research","Wealth Management"]


# mydb = mysql.connector.connect(host = "15.206.16.152", database= "nishtyainfotech_ccd", user = "nishtyainfotech_ccd", password = "YGdz270RlQeN")  
mydb = mysql.connector.connect(host = "15.206.16.152", database= "nishtyainfotech_jobaaj", user = "nishtyainfotech_jobaaj", password = "9k,w8IvdPGrL")  

mycursor = mydb.cursor(buffered=True)

mycursor.execute("select distinct app_type from job_product where company_id = 284136")
records = mycursor.fetchall()
list1 = []
for rec in records: 
    list1.append(rec[0])


options = Options()
  
#options.headless = True
  
driver = webdriver.Chrome(options=options)
  

category = {
    cat_array[0] : "1,2,3,4,6,7",
    cat_array[1] : "1,2,3,4,6,7",
    cat_array[2] : "1,2,3,4,6,7",
    cat_array[3] : "1,2,3,4,6,7",
    cat_array[4] : "1,2,3,4,6,7",
    cat_array[5] : "6,7",   
    cat_array[6] : "1,2,3,4,6,7",
    cat_array[7] : "6,7",
    cat_array[8] : "6,7",
    cat_array[9] : "6,7",
}

functional_area = {
    cat_array[0] : "6",
    cat_array[1] : "1",
    cat_array[2] : "11",
    cat_array[3] : "1",
    cat_array[4] : "2",
    cat_array[5] : "5",
    cat_array[6] : "13",
    cat_array[7] : "11",
    cat_array[8] : "11",
    cat_array[9] : "11",
}


for cat in cat_array: 
   
    val = 0

    main_url = "https://jpmc.fa.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1001/requisitions?keyword={}&location=India"
    main_url = main_url.format(cat)

    jobs_arr = []
    job_arr = [[]]

    driver.get(main_url)


    while True:
       
        jobs =   wait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "joblist-grid")))
        if val == 0:
           val = int(driver.find_element(By.CLASS_NAME,'search-results-title-job-count').text)

        if val <= len(job_arr) :
            print('Lopp has Break')
            break  
            
        html = driver.find_element(By.TAG_NAME,'html')
        html.send_keys(Keys.PAGE_DOWN)
        job_arr.append(jobs.find_elements(By.TAG_NAME,'li'))
        
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
    for job in job_arr:
        
        try:
            job_single = []
            url = job.find_element(By.TAG_NAME,'a')
            if url not in list1 :
                wait(driver,10).until(EC.element_to_be_clickable(url))
            
                try : 
                    try : 
                        element = driver.find_element(By.CLASS_NAME,'oj-dialog')
                        driver.execute_script("""var element = arguments[0];element.parentNode.removeChild(element);""",element)
                    except : 
                        print()
                    
                    driver.execute_script("arguments[0].click()",url)
                    single_job = wait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "job-elements-wrapper")))
                    title = single_job.find_element(By.TAG_NAME,'h2').text
                    location = single_job.find_element(By.CLASS_NAME,'primary-location').text
                    desc = str(driver.find_element(By.CLASS_NAME,'details').get_attribute("innerHTML"))
                    job_url = url.get_property('href')
                    title = str(title).replace("'", "")
                    desc = str(desc).replace("'", "")
                    title = str(title).replace("'", "")
                    location = str(location).replace("'", "")
                    job_single = [title.strip(), desc, job_url, location.strip()]
                    jobs_list.append(job_single)
                    print(title)
                    sleep(3)
                except :
                     print('No Job')
        except Exception as er:
            print(er)
        print()


    if len(jobs_list) > 0  :
            query = 'INSERT INTO `job_product` (product_name,description,company_id,app_type,location,city,j_role,f_area,category,user_id,status,featured,product_type,country,salary_max,salary_min,free,phone,application_url,emails,gender,as_per_comp,hide_salary,work_pref,view,p_graduate,u_graduate,experience_min,experience_max,c_level,created_at,expire_date,job_type,validity,created_via,upload) VALUES '
            i = 0
            for job_s in jobs_list :
                #print(job)
                i= i+1
                if i > 40 :
                    break
                current_date = datetime.now()
                end_date = current_date + timedelta(days=90) # Adding 5 days.
                expire = end_date.strftime("%Y-%m-%d %H:%M:%S")
                query  += "('" +  str(job_s[0]) + "','" + str(job_s[1]) + "','284136','"+str(job_s[2])+"','"+str(job_s[3])+"','"+str(job_s[3])+"','','"+functional_area[cat]+"','"+category[cat]+"','1','active','0','4','India','5000000','100000','0','0','0','contact@jobaaj.com','No Preferences','1','1','Work from Office','0','52','40','0','25','20','"+str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+"','"+expire+"','free','90','upload','jpmorgen'),"

        

            query = query[:-1]
            print(query)
            mycursor.execute(query)
            query = ''
            mydb.commit()



    # close browser after our manipulations
driver.close()




# jobs = bs.find('section',{'id':'search-results-list'}).find_all('li')





    
    