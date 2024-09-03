import csv
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from tempfile import NamedTemporaryFile

# Specify the path to the ChromeDriver
service = Service('/opt/homebrew/bin/chromedriver')  # Update this path to your chromedriver location

# Initialize WebDriver with the Service object
driver = webdriver.Chrome(service=service)

# List to hold all contact information
contacts = []

def process_send_emails():
    input_file = 'data/contact_info.csv'
    output_file = 'data/processed_contact_info.csv'

    with open(input_file, mode='r', newline='') as infile, open(output_file, mode='w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Write the new header row only once
        writer.writerow(["Name", "Link"])

        for row in reader:
            name = row[0]  # Assumes "Person Name" is the first column

            # Skip "CONTACT DETAILS" rows and the original header
            if name == "Name":
                continue

            writer.writerow([name, row[1], row[2]])

def process_contact_links():
    input_file = 'data/contact_links.csv'
    output_file = 'data/processed_contacts_links.csv'

    # Read the input CSV and filter out unwanted rows
    with open(input_file, mode='r', newline='') as infile, open(output_file, mode='w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Write the new header row only once
        writer.writerow(["Name", "Link"])

        for row in reader:
            person_name = row[0]  # Assumes "Person Name" is the first column

            # Skip "CONTACT DETAILS" rows and the original header
            if person_name == "CONTACT DETAILS" or person_name == "Person Name":
                continue

            # Keep only the first name (assuming names are separated by space)
            first_name = person_name.split()[0]

            # Write the new row with blank "Recipient" and "Company"
            writer.writerow([first_name, row[1]])


try:
    # Open the Careershift login page
    driver.get("https://www.careershift.com/App/Contacts/Search?searchId=51954522&savedSearchId=1807249")

    # Find the email field by its ID and enter the email
    email_field = driver.find_element(By.ID, "UserEmail")
    email_field.send_keys("aditya.naik@tamu.edu")

    # Find the password field by its ID and enter the password
    password_field = driver.find_element(By.ID, "Password")
    password_field.send_keys("KLRahul@199")

    # Submit the login form
    password_field.send_keys(Keys.RETURN)

    time.sleep(2)
    print("Login successful!")


    def fetch_contact_links():
        # Find all elements with hrefs that match the pattern
        links = driver.find_elements(By.XPATH, "//a[contains(@href, '/App/Contacts/SearchDetails?personId=')]")

        # Open or create a CSV file to write the links
        with open('data/contact_links.csv', mode='a', newline='') as file:
            writer = csv.writer(file)

            # Loop through each link and write to CSV
            for link in links:
                person_name = link.text.strip()  # Extract the name from the link text
                href = link.get_attribute("href")  # Extract the actual href link
                writer.writerow([person_name, href])  # Write the name and link to the CSV

        print(f"{len(links)} links have been written to contact_links.csv")


    def get_info_links_to_csv():

        input_file = 'data/processed_contacts_links.csv'
        output_file = 'data/contact_info.csv'

        # List to store the first 50 links
        links = []
        names = []
        temp_file = NamedTemporaryFile(mode='w', delete=False, newline='')

        # Read the CSV file and extract the first 50 links
        with open(input_file, mode='r', newline='') as infile, temp_file:
            reader = csv.reader(infile)
            writer = csv.writer(temp_file)

            # Read and write the header row
            header = next(reader)
            writer.writerow(header)

            # Process the first 50 rows and keep the rest in the temp file
            for i, row in enumerate(reader):
                if i < 5:
                    name = row[0]  # Assuming 'Name' is in the first column
                    link = row[1]  # Assuming 'Link' is in the second column
                    names.append(name)
                    links.append(link)
                else:
                    writer.writerow(row)

        extracted_data = []

        # Iterate through each contact link
        for name, link in zip(names, links):
            driver.get(link)  # Navigate to the link
            time.sleep(3)  # Wait for the page to load

            # Extract the email if present
            try:
                email_element = driver.find_element(By.XPATH, "//a[contains(@href, 'mailto:')]")
                email = email_element.get_attribute("href").replace("mailto:", "")
            except:
                email = "No email found"

            # Extract the company name from the <h4> tag
            try:
                company_element = driver.find_element(By.XPATH, "//h4")
                company = company_element.text.strip()
            except:
                company = "No company found"

            # Append the dictionary to the contacts list (this will form our JSON array)
            extracted_data.append([name, company, email])
            print(f"Collected contact: {[name, company, email]}")

        with open(output_file, mode='a', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(["Name", "Company", "Email"])
            writer.writerows(extracted_data)

        os.replace(temp_file.name, input_file)


    get_info_links_to_csv()

    # while True:
    #     # process_contacts_on_page()
    #     # fetch_contact_links()
    # 
    #     try:
    #         # Find the "Next" button and click it
    #         next_button = driver.find_element(By.CLASS_NAME, "btnNext.traverse")
    #         next_button.click()
    #         time.sleep(3)  # Wait for the next page to load
    #     except:
    #         # If the "Next" button is not found, we've reached the last page
    #         print("Last page reached. No more pages to process.")
    #         break

finally:
    driver.quit()
