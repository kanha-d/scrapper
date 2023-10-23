from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import shutup; shutup.please()
from scrapper_functions import *
import requests
import bs4
import mysql.connector
import pandas as pd

from time import sleep
from scrapper_functions import *

# ######################################
option = Options()
option.add_argument("--disable-infobars")
option.add_argument("start-maximized")
option.add_argument("--disable-extensions")
# Pass the argument 1 to allow and 2 to block
option.add_experimental_option(
    "prefs", {"profile.default_content_setting_values.notifications": 1}
)
driver = webdriver.Chrome(chrome_options=option, executable_path="./chromedriver.exe")
# ######################################
actions = ActionChains(driver)
driver.maximize_window()


mydb = mysql.connector.connect(
    host="15.206.16.152",
    user="nishtyainfotech_jobaaj",
    database="nishtyainfotech_jobaaj",
    password="9k,w8IvdPGrL"
)

mycursor = mydb.cursor(buffered=True)
mycursor.execute("select distinct app_type from job_product where company_id = 1185")

records = mycursor.fetchall()
list1 = []
for rec in records:
    list1.append(rec[0])



def findExp(title) : 
    exp = ['0','15']

    if "associate consultant" in title :
        exp = ['2','5']
    if 'consultant' in title :
        exp = ['3','6']   
    if 'junior' in title :
        exp = ['1','2']  
    if any(keyword in title for keyword in ["intern","trainee","part-time","summer"]) :
        exp = ['0','1']
    if 'senior' in title :
        exp = ['7','10']  

    return exp

# collect all urls
jobs_url = []

url = "https://www.bain.com/careers/find-a-role/?filters=areasofwork(1831443)"
driver.get(url)
sleep(2)



job_array =[]
jobs_array = [[]]

job_listings = driver.find_elements(By.CLASS_NAME, "card--role-results")

job_count_check = 0

sql_for_skill = "select skill from scrapper_skills where cat = 16"
skl = pd.read_sql(sql_for_skill,mydb)


for job_listing in job_listings:
    job_div = job_listing.find_element(By.CLASS_NAME, "card__content")
    j_title = job_div.find_element(By.TAG_NAME, "h4").text
    j_location = "Bengaluru"
    j_fun = "16"
    
    j_url = job_listing.find_element(By.TAG_NAME, "a").get_attribute("href")
    j_exp = findExp(j_title.lower().split())

    
    if j_url not in list1 : 
        job_count_check +=1
        response = requests.get(j_url)  
        # Parse the HTML content using BeautifulSoup
        
        soup = bs4.BeautifulSoup(response.content, "html.parser")
        j_description = soup.find("div", class_="title-with-rte-block__wrapper")
        
        j_skill =  remove_duplicates(get_skills(j_description,skl,j_title) + ",management consulting")
        j_description = str(j_description).replace("'","")
        j_title = str(j_title).replace("'","")

        job_arr = [j_title,j_description,j_url,j_location,j_fun,j_skill,j_exp]
        jobs_array.append(job_arr)


if job_count_check > 0: 
 store_jobs(mydb,mycursor,jobs_array,"1185","bain-company")
else : 
 print('No New Jobs Found!')


driver.close()       

