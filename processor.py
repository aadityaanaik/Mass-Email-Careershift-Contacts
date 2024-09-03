import csv
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from config import CONTACT_LINKS_FILE, USERNAME, PASSWORD

def login_to_careershift(driver):
    driver.get("https://www.careershift.com/App/Contacts/Search?searchId=51954522&savedSearchId=1807249")

    email_field = driver.find_element(By.ID, "UserEmail")
    email_field.send_keys(USERNAME)

    password_field = driver.find_element(By.ID, "Password")
    password_field.send_keys(PASSWORD)

    password_field.send_keys(Keys.RETURN)
    time.sleep(2)
    print("Login successful!")

def fetch_contact_links(driver):
    links = driver.find_elements(By.XPATH, "//a[contains(@href, '/App/Contacts/SearchDetails?personId=')]")

    with open(CONTACT_LINKS_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        for link in links:
            person_name = link.text.strip()
            href = link.get_attribute("href")
            writer.writerow([person_name, href])

    print(f"{len(links)} links have been written to {CONTACT_LINKS_FILE}")