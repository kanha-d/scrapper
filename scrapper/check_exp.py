import mysql.connector
import html2text
import re
from scrapper_functions import *
import en_core_web_sm
import shutup; shutup.please()


# Load the English language model
nlp = en_core_web_sm.load()

mydb = mysql.connector.connect(host = "15.206.16.152", database= "nishtyainfotech_jobaaj", user = "nishtyainfotech_jobaaj", password = "9k,w8IvdPGrL")  
mycursor = mydb.cursor(buffered=True)

# mycursor.execute("select experience_min,experience_max,description from job_product where upload = 'linkedin' order by id desc limit 0,50")
# mycursor.execute("select experience_min,experience_max,description,product_name,id from job_product where  experience_min = 0 and (experience_max = 25 or experience_max = 15) order by id desc limit 0,10000")
# mycursor.execute("select experience_min,experience_max,description,product_name,id from job_product where created_at > NOW() - INTERVAL 15 Day ")
# mycursor.execute("select experience_min,experience_max,description,product_name,id from job_product where id = 308363")

# Load the English language model

def extract_experience_level(job_description,expL):
    doc = nlp(job_description.lower())  # Convert to lowercase for case-insensitive matching
    
    # keywords = ["entry level", "junior", "intermediate", "mid-level", "experienced", "senior"]
    experience_level = None
    
    for exp in expL:
        keyword = exp[0]
        if keyword in job_description.lower():
            experience_level = [keyword,exp[1],exp[2]]
            break
    
    return experience_level

records = mycursor.fetchall()
list1 = []
expList = []

for rec in records: 
    try :
        textD = html2text.html2text(rec[2])
        job = [] 
        job = [rec[0],rec[1],textD,rec[3],rec[4]]
        list1.append(job)
    except :
        continue

mycursor.execute("select level,min,max from exp_level order by min asc")
experiences = mycursor.fetchall()

for e in experiences: 
    exp = [] 
    exp = [e[0],e[1],e[2]]  
    expList.append(exp)

for j in list1:

    job_description = j[2]
    title = j[3]
    job_description = title+" "+re.sub("\s+", " ", job_description.lower())
    
    digits = find_experience(job_description,title)
    print(digits)
    try : 
        min = int(digits[0])
        max = int(digits[1])
    except :
        min = 0
        max = 15

    if min >= 30 or (min == 0 and max==15): 
        # fetch experiece by keyword
        experience_level = extract_experience_level(job_description,expList)
        if experience_level:
            digits = [experience_level[1],experience_level[2]]
            print(f"Experience Level: {experience_level} Exp : {j[0]} - {j[1]}")
            print(f"https://www.jobaaj.com/job/job-details-{j[4]}\n\n")

        else:
            digits = ['3','8']

    print(digits)
    product_id = str(j[4])
    min = str(digits[0])
    max = str(digits[1])
    mycursor.execute("update job_product set experience_min = "+min+", experience_max = "+max+"  where id = "+product_id+"")

   
        

