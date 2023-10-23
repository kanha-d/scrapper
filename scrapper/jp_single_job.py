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
from selenium.webdriver.common.keys import Keys
import re
import pandas as pd
from scrapper_functions import *

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
driver = webdriver.Chrome(options=option)
# ######################################
action = ActionChains(driver)
driver.maximize_window()


comp_id = 284136
upload = "JPMorgan"
db = mysql.connector.connect(host = "15.206.16.152", database= "nishtyainfotech_jobaaj", user = "nishtyainfotech_jobaaj", password = "9k,w8IvdPGrL")  
cursor = db.cursor(buffered=True)

list1 = []
# pass company id to fetch all app_type
# list1 = fetch_app_type(cursor,comp_id)


cat_array = [
    "lending services",
    "trading lifecycle",
    "financial analysis",
    "client data",
    "business analaysis",
    "controller",
    "payements lifecycle",
    "fund servicing",
    "product",
    "program & project management ",
    "data management",
    "trading services",
    "quant analytics",
    "analytics solutions & delivery",
    "product development",
    "reference data",
    "risk analytics/modeling",
    "client operations management",
    "program management ",
    "control officers",
    "program management",
    "operating risk & control mgt",
    "analysts ",
    "client service",
    "business management",
    "project management",
    "credit risk ",
    "general management & ops",
    "counsel",
    "data doc & trans processing",
    "fraud",
    "asset servicing",
    "client advisory ",
    "process improvement",
    "risk reporting",
    "onboarding",
]
cat_array = ["lending services"]

cat_id = {
    "lending services":"300001568270660",
    "trading lifecycle":"300001586035618",
    "financial analysis":"300000086152826",
    "client data":"300001586035466",
    "business analaysis":"300000086152685",
    "controller":"300000086249994",
    "payements lifecycle":"300001586035378",
    "fund servicing":"300001586035594",
    "product":"300000086144020",
    "program & project management ":"300007929924867",
    "data management":"300000086144003",
    "trading services":"300000921822354",
    "quant analytics":"300000086249650",
    "analytics solutions & delivery":"300000086250134",
    "product development":"300000086249543",
    "reference data":"300001586035600",
    "risk analytics/modeling":"300000086153256",
    "client operations management":"300001586035338",
    "program management ":"300000086152512",
    "control officers":"300000086249991",
    "program management":"300000086152512",
    "operating risk & control mgt":"300000086153038",
    "analysts ":"300000086153065",
    "client service":"300000086249881",
    "business management":"300000086152593",
    "project management":"300000086251909",
    "credit risk ":"300000086152757",
    "general management & ops":"300000086152904",
    "counsel":"300000086250680",
    "data doc & trans processing":"300000086153325",
    "fraud":"300000086250654",
    "asset servicing":"300001586035427",
    "client advisory ":"300000086143853",
    "process improvement":"300007929924879",
    "risk reporting":"300000086143856",
    "onboarding":"300000086152607",
}

catValues = {
   "lending services":"lending services",
    "trading lifecycle":"trading lifecycle",
    "financial analysis":"financial analysis",
    "client data":"client data",
    "business analaysis":"business analaysis",
    "controller":"controller",
    "payements lifecycle":"payements lifecycle",
    "fund servicing":"fund servicing",
    "product":"product",
    "program & project management ":"program & project management ",
    "data management":"data management",
    "trading services":"trading services",
    "quant analytics":"quant analytics",
    "analytics solutions & delivery":"analytics solutions & delivery",
    "product development":"product development",
    "reference data":"reference data",
    "risk analytics/modeling":"risk analytics/modeling",
    "client operations management":"client operations management",
    "program management ":"program management ",
    "control officers":"control officers",
    "program management":"program management",
    "operating risk & control mgt":"operating risk & control mgt",
    "analysts ":"analysts ",
    "client service":"client service",
    "business management":"business management",
    "project management":"project management",
    "credit risk ":"credit risk ",
    "general management & ops":"general management & ops",
    "counsel":"counsel",
    "data doc & trans processing":"data doc & trans processing",
    "fraud":"fraud",
    "asset servicing":"asset servicing",
    "client advisory ":"client advisory ",
    "process improvement":"process improvement",
    "risk reporting":"risk reporting",
    "onboarding":"onboarding",
}

functional_area = {
    "lending services":"7",
    "trading lifecycle":"7",
    "financial analysis":"financial analysis",
    "client data":"client data",
    "business analaysis":"business analaysis",
    "controller":"controller",
    "payements lifecycle":"payements lifecycle",
    "fund servicing":"fund servicing",
    "product":"product",
    "program & project management ":"program & project management ",
    "data management":"data management",
    "trading services":"trading services",
    "quant analytics":"quant analytics",
    "analytics solutions & delivery":"analytics solutions & delivery",
    "product development":"product development",
    "reference data":"reference data",
    "risk analytics/modeling":"risk analytics/modeling",
    "client operations management":"client operations management",
    "program management ":"program management ",
    "control officers":"control officers",
    "program management":"program management",
    "operating risk & control mgt":"operating risk & control mgt",
    "analysts ":"analysts ",
    "client service":"client service",
    "business management":"business management",
    "project management":"project management",
    "credit risk ":"credit risk ",
    "general management & ops":"general management & ops",
    "counsel":"counsel",
    "data doc & trans processing":"data doc & trans processing",
    "fraud":"fraud",
    "asset servicing":"asset servicing",
    "client advisory ":"client advisory ",
    "process improvement":"process improvement",
    "risk reporting":"risk reporting",
    "onboarding":"onboarding",
}

skillSet = {
    "lending services":"7",
    "trading lifecycle":"7",
    "financial analysis":"financial analysis",
    "client data":"client data",
    "business analaysis":"business analaysis",
    "controller":"controller",
    "payements lifecycle":"payements lifecycle",
    "fund servicing":"fund servicing",
    "product":"product",
    "program & project management ":"program & project management ",
    "data management":"data management",
    "trading services":"trading services",
    "quant analytics":"quant analytics",
    "analytics solutions & delivery":"analytics solutions & delivery",
    "product development":"product development",
    "reference data":"reference data",
    "risk analytics/modeling":"risk analytics/modeling",
    "client operations management":"client operations management",
    "program management ":"program management ",
    "control officers":"control officers",
    "program management":"program management",
    "operating risk & control mgt":"operating risk & control mgt",
    "analysts ":"analysts ",
    "client service":"client service",
    "business management":"business management",
    "project management":"project management",
    "credit risk ":"credit risk ",
    "general management & ops":"general management & ops",
    "counsel":"counsel",
    "data doc & trans processing":"data doc & trans processing",
    "fraud":"fraud",
    "asset servicing":"asset servicing",
    "client advisory ":"client advisory ",
    "process improvement":"process improvement",
    "risk reporting":"risk reporting",
    "onboarding":"onboarding",
}

cat_array = ["lending services"]


jobs_url = ["https://jpmc.fa.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1001/job/210406295/?lastSelectedFacet=CATEGORIES&location=India&selectedCategoriesFacet=300001568270660"]

sq = "select distinct skill from scrapper_skills where cat in("+skillSet["lending services"]+")"
skl = pd.read_sql(sq,db)

for url in jobs_url:
    try:
        if url not in list1 :
            driver.get(url)
            sleep(2)
        
            single_job = driver.find_element(By.CLASS_NAME, "job-details")

            title = single_job.find_element(By.CSS_SELECTOR,'h2.job-details__title').text
            location = single_job.find_element(By.CSS_SELECTOR,'div.job-details__subtitle span').text
            desc = driver.find_element(By.CSS_SELECTOR,'div.job-details__description-content')
            job_url = url

            f = open("experience.txt", "a")
            
            f.write(desc.text.lower())
            f.close()


            digits = find_experience(desc,title)
            skills = get_skills(desc,skl,title)+","+ catValues["lending services"].lower()
            skills = remove_duplicates(skills)

            desc = str(desc.get_attribute("innerHTML")).replace("'", "")
            title = str(title).replace("'", "").strip()
            location = str(location).replace("'", "").strip()
            job_exp = [int(digits[0]),int(digits[1])]

            job_arr = [title,desc,job_url,location,functional_area["lending services"],skills,job_exp]
            # jobs_arr.append(job_arr)


            print(url)
            print(title)
            print('skills : ',end =" ")
            print(skills) 
            print('Exp : ',end =" ")
            print(digits) 
            print('Functional Area  : ',end =" ")
            print(str(functional_area["lending services"]))
            # print(desc)
            # print(re.sub("\s+"," ",desc.text.lower()))

           
            
            sleep(3)
    except Exception as er:
            print('No Job')
            print(er)





# close browser after our manipulations
driver.close()




    