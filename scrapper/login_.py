from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import shutup; shutup.please()
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from password import pass_import,email_import
# Set the path to your webdriver. Make sure you have the WebDriver installed and configured.
# Download the appropriate WebDriver from https://selenium.dev/documentation/en/webdriver/driver_requirements/
import time 
from time import sleep
import requests
import bs4


option = Options()
#option.add_argument("--headless")
option.add_argument("--disable-infobars")
option.add_argument("start-maximized")
option.add_argument("--disable-extensions")
# Pass the argument 1 to allow and 2 to block
option.add_experimental_option(
    "prefs", {"profile.default_content_setting_values.notifications": 1}
)

# # LinkedIn login credentials
email = email_import
password = pass_import

# Initialize the WebDriver
driver = webdriver.Chrome(ChromeDriverManager().install())
action = ActionChains(driver)
driver.maximize_window()

# Open LinkedIn
driver.get("https://www.linkedin.com")

# Locate the email and password fields and enter your credentials
email_elem = driver.find_element(By.ID,"session_key")
password_elem = driver.find_element(By.ID,"session_password")

email_elem.send_keys(email)
password_elem.send_keys(password)

# Submit the login form
password_elem.send_keys(Keys.RETURN)

# You may need to handle additional verification steps depending on your LinkedIn account's security settings.

# Add some waiting time to see the result
sleep(10)
f = open("linkedin.txt","a")

# collect all urls
jobs_url = []

jobsCount =0
# try:
#     jobsCountText = driver.find_element(By.CLASS_NAME, 'jobs-search-results-list__subtitle').text
#     jobsCount = jobsCountText.split()[0][1:].replace(",", "")
#     print(jobsCount)
#     sleep(2)
# except:
#     print('Excepiton')

# URL of the LinkedIn job search page
base_url = "https://www.linkedin.com/jobs/search/?currentJobId=3738352844&f_F=cnsl%2Cstra&f_I=11&keywords=consulting&origin=JOB_SEARCH_PAGE_JOB_FILTER&sortBy=R&start="

# List to store job links
job_links = [[]]

# Loop through multiple pages (change the range as needed)
for page in range(1, 7):  # Scraping the first 3 pages
    url = f"{base_url}{(page-1)*25}"  # Adjust based on the number of jobs displayed per page
    # Navigate to the web page
    driver.get(url)
    time.sleep(3)  # Wait for the page to load
    jobsListScroll = driver.find_element(By.CSS_SELECTOR, ".scaffold-layout__list-container")  # Replace with the actual element locator method you are using (e.g., by_id, by_xpath, by_css_selector, etc.)

    # actions = ActionChains(driver)
    # actions.w3c_actions.pointer_action._duration = 7000
    # actions.move_to_element(jobsListScroll).perform()
    # Scroll down to load more jobs (adjust the number of scrolls as needed)
    for _ in range(4):
        print('scrolling.....')
        driver.execute_script('arguments[0].scrollIntoView({ behavior: "smooth",block: "end",inline:"end"})', jobsListScroll)
        # driver.execute_script("scroll(0, document.body.scrollHeight)",jobsListScroll)
        time.sleep(5)  # Wait for the page to load
    
    # Find job links
    container = driver.find_element(By.CSS_SELECTOR, ".scaffold-layout__list-container")
    li_elements = container.find_elements(By.TAG_NAME, "li")

    print(len(li_elements))

    for elem in li_elements:
        try:
            anchor = elem.find_element(By.CLASS_NAME, "job-card-list__title")
            # anchor = WebDriverWait(driver, 20).until(EC.visibility_of_element_located(elem.find_element(By.CLASS_NAME, "job-card-list__title")))
            job_link = [anchor.get_attribute("href"),anchor.text]
            job_links.append(job_link)
        #     print('got Links')
        except Exception as ex:
        #     print(ex)
            print('no link')
    # Print the job links on this page
    # for link in job_links:
    #     print(link)


# # for jobIndex in range(1, int(jobsCount)+1):

# #     if (jobIndex % 25 == 0):
# #         driver.execute_script("scroll(0, document.body.scrollHeight);")
# #         show_button = driver.find_element(By.CLASS_NAME, 'infinite-scroller__show-more-button')
# #         driver.execute_script("arguments[0].click();", show_button)
# #         sleep(3)

# #     elements = driver.find_element(By.CLASS_NAME, 'jobs-search__results-list')

# #     try:
# #         job = elements.find_element(By.CSS_SELECTOR, 'li:nth-of-type('+str(jobIndex)+')')
# #         link = job.find_element(By.TAG_NAME, 'a').get_attribute('href')
# #         url_key = "in.linkedin"
        
# #         if url_key in link:
# #             link = link.replace(url_key,"linkedin")
        
        
# #         jobs_url.append([16,link])
# #         if jobIndex > 100: 
# #             break
            
# #     except Exception as ex:
# #         print('Exception in li')
# #         continue
    
    
# Jobs count in array
print('jobs count final')
print(len(job_links))

for link in job_links:
    print(link)
    try : 
     f.write("Job : "+str(link[0])+"\n")
     f.write("URL: "+link[1]+"\n")
     f.write("\n\n")
    except :
        print('empty')
    
    #     print(link)



# #     # collect all data

# jobs_arr = []
# job_arr = []    


# i = 0
# for url in jobs_url :
#         if i == 20:
#             break
#         i+=1
#         if url != 'list1' :   
#             try:
#                 res = requests.get(url[1])
#                 bs = bs4.BeautifulSoup(res.text,"html.parser")
#                 try:
#                     cat = url[0]
#                     try : 
#                      title = bs.find('h1',{'class' :'top-card-layout__title'}).text
#                     except:
#                      title = bs.find('h1',{'class' :'jobs-unified-top-card__job-title'}).text
                    
#                     custom_exp = [0,15]
#                     try : 
#                         first_span_tag = bs.find('ul', class_='description__job-criteria-list').find('span')
                        
#                         if first_span_tag:
#                             span_exp = first_span_tag.get_text(strip=True)
#                             if span_exp.startswith("Internship"):
#                                 custom_exp = [0,1]
#                             elif span_exp.startswith(("Executive", "Associate")):
#                                 custom_exp = [2,5]
#                             elif span_exp.startswith("Entry level") :
#                                 custom_exp = [0,2]  
#                             elif span_exp.startswith("Mid-Senior level") :
#                                 custom_exp = [5,10]       
#                             elif span_exp.startswith("Director"):
#                                 custom_exp = [10,15]   
#                             else :
#                                 custom_exp = [0,15]  
#                         else:
#                             print("Span tag not found.")    
#                     except:
#                         print("Span tag not found.")   
                    
#                     title = title.strip().replace("'", "")
#                     temp_title = title.strip().replace("'", "").lower()
#                     print(title)

#                     location = location.strip().replace("'", "")

#                     # f.write("External URL: "+job_url+"\n")
#                     f.write("Title: "+title+"\n")
#                     # f.write("linkedin URL: "+url[1]+"\n")
#                     f.write("location: " + location+"\n")
#                     # f.write("skills: " + skills+"\n")
#                     # f.write("Exp : " + str(job_exp)+"\n")
                
#                     f.write("\n\n")

#                 except Exception as ex:
#                     print('\n')
#                     continue
#             except Exception as ex:
#                 continue
#             # temp_job_arr = [title,desc,job_url,company,location,skills,job_exp,functional_area["consulting"]]
#             # jobs_arr.append(temp_job_arr)
 
  




# Close the browser
driver.quit()
