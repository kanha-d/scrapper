import requests
import bs4
from collections import Counter
import mysql.connector
from datetime import datetime,timedelta,date
import re
import pandas as pd

#cat_array = ["TAX","Audit+%26+Assurance","Consulting","Enabling+Areas","Financial+Advisory","Internal+Firm+Services","Risk+Advisory"]
cat_array = ["TAX"]


# mydb = mysql.connector.connect(host = "localhost", database= "mydb13", user = "root", password = "")  
mydb = mysql.connector.connect(host = "15.206.16.152", database= "nishtyainfotech_jobaaj", user = "nishtyainfotech_jobaaj", password = "9k,w8IvdPGrL")  


mycursor = mydb.cursor(buffered=True)

mycursor.execute("select distinct app_type from job_product where company_id = 99")

records = mycursor.fetchall()
list1 = []

skl = pd.read_sql("select distinct skill from scrapper_skills where cat in (2,4)",mydb)


def getExp(exp):
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
    
def getSkills(desc):
    strr = re.sub("\s\s+", " ", desc.text.lower())
    strr = re.sub("\s\s+", " ", strr)
    my_str = ''


    for i in skl.index:
        skill  =  str(skl['skill'][i])
      
        pat1 = ' ' + re.escape(skill) + r'\n'
        pat2 = ' ' + re.escape(skill) + r' '
        pat3 = ' ' + re.escape(skill) + r','
        pat4 = ' ' + re.escape(skill) + r'/'
        pat5 = ' ' + re.escape(skill) + r' '
        pat6 = '\n' +re.escape(skill) + r'\n'
        pat7 = '\n' +re.escape(skill) + r' '
        pattern = re.compile(pat1 + '|' + pat2 + '|' + pat3 + '|' + pat4 + '|' + pat5 + '|' + pat6 + '|' + pat7)

        if pattern.search(strr) or pattern.search(title.lower()):
            my_str += skill.strip() + ','

       
        skills = my_str.split(",")
        skills = [*set(skills)]
        newskills = ','.join(str(s) for s in skills)
                            
    return  newskills[1:]



for rec in records: 
    list1.append(rec[0])



functional_area = {
   "TAX" : "3",
   "Audit+%26+Assurance" : "2",
   "Risk+Advisory" : "2",
   "Financial+Advisory" : "4"
}


skills = {
   "TAX" : "2",
   "Audit+%26+Assurance" : "2",
   "Risk+Advisory" : "2",
   "Financial+Advisory" : "4"
}


for cat in cat_array :
        count = 0 
        i = 0

        jobs_arr = []
        job_arr = [[]]
        while True  : 
            try :
                template = "https://jobsindia.deloitte.com/search/?q=&locationsearch=india&optionsFacetsDD_customfield2={}&startrow={}"
                weburl = template.format(cat,count)
                response = requests.get(weburl)
                bs = bs4.BeautifulSoup(response.text,"html.parser")
                jobs = bs.find_all('a','jobTitle-link')
            
                if len(jobs)==0 : 
                   break

                temp = Counter(jobs)
                jobs = [*temp]
            

                for job in jobs: 
                    url = 'https://jobsindia.deloitte.com/'+job.get('href')
                    if url not in list1:
                        res = requests.get(url)
                        try :
                            bs = bs4.BeautifulSoup(res.text,"html.parser")
                            title = bs.find('span',{'data-careersite-propertyid' :'title'}).text
                           
                            if cat=="Risk+Advisory" and "internal audit" not in title.lower():
                               continue

                            location = bs.find('span',{'data-careersite-propertyid' :'city'}).text
                            #posted = bs.find('span',{'data-careersite-propertyid' :'date'}).text
                            desc = bs.find('span',{'class' :'jobdescription'})
                            job_url = url

                        
                            i=i+1
                        
                            job_arr = [title.strip(),desc,job_url,location.strip()]
                            jobs_arr.append(job_arr)
                            
                            try :
                                    strr = re.sub("\s\s+", " ", desc.text.lower())
                                    strr = re.sub("\s\s+", " ", strr)
                                    try : 
                                            exp = strr.find("year")
                                            digits = getExp(exp)        
                                    except : 
                                            exp = strr.find("year",strr.find("year")+1)
                                            digits = getExp(exp)        
                                                    
                            except Exception as ex :
                                print('Exception from Exp')          
                                
                            # skills
                            
                            skills = getSkills(desc)
                            skills = skills+','+ cat.lower()
                           
                            print(url)
                            print(title)
                            print('skills : ',end =" ")
                            print(skills) 
                            print('Exp : ',end =" ")
                            print(digits) 
                            print('Functional Area  : ',end =" ")
                            #desc = str(desc).replace("'","")
                            title = str(title).replace("'","").strip()
                            location = str(location).replace("'","").strip()
                            job_exp = [int(digits[0]),int(digits[1])]
                            
                            job_arr = [title,desc,job_url,location,skills,job_exp]
                            jobs_arr.append(job_arr)


                            f = open("ey.txt", "a")
                            f.write(url+"\n")
                            f.write(title+"\n")
                            f.write("skills: " + skills+"\n")
                            f.write("Exp : " + str(job_exp)+"\n")
                            f.write("Functional : " + str(functional_area[cat])+"\n")
                            f.write("\n")
                        except: 
                            continue
                    else :
                        print('Duplicate')
                    
                count = count+25
            except: 
                print('Scarpping Complete!')
                break




        # if len(jobs_arr) > 0 :
        #     query = 'INSERT INTO `job_product` (product_name,description,company_id,app_type,location,city,j_role,f_area,category,user_id,status,featured,product_type,country,salary_max,salary_min,free,phone,application_url,emails,gender,as_per_comp,hide_salary,work_pref,view,p_graduate,u_graduate,experience_min,experience_max,c_level,created_at,expire_date,job_type,validity,created_via,upload) VALUES '
        #     for job in jobs_arr :
        #         #print(job)
        #         current_date = datetime.now()
        #         end_date = current_date + timedelta(days=90) # Adding 5 days.
        #         expire = end_date.strftime("%Y-%m-%d %H:%M:%S")
        #         query  += "('" +  str(job[0]) + "','" + str(job[1]) + "','909','"+str(job[2])+"','"+str(job[3])+"','"+str(job[3])+"','','"+functional_area[cat]+"','','1','active','0','4','India','5000000','100000','0','0','0','contact@jobaaj.com','No Preferences','1','1','Work from Office','0','52','40','0','25','20','"+str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+"','"+expire+"','free','90','upload','Deloitte'),"


        
        #     query = query[:-1]
        #     print(query)
        #     mycursor.execute(query)
        #     query = ''
        #     mydb.commit()

        # else :
        #     print('No Records!')



    


mycursor.close()
mydb.close()
exit()




