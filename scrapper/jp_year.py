from collections import Counter
import re
from datetime import datetime,timedelta,date

desc ="The internship will run for 3 months, with the successful candidate placed in a role withi"
title ="Loan Credit Support - Team Member"


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
            digits = ['0','25']
        
    return digits

       
desc_str = re.sub("\s+", " ", desc)
all_digits = []
digits = []
try:
    matches = list(re.finditer('year', desc_str))

    if len(matches)>0:
        for m in matches:
            exp = m.start()    
            
            experience = ''
            for k in range(-20, -1):
                experience+=desc[exp+k]
            experience.strip()
            digits = re.findall(r'\d+', experience)
            print(experience)
            
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
            

            if 'months' in experience:
                digAr =  list(str(digits[1]))
                if len(digAr) > 1:
                 digits = [digits[0],digAr[0]+'.'+digAr[1]]
                else :
                 digits = [digits[0],digits[1]]
            all_digits.append(digits)
    else:
        print()
except Exception as ex :
    print('Exception from Exp')

    # if all_digits:
    #  digits = max(all_digits, key=lambda x: sum(int(i) for i in x if str(i).isdigit()))
    # else:
    #  digits = ['0','25']

print(digits)

 