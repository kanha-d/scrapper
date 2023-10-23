import mysql.connector
import html2text
import re
import en_core_web_sm

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


mydb = mysql.connector.connect(host = "15.206.16.152", database= "nishtyainfotech_jobaaj", user = "nishtyainfotech_jobaaj", password = "9k,w8IvdPGrL")  
mycursor = mydb.cursor(buffered=True)

mycursor.execute("select experience_min,experience_max,description,id from job_product where upload = 'linkedin' and experience_min = 0 and experience_max = 15  order by id desc limit 0,50")

# Load the English language model
nlp = en_core_web_sm.load()

records = mycursor.fetchall()
list1 = []
expList = []

for rec in records: 
    textD = html2text.html2text(rec[2])
    job = [] 
    job = [rec[0],rec[1],textD,rec[3]]
    list1.append(job)

mycursor.execute("select level,min,max from exp_level order by min asc")
experiences = mycursor.fetchall()

for e in experiences: 
    exp = [] 
    exp = [e[0],e[1],e[2]]  
    expList.append(exp)


for j in list1:
    job_description = j[2]
    job_description = re.sub("\s+", " ", job_description.lower())
    experience_level = extract_experience_level(job_description,expList)
    if experience_level:
        print(f"Experience Level: {experience_level} Exp : {j[0]} - {j[1]}")
        print(f"https://www.jobaaj.com/job/job-details-{j[3]}\n\n")

    else:
        print(f"Experience Level not Found . Exp : {j[0]} - {j[1]}")
        print(f"https://www.jobaaj.com/job/job-details-{j[3]}\n\n")

        # f = open("experience.txt", "a")
        # f.write(j[3]+"\n")
        # f.write("\n")
        # f.close()
        


