import requests
import pandas as pd
import bs4
from collections import Counter
import mysql.connector
from datetime import datetime,timedelta,date
import re

from bs4 import BeautifulSoup
 


# cat_array = ["Assurance","Consulting","Strategy+and+Transactions","TAX"]


# mydb = mysql.connector.connect(host = "15.206.16.152", database= "nishtyainfotech_jobaaj", user = "nishtyainfotech_jobaaj", password = "9k,w8IvdPGrL")  

# mycursor = mydb.cursor(buffered=True)

# mycursor.execute("select distinct app_type from job_product where company_id = 762")

# records = mycursor.fetchall()
# list1 = []


# skl = pd.read_sql("select * from job_skills",mydb)


# for rec in records: 
#     list1.append(rec[0])

# category = {
#     "Assurance" : "1,2,3,4,6,7,8",
#     "Consulting" : "6,7,8",
#     "Strategy+and+Transactions" : "2,3,5,6,7,8",
#     "TAX" : "1,3,6,7,4"
# }

# functional_area = {
#     "Assurance" : "2",
#     "Consulting" : "16",
#     "Strategy+and+Transactions" : "5",
#     "TAX" : "3"
# }

# for cat in cat_array :
#         count = 0 
#         i = 0 

list1 = []

jobs_arr = []
job_arr = [[]]
count = 0  
while True : 
 try :
    template = "https://careers.ey.com/search/?optionsFacetsDD_country=IN&optionsFacetsDD_customfield1={}&startrow={}"
    weburl = template.format('Assurance',count)
    response = requests.get(weburl)
    bs = bs4.BeautifulSoup(response.text,"html.parser")
    jobs = bs.find_all('a','jobTitle-link')

    if len(jobs)==0 : 
        break

    temp = Counter(jobs)
    jobs = [*temp]


    for job in jobs: 
        
        url = 'https://careers.ey.com'+job.get('href')
        url = 'https://careers.ey.com/ey/job/Bengaluru-Executive-Director-Core-Audit-GDS-Assurance-KA-560037/802770101/'
        if url not in list1:
            res = requests.get(url)
            bs = bs4.BeautifulSoup(res.text,"html.parser")
            try : 
                title = bs.find('div',{'class' :'fontalign-left'}).text
                # location = bs.find('span',{'data-careersite-propertyid' :'city'}).text
                # posted = bs.find('span',{'data-careersite-propertyid' :'date'}).text
                desc = bs.find('span',{'class' :'jobdescription'})

                # job_url = url
                # i=i+1
                # j=0
                try :
                        strr = re.sub("\s\s+", " ", desc.text.lower())
                        strr = re.sub("\s\s+", " ", strr)
                        print(url)
                        try : 
                            exp = strr.find("year")
                            
                            
                            if exp != -1 : 
                                print('raw') 
                                #print(exp)
                                expirence = ''
                                for k in range(-9, 0):
                                    expirence+=strr[exp+k]
                               

                                print(strr[exp])
                                digits = '-'.join(filter(str.isdigit, expirence))
                                digits = digits.split("-")

                                
                                
                                if len(digits) == 1:
                                    digits = [digits[0],int(digits[0])+2]

                                if len(digits) == 3 :
                                    digits = [digits[0],digits[1]+''+digits[2]]
                                if len(digits) == 4 :
                                    digits = [digits[0] + '' + digits[1],digits[2]+''+digits[3]]  
                                
                                
                                if digits[0] == '1' and int(digits[1]) >= 4 :
                                    digits = [digits[0]+''+digits[1],10+int(digits[1])+2]


                                if digits[0] == '1' and digits[1] == '0' :
                                    digits = [digits[0]+''+digits[1],10+int(digits[1])+2]   

                            else : 
                                if 'Manager' in title :
                                    digits = ['4','8']
                                elif 'Senior' in title :
                                    digits = ['5','10']
                                else :
                                    digits = ['0','1']
                        except : 
                            
                            exp = strr.find("year",strr.find("year")+1)
                            
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

                                
                            else : 
                                if 'Manager' in title :
                                    digits = ['4','8']
                                    # jexp = [3,15]
                                elif 'Senior Analyst' in title: 
                                    digits = ['5','8']
                                else :
                                    digits = ['0','1']


                        print(digits)
                        desc = str(desc).replace("At EY, you’ll have the chance to build a career as unique as you are, with the global scale, support, inclusive culture and technology to become the best version of you. And we’re counting on your unique voice and perspective to help EY become even better, too. Join us and build an exceptional experience for yourself, and a better working world for all.","")
                        desc = str(desc).split("EY | Building a better working world")
                        file1 = open("ey.txt", "a")  # append mode
                        file1.write(desc[0])
                        file1.close()
                    
                        # jexp = []

                        # try:
                        #     expirence = int(expirence.replace("-",""))
                        #     exp = [int(i) for i in str(expirence)]
                        #     if len(exp)==1 : 
                        #         jexp = [0,exp[0]]
                        #     else :
                        #         jexp = [exp[0],exp[1]]

                        # except:
                        #     try:
                        #         print(expirence)
                        #         expirence = int(expirence.replace("to",""))
                                
                                
                        #         exp = [int(i) for i in str(expirence)]
                        #         if len(exp)==1 : 
                        #             print(exp)
                        #             jexp = [0,exp[0]]
                        #         else :
                        #             jexp = [exp[0],exp[1]]
                        #     except:
                        #         if 'Manager' in title :
                        #             jexp = [3,15]
                        #         else :
                        #             jexp = [0,25]

                    


                        


                        #print(jexp)  

                        # if jexp[1] == 25 :
                        #     break
                        # delimiters = ":-"," ","-","\/","/",".","\,","!","?","'s","<br>"
                        # regexPattern = '|'.join(map(re.escape, delimiters))
                        # neww = re.split(regexPattern, strr)

                        my_str = ''

                        # for si in neww:
                        # print(i)
                        # print(len(skl.loc[skl['skill'] == f'{i}']))
                        #     if(len(skl.loc[skl['skill'] == f'{si}']=='True')>0):
                        #         if si not in my_str:
                        #             my_str+=si
                        #             my_str+=','

                        # new_str = re.sub(",,",",",my_str)
                        # new_str = re.sub(",,",",",new_str)
                        # new_str = new_str.strip(",")

                        # break
                        # skills =  my_str[:-1]
                except Exception as ex :
                    print(ex)       
                    print('Exception')       
                

                desc = str(desc).replace("'","")
                desc = str(desc).replace("'","")
                title = str(title).replace("'","")
                # location = str(location).replace("'","")
                # job_arr = [title.strip(),desc,'job_url',location.strip(),'skills',jexp]
                # jobs_arr.append(job_arr)          
            except : 
                continue
        
        else :
            print('Duplicate')
        
        break
    count = count+25
    break

 except Exception as ex: 
    print('Scarpping Complete!')
    break





        # if len(jobs_arr) > 0 :
        #     query = 'INSERT INTO `job_product` (product_name,description,company_id,app_type,location,city,skills,f_area,category,user_id,status,featured,product_type,country,salary_max,salary_min,free,phone,application_url,emails,gender,as_per_comp,hide_salary,work_pref,view,p_graduate,u_graduate,experience_min,experience_max,c_level,created_at,expire_date,job_type,validity,created_via,upload) VALUES '
        #     for job in jobs_arr :
        #         #print(job)
        #         current_date = datetime.now()
        #         end_date = current_date + timedelta(days=90) # Adding 5 days.
        #         expire = end_date.strftime("%Y-%m-%d %H:%M:%S")
        #         query  += "('" +  str(job[0]) + "','" + str(job[1]) + "','762','"+str(job[2])+"','"+str(job[3])+"','"+str(job[3])+"','"+str(job[4])+"','"+functional_area[cat]+"','"+category[cat]+"','1','active','0','4','India','5000000','100000','0','0','0','contact@jobaaj.com','No Preferences','1','1','Work from Office','0','52','40','"+str(job[5][0])+"','"+str(job[5][1])+"','20','"+str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+"','"+expire+"','free','90','upload','EY'),"
        



        
        #     query = query[:-1]
        #     print(query)
        #     mycursor.execute(query)
        #     query = ''
        #     mydb.commit()

        # else :
        #     print('No Records!')



    


# mycursor.close()
# mydb.close()
# exit()



    
    