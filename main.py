from selenium import webdriver
import os
co=webdriver.ChromeOptions()
co.binary_location=os.environ.get("GOOGLE_CHROME_BIN")
co.add_argument("--headless")
co.add_argument("--diable-dev-shm-usage")
co.add_argument("--no-sandbox")
d=webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),chrome_options=co)
d.get("https://lms.veltech.edu.in/login/index.php")
print(d.page_source)
