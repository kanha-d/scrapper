from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from collections import Counter
import mysql.connector
from datetime import datetime,timedelta,date

cat_array = ["tax","Finance","Consulting","Strategy+and+Transactions"]

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
  

options = Options()
  
options.headless = True
  
driver = webdriver.Chrome(options=options)
  
url = "https://jobs.citi.com/search-jobs/FINANCE/India/287/1/2/1269750/22/79/50/2"
i=0
while True :
    
    driver.get(url)
    i=i+1
    jobs = driver.find_element(By.ID,'search-results-list')
    
    job_arr = jobs.find_elements(By.TAG_NAME,'li')

    for job in job_arr : 
        try:
            print(job.text)
        except:
            print('continue')
        print()

    try: 
      next_btn = driver.find_element(By.CLASS_NAME,'next')
      sleep(1)
      wait(driver,10).until(EC.element_to_be_clickable(next_btn))
      driver.execute_script("arguments[0].click()",next_btn)
      sleep(2)
    except Exception as err:
        print(err)
        break


    print('------------- Pagination '+ str(i) )



  
# close browser after our manipulations
driver.close()






# jobs = bs.find('section',{'id':'search-results-list'}).find_all('li')





    
    