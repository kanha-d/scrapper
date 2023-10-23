import requests
import bs4
from collections import Counter
import mysql.connector
from datetime import datetime,timedelta,date

#cat_array = ["tax","audit","assurance","consulting","data","finance"]
cat_array = ["finance","audit","tax"]


# mydb = mysql.connector.connect(host = "15.206.16.152", database= "nishtyainfotech_ccd", user = "nishtyainfotech_ccd", password = "G+G-WkSHohEI")  

# mycursor = mydb.cursor(buffered=True)

# mycursor.execute("select distinct app_type from job_product where company_id = 909")

# records = mycursor.fetchall()
list1 = []


# for rec in records: 
#     list1.append(rec[0])



job_role = {
    cat_array[0] : "44",
    cat_array[1] : "7",
    cat_array[2] : "59",
}

category = {
    cat_array[0] : "1,3,6,7,4",
    cat_array[1]: "1,2,3,4,6,7,8",
    cat_array[2] : "6,7,8",
}

functional_area = {
    cat_array[0] : "3",
    cat_array[1] : "4",
    cat_array[2] : "4",
}



for cat in cat_array :
        count = 0 
        i = 0

        jobs_arr = []
        job_arr = [[]]
        while count == 0  : 
            try :
                template = "https://careers.statestreet.com/global/en/search-results?keywords={}&from={}&s=1"
                weburl = template.format(cat,count)
                response = requests.get(weburl)
                bs = bs4.BeautifulSoup(response.text,"html.parser")
                jobs = bs.find('script',{'type':'text/javascript'})
                #print(jobs)
                jobs = str(jobs).replace('<script type="text/javascript">/*&lt;!--*/ var phApp = phApp || ',"")           
                jobs = str(jobs).replace('; /*--&gt;*/</script>',"")           
                # jobs = [jobs]
                print(type(jobs))
                f = open("demofile2.txt", "w")
                f.write(jobs)
                f.close()   
                # for job in jobs : 
                #    print(job["applyUrl"])


               
                
               
                
                # if len(jobs)==0 : 
                #     break

                # temp = Counter(jobs)
                # jobs = [*temp]
            

                # for job in jobs: 
                #     url = 'https://jobsindia.deloitte.com/'+job.get('href')
                #     if url not in list1:
                #         res = requests.get(url)
                #         bs = bs4.BeautifulSoup(res.text,"html.parser")
                #         title = bs.find('span',{'data-careersite-propertyid' :'title'}).text
                #         location = bs.find('span',{'data-careersite-propertyid' :'city'}).text
                #         #posted = bs.find('span',{'data-careersite-propertyid' :'date'}).text
                #         desc = bs.find('span',{'class' :'jobdescription'})
                #         job_url = url
                #         i=i+1
                #         desc = str(desc).replace("'","")
                #         job_arr = [title.strip(),desc,job_url,location.strip()]
                #         jobs_arr.append(job_arr)
                #         print(title)
                #         print(count)
                    
                    
                #     else :
                #         print('Duplicate')
                    
                count = count+10
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
        #         query  += "('" +  str(job[0]) + "','" + str(job[1]) + "','909','"+str(job[2])+"','"+str(job[3])+"','"+str(job[3])+"','"+job_role[cat]+"','"+functional_area[cat]+"','"+category[cat]+"','1','pending','0','4','India','5000000','100000','0','0','0','contact@jobaaj.com','No Preferences','1','1','Work from Office','0','52','40','0','25','20','"+str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+"','"+expire+"','free','90','upload','Deloitte'),"
        



        
        #     query = query[:-1]
        #     print(query)
        #     mycursor.execute(query)
        #     query = ''
        #     mydb.commit()

        # else :
        #     print('No Records!')



    


# mycursor.close()
# mydb.close()
exit()




    
    