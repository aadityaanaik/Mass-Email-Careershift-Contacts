import csv
import os
import time
from tempfile import NamedTemporaryFile
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from config import CONTACT_LINKS_FILE, USERNAME, PASSWORD, PROCESSED_CONTACT_LINKS_FILE, CONTACT_INFO_FILE


def login_to_careershift(driver):
    driver.get("https://www.careershift.com/App/Contacts/Search?searchId=51954522&savedSearchId=1807249")

    email_field = driver.find_element(By.ID, "UserEmail")
    email_field.send_keys(USERNAME)

    password_field = driver.find_element(By.ID, "Password")
    password_field.send_keys(PASSWORD)

    password_field.send_keys(Keys.RETURN)
    time.sleep(2)
    print("Login successful!")


def multiple_pages(driver):
    while True:
        try:
            next_button = driver.find_element(By.CLASS_NAME, "btnNext.traverse")
            next_button.click()
            time.sleep(3)
        except:
            print("Last page reached. No more pages to process.")
            break


def get_contact_links(driver):
    links = driver.find_elements(By.XPATH, "//a[contains(@href, '/App/Contacts/SearchDetails?personId=')]")

    with open(CONTACT_LINKS_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        for link in links:
            person_name = link.text.strip()
            href = link.get_attribute("href")
            writer.writerow([person_name, href])

    print(f"{len(links)} links have been written to {CONTACT_LINKS_FILE}")


def process_contact_links(input_file, output_file):
    with open(input_file, mode='r', newline='') as infile, open(output_file, mode='w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        writer.writerow(["Name", "Link"])
        for row in reader:
            person_name = row[0]
            if person_name == "CONTACT DETAILS" or person_name == "Person Name":
                continue
            first_name = person_name.split()[0]
            writer.writerow([first_name, row[1]])


def get_info_from_links(driver):
    links = []
    names = []
    temp_file = NamedTemporaryFile(mode='w', delete=False, newline='')

    with open(PROCESSED_CONTACT_LINKS_FILE, mode='r', newline='') as infile, temp_file:
        reader = csv.reader(infile)
        writer = csv.writer(temp_file)

        header = next(reader)
        writer.writerow(header)

        for i, row in enumerate(reader):
            if i < 49:
                name = row[0]
                link = row[1]
                names.append(name)
                links.append(link)
            else:
                writer.writerow(row)

    extracted_data = get_info_from_web(driver, names, links)

    with open(CONTACT_INFO_FILE, mode='a', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["Name", "Company", "Email", "isSent"])
        for row in extracted_data:
            writer.writerow([row[0], row[1], row[2], 'N'])

    os.replace(temp_file.name, PROCESSED_CONTACT_LINKS_FILE)


def get_info_from_web(driver, names, links):
    extracted_data = []

    for name, link in zip(names, links):
        driver.get(link)
        time.sleep(3)

        try:
            email_element = driver.find_element(By.XPATH, "//a[contains(@href, 'mailto:')]")
            email = email_element.get_attribute("href").replace("mailto:", "")
        except:
            email = "No email found"

        try:
            company_element = driver.find_element(By.XPATH, "//h4")
            company = company_element.text.strip()
        except:
            company = "No company found"

        extracted_data.append([name, company, email])

    return extracted_data
