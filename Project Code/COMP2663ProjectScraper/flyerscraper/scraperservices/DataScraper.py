import os
import time
import undetected_chromedriver as uc
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
import json


def swap_to_iframe(driver, iframe_class="flippiframe.mainframe"):
    driver.switch_to.default_content()
    # Switch to the iframe
    iframe = driver.find_element(By.CLASS_NAME, iframe_class)
    # then find frame and swap
    driver.switch_to.frame(iframe)

def create_files(store_link):
    if not os.path.exists('data'):
        os.makedirs('data')
    
    driver = uc.Chrome(headless=True, use_subprocess=False)
    driver.get(store_link)

    config_independent = {
        'url': "https://www.yourindependentgrocer.ca/print-flyer",
        'postal_code': "V5H 4M1",
        'error_file': "data/error_superstore.html",
        'cookies_file': "data/superstore_cookies.json",
        'html_file': "data/superstore.html",
        'data_file': "data/superstore.json",
        'item_text': 'Select for details',
        'rollbar_regex': r'Rollback, (\d+)',
        'save_regex': r'Save \$([\d*?]+), \$([\d.]+)',
        'max_items': 50,
        'type': 'superstore',
    }

    print("Creating Files")
    try:
        main_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.TAG_NAME, "main")))
    except Exception as e:
        # save page source
        error_file = config_independent.get("error_file", "error_superstore.html")
        with open(error_file, "w", errors="ignore", encoding="utf-8") as f:
            f.write(driver.page_source)
        time.sleep(3)
    time.sleep(5)
    # Switch to the iframe
    swap_to_iframe(driver)
    # save content as data/superstore.html
    cookies = driver.get_cookies()
    # save cookies are cookies.json
    cookies_file = config_independent.get("cookies_file", "data/cookies.json")
    with open(cookies_file, "w") as f:
        json.dump(cookies, f)
    
    # get source html for driver
    html = driver.page_source

    html_file = config_independent.get("html_file", "data/superstore.html")
    # save to data/html
    with open(html_file, "w", errors="ignore", encoding="utf-8") as f:
        f.write(html)

    # The code above uses a flipp flyer scraper and runs it
    # The scraper mechanism doesnt work but it does save the correct html information to a file
    # This saved html file can be scraped manually

def scrape_independent():
    with open("/Users/Jon/Documents/SCHOOL WORK/COMP 2663/COMP2663Group19Project/ProjectCode/data/superstore.html", "r") as html_file: # Change the file path as necessary
        soup = BeautifulSoup(html_file, "html.parser")

    aria_labels = soup.find_all("sfml-flyer-image-a", attrs={"aria-label":True})
    deals = [deal['aria-label'] for deal in aria_labels]

    for x in range(len(deals)): # Breaking each deal in it's own list
        deals[x] = deals[x].split(", ")

    for x in range(len(deals)): # Converting data to dictionaries
        dict = {
            "Name" : deals[x][0], 
            "Info" : deals[x][1:-1], 
            "Price" : deals[x][-1], 
        }
        deals[x] = dict
    
    return deals

if __name__ == "__main__":
    create_files("https://www.yourindependentgrocer.ca/print-flyer")
    print(scrape_independent())
