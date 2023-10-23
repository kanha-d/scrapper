from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from collections import Counter
import mysql.connector
from datetime import datetime,timedelta
import re
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from scrapper_functions import *
import shutup; shutup.please()


# ######################################
option = Options()
#option.add_argument("--headless")
option.add_argument("--disable-infobars")
option.add_argument("start-maximized")
option.add_argument("--disable-extensions")
# Pass the argument 1 to allow and 2 to block
option.add_experimental_option(
    "prefs", {"profile.default_content_setting_values.notifications": 1}
)

driver = webdriver.Chrome(ChromeDriverManager().install())
action = ActionChains(driver)
driver.maximize_window()


comp_id = 799
upload = "Kpmg"
db = mysql.connector.connect(host = "15.206.16.152", database= "nishtyainfotech_jobaaj", user = "nishtyainfotech_jobaaj", password = "9k,w8IvdPGrL")  
cursor = db.cursor(buffered=True)

list1 = []
# pass company id to fetch all app_type
list1 = fetch_app_type(cursor,comp_id)

cat_array = {
    "quantanalytics":"300000086249650",
    "refrencedata":"300001586035600",
    "controller":"300000086249994",
    "clientdata":"300001586035466",
    "creditrisk":"300000086152757",
    "product":"300000086144020",
    "financialanalysis":"300000086152826",
    "analysts":"300000086153065",
    "fundservicing":"300001586035594",
    "businessanalysis":"300000086152685"
}

functional_area = {
    "quantanalytics":"12",
    "refrencedata":"14",
    "controller":"4",
    "clientdata":"7",
    "creditrisk":"6",
    "product":"5",
    "financialanalysis":"4",
    "analysts":"4",
    "fundservicing":"5",
    "businessanalysis":"4"
}

skillSet = {
    "quantanalytics":"12",
    "refrencedata":"14",
    "controller":"4",
    "clientdata":"7",
    "creditrisk":"6",
    "product":"5",
    "financialanalysis":"4",
    "analysts":"4",
    "fundservicing":"5",
    "businessanalysis":"4"
}

for cat in cat_array: 

    jobs_count = 0
    loop_run = 0
    jobs_arr = []
    job_arr = []
    jobs_url = []
    template = "https://ejgk.fa.em2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/requisitions?keyword=accounting&mode=location"
    main_url = template.format(cat_array[cat])
    driver.get(main_url)
    sleep(5)

    sq = "select distinct skill from scrapper_skills where cat in("+skillSet[cat]+")"
    skl = pd.read_sql(sq,db)

    if jobs_count == 0:
        number_text = driver.find_element(By.CLASS_NAME,"search-filters__counter").text
        digits = re.findall(r'\d+', number_text)
        jobs_count = int(digits[0])
    
    jobs = wait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "jobs-list__list")))

    for job_index in range(1,jobs_count+1):
        if(job_index%25==0):
            driver.execute_script("scroll(0, document.body.scrollHeight);")
            sleep(10)
        try:
            job = jobs.find_element(By.CSS_SELECTOR,'ul li:nth-of-type('+str(job_index)+')')
            div = job.find_element(By.TAG_NAME,'div')
            link = div.find_element(By.CLASS_NAME, 'job-list-item__link').get_attribute('href')
            jobs_url.append(link)
            f = open("kpmg-links.txt","a")
            f.write(link+" "+str(job_index)+"\n")
            f.close()
        except Exception as ex:
            print('Exception in li')
            print(ex)
        
    # print('ENDED')

    print(len(jobs_url))

    count = 0
    for url in jobs_url:
        count+=count
        if count>20: 
         break
        try:
            if url not in list1 :
                driver.get(url)
                sleep(3)
                single_job = driver.find_element(By.CLASS_NAME, "cc-section__content")
                title = single_job.find_element(By.CLASS_NAME,'job-details__title').text
                location = single_job.find_element(By.CLASS_NAME,'job-details__subtitle').text
                desc = driver.find_element(By.CLASS_NAME,'job-details__description-content')
                job_url = url

                digits = find_experience(desc,title)
                skills = get_skills(desc,skl,title)

                desc = str(desc.get_attribute("innerHTML")).replace("'", "")
                title = str(title).replace("'", "").strip()
                location = str(location).replace("'", "").strip()
                job_exp = [int(digits[0]),int(digits[1])]

                job_arr = [title,desc,job_url,location,functional_area[cat],skills,job_exp]
                jobs_arr.append(job_arr)


                print(url)
                print(title)
                # print('skills : ',end =" ")
                # print(skills) 
                # print('Exp : ',end =" ")
                # print(digits) 
                # print('Functional Area  : ',end =" ")
                # print(str(functional_area[cat]))
                # print(desc)
                # print(re.sub("\s+"," ",desc.text.lower()))

                f = open("kpmg.txt", "a")
                f.write(url+"\n")
                f.write(title+"\n")
                f.write("skills: " + skills+"\n")
                f.write("Exp : " + str(job_exp)+"\n")
                f.write("Functional : " + str(functional_area[cat])+"\n\n")
                f.write("\n")
                # f.close()
                
                sleep(3)
        except Exception as er:
            print('No Job')
            print(er)
        
    # store_jobs(db,cursor,jobs_arr,comp_id,upload)


# close browser after our manipulations
driver.close()




    