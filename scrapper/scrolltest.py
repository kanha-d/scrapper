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

# # Open LinkedIn
# driver.get("https://www.linkedin.com")

# # Locate the email and password fields and enter your credentials
# email_elem = driver.find_element(By.ID,"session_key")
# password_elem = driver.find_element(By.ID,"session_password")

# email_elem.send_keys(email)
# password_elem.send_keys(password)

# # Submit the login form
# password_elem.send_keys(Keys.RETURN)

# # You may need to handle additional verification steps depending on your LinkedIn account's security settings.

# # Add some waiting time to see the result
# sleep(10)
# f = open("linkedin.txt","a")

# # collect all urls
# jobs_url = []

# jobsCount =0
# try:
#     jobsCountText = driver.find_element(By.CLASS_NAME, 'jobs-search-results-list__subtitle').text
#     jobsCount = jobsCountText.split()[0][1:].replace(",", "")
#     print(jobsCount)
#     sleep(2)
# except:
#     print('Excepiton')

# URL of the LinkedIn job search page
base_url = "https://www.linkedin.com/jobs/search/?currentJobId=3744133218&geoId=102713980&keywords=data&location=India&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true"

# List to store job links
job_links = []
# Loop through multiple pages (change the range as needed)
driver.get(base_url)
time.sleep(3)  # Wait for the page to load
jobsListScroll = driver.find_element(By.CSS_SELECTOR, ".jobs-search__results-list")  # Replace with the actual element locator method you are using (e.g., by_id, by_xpath, by_css_selector, etc.)
for _ in range(3):
    print('dddd')
    driver.execute_script('arguments[0].scrollIntoView({ behavior: "smooth",block: "end",inline:"end"})', jobsListScroll)
    time.sleep(3)



# Close the browser
# driver.quit()
