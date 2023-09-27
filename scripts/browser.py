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
    try:
        iframe_element = driver.find_element(By.XPATH, "//iframe[@src='https://www.tiktok.com/creator#/upload?scene=creator_center']")
    except Exception as e:
        print(f"[---] Oops, something went wrong while trying to get the iframe element. This could be caused by tiktok updating their's HTML structure. To fix this error, you most likely have to go to https://www.tiktok.com/creator-center/upload?lang=en select the appropiate element identifier, and update it :) (file browser.py, line 44). If you'll encounter new problems, don't be shy to create a github issue. Exception: {e}")
        return
    driver.switch_to.frame(iframe_element)

    # select the select file input
    try:
        select_input = driver.find_element(By.CSS_SELECTOR, 'input.jsx-2207703846')
    except Exception as e:
        print(f"[---] Oops, something went wrong while trying to get the path input element. This could be caused by tiktok updating their's HTML structure. To fix this error, you most likely have to go to https://www.tiktok.com/creator-center/upload?lang=en select the appropiate element identifier, and update it :) (file browser.py, line 51). If you'll encounter new problems, don't be shy to create a github issue. Exception: {e}")
        return

    # write the path to the select input
    select_input.send_keys(path)

    print("[+] entered the path to the video")

    # select the caption input box
    try:
        caption_input = driver.find_element(By.CSS_SELECTOR, '.notranslate')
    except Exception as e:
        print(f"[---] Oops, something went wrong while trying to get the caption input element. This could be caused by tiktok updating their's HTML structure. To fix this error, you most likely have to go to https://www.tiktok.com/creator-center/upload?lang=en select the appropiate element identifier, and update it :) (file browser.py, line 62). If you'll encounter new problems, don't be shy to create a github issue. Exception: {e}")
        return

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

    # select the post button
    try:
        post_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.css-y1m958')))
    except Exception as e:
        print(f"[---] Oops, something went wrong while trying to get the post button element. This could be caused by tiktok updating their's HTML structure. To fix this error, you most likely have to go to https://www.tiktok.com/creator-center/upload?lang=en select the appropiate element identifier, and update it :) (file browser.py, line 86). If you'll encounter new problems, don't be shy to create a github issue. Exception: {e}")
        return

    # click the post button
    post_button.click()
    print("[+] clicked the post button!")

    time.sleep(20)
    driver.quit()