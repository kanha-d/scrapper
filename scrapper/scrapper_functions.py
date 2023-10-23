from collections import Counter
import re
from datetime import datetime,timedelta,date

def fetch_app_type(cursor,comp_id):

    cursor.execute("select distinct app_type from job_product where company_id = " + str(comp_id))

    records = cursor.fetchall()
    list1 = []
    for rec in records: 
        list1.append(rec[0])
    
    return list1

def remove_duplicates(skills):
    skills_array = skills.split(",")
    # now create dictionary using counter method
    # which will have strings as key and their
    # frequencies as value
    UniqW = Counter(skills_array)
    # joins two adjacent elements in iterable way
    skills = ",".join(UniqW.keys())
    return skills


def find_experience(desc,title):
    desc_str = re.sub("\s+", " ", desc.text.lower())
    all_digits = []
    digits = []
    try:
        matches1 = list(re.finditer('year', desc_str))
        matches2 = list(re.finditer('yrs', desc_str))
        matches = matches1 + matches2
        if len(matches)>0:
            for m in matches:
                
                exp = m.start()  
                
                digits = get_experience(exp,desc_str,title)
                all_digits.append(digits)
        else:
            digits = get_experience(-1,desc_str,title)
            all_digits.append(digits)
    except Exception as ex :
        print('Exception from Exp')

    if all_digits:
        digits = min(all_digits, key=lambda x: sum(int(i) for i in x if str(i).isdigit()))
    else:
        digits = ['0','15']
    
    return digits
    
def find_experience_text(desc,title):
    desc_str = re.sub("\s+", " ", desc.lower())
    all_digits = []
    digits = []
    try:
        matches1 = list(re.finditer('year', desc_str))
        matches2 = list(re.finditer('yrs', desc_str))
        matches = matches1 + matches2
        if len(matches)>0:
            for m in matches:
                
                exp = m.start()  
                
                digits = get_experience(exp,desc_str,title)
                all_digits.append(digits)
        else:
            digits = get_experience(-1,desc_str,title)
            all_digits.append(digits)
    except Exception as ex :
        print('Exception from Exp')

    if all_digits:
        digits = min(all_digits, key=lambda x: sum(int(i) for i in x if str(i).isdigit()))
    else:
        digits = ['0','15']
    
    return digits


def get_experience(exp,desc,title):
    
    if exp != -1 : 
        experience = ''
        for k in range(-20, -1):
            experience+=desc[exp+k]
        experience.strip()
        digits = re.findall(r'\d+', experience)

        if '+' in experience:
            temp = ''
            for dig in digits:
                temp = temp+''+dig
            digits = [temp.strip(),str(int(temp.strip())+2)]
        elif len(digits) == 1:
            digits = [digits[0],str(int(digits[0])+2)]
        elif len(digits) == 3 :
            digits = [digits[0],digits[1]+''+digits[2]]
        elif len(digits) == 4 :
            digits = [digits[0] + '' + digits[1],digits[2]+''+digits[3]]  
        
    else : 
        if 'Manager' in title :
            digits = ['4','8']
        elif 'AM' in title :
            digits = ['2','4']
        elif 'DM' in title :
            digits = ['3','6']
        elif 'SM' in title :
            digits = ['5','8']    
        elif any(keyword in title for keyword in ["Senior","Sr."]) :
            digits = ['4','10']
        elif any(keyword in title for keyword in ["Intern","Fresher"]):
            digits = ['0','1']
        else :
            digits = ['0','15']
        
    return digits


def get_skills(desc,skl,title):
    desc_str = re.sub("\s+", " ", desc.text.lower())
    my_str = ''

    patterns = []
    pattern_start = r'(?:\s|^)'
    pattern_end = r'(?:[,./\s]|$)'
    for skill in skl['skill']:
        patterns.append(re.compile(pattern_start + re.escape(skill) + pattern_end))

    my_str = ''
    for pattern in patterns:
        if pattern.search(desc_str) or pattern.search(title.lower()):
            matched_skill = pattern.pattern[len(pattern_start):-len(pattern_end)].strip().replace('\\', '')
            my_str += matched_skill + ','
                            
    return  remove_duplicates(my_str[:-1])



def store_jobs(db,cursor,jobs_arr,comp_id,upload):
    if len(jobs_arr) > 0 :
        query = "INSERT INTO `job_product` (product_name,description,company_id,app_type,location,city,f_area,user_id,status,featured,product_type,country,salary_max,salary_min,free,phone,application_url,emails,gender,as_per_comp,hide_salary,work_pref,view,p_graduate,u_graduate,experience_min,experience_max,c_level,created_at,expire_date,job_type,validity,created_via,upload,skills) VALUES "

        current_date = datetime.now()
        end_date = current_date + timedelta(days=120) # Adding 5 days.

        created_at = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        expire = str(end_date.strftime("%Y-%m-%d %H:%M:%S"))
        for job in jobs_arr :
          if not job: 
              continue
          else :
            #   job[0] = job[0].replace("'","\'")
            #   job[0] = job[0].replace(",","\,")
              job[1] = job[1].replace("'","\'")
              job[3] = job[3].replace("'","\'")
              job[5] = job[5].replace("'","\'")
              query  += "('" +  job[0] + "','" + str(job[1]) + "','"+str(comp_id)+"','"+str(job[2])+"','"+str(job[3])+"','"+str(job[3])+"','"+job[4]+"','1','active','0','4','India','5000000','100000','0','0','0','contact@jobaaj.com','No Preferences','1','1','Work from Office','0','52','40','"+str(job[6][0])+"','"+str(job[6][1])+"','20','"+created_at+"','"+expire+"','free','90','upload','"+upload+"','"+str(job[5])+"'),"

        
        try : 
            # f = open("hsbc.txt", "a")
            # f.write(query+"\n")
            query = query[:-1]
            cursor.execute(query)

            query = "INSERT INTO `job_indexapi` (job_id,api_status) SELECT id,1 FROM `job_product` WHERE `created_via`='upload'  and upload='"+upload+"' ORDER BY `id` DESC LIMIT "+str(cursor.rowcount)
            cursor.execute(query)

            query = ''
            db.commit()
        except Exception as ex :
            print('problem on posting')

         

    else :
        print('No Records!')


        