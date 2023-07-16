import os
import time
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service


os.environ['TMPDIR'] = os.path.expanduser("~/tmp/khenz-tiktokbot")

options = Options()
options.add_argument("--headless")
options.add_argument("-profile")
profile_path = os.path.abspath("geckodriver_stuff/profile/")
options.add_argument(profile_path)

def get_image(post_url: str, post_id: str, name: str):
    service = Service(executable_path="./geckodriver_stuff/geckodriver", log_path="./geckodriver_stuff/geckodriver.log")
    driver = webdriver.Firefox(service=service, options=options)

    driver.get(post_url)

    time.sleep(10)
    post_content_div = driver.find_element(By.XPATH, f'//*[@id="t3_{post_id}"]')
    post_content_div.screenshot(name)

    driver.quit()

def post(path: str, caption: str, tags: list = ["redditstories", "fyp", "foryoupage"]):
    service = Service(executable_path="./geckodriver_stuff/geckodriver", log_path="./geckodriver_stuff/geckodriver.log")
    driver = webdriver.Firefox(service=service, options=options)

    driver.set_window_size(1920, 1080)
    driver.get("https://www.tiktok.com/upload?lang=en")
    print("[+] got to the titkok.com")
    time.sleep(30)

    # select the iframe element
    iframe_element = driver.find_element(By.XPATH, "//iframe[@src='https://www.tiktok.com/creator#/upload?lang=en']")
    driver.switch_to.frame(iframe_element)

    # select the select file input
    select_input = driver.find_element(By.CSS_SELECTOR, 'input.jsx-1625145290')
    # write the path to the select input
    select_input.send_keys(path)

    print("[+] entered the path to the video")

    # select the caption input box
    caption_input = driver.find_element(By.CSS_SELECTOR, '.notranslate')
    # write the caption
    caption_input.send_keys(caption)

    print("[+] entered the caption of the video")

    #write the tags
    for tag in tags:
        ActionChains(driver).send_keys('#').perform()
        caption_input.send_keys(tag)
        time.sleep(3)  # Add a delay to allow the tags to load
        ActionChains(driver).send_keys(Keys.SPACE).perform()
    
    print("[+] entered the tags of the video")

    print("[i] waiting for tiktok to fetch the video...")
    # Wait until the button is clickable
    wait = WebDriverWait(driver, 300)
    post_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.css-y1m958')))

    # click the post button
    post_button.click()
    print("[+] clicked the post button!")

    time.sleep(20)
    driver.quit()