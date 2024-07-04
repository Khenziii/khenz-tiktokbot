from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
import os


profile_path = os.path.abspath("geckodriver_stuff/profile/")
options = Options()
options.add_argument("-profile")
options.add_argument(profile_path)

service = Service(executable_path="./geckodriver_stuff/geckodriver", log_path="./geckodriver_stuff/geckodriver.log")
driver = webdriver.Firefox(service=service, options=options)
    
driver.get("https://www.tiktok.com/login/")

wait = input("if you have logged in already type ':)' and click enter to proceed: ")

driver.quit()
