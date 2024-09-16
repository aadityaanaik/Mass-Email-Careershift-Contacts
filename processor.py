import os
import time
from tempfile import NamedTemporaryFile
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import config
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def login_to_careershift(driver):
    driver.get(config.SEARCH_URL)

    email_field = driver.find_element(By.ID, "UserEmail")
    email_field.send_keys(config.USERNAME)

    password_field = driver.find_element(By.ID, "Password")
    password_field.send_keys(config.PASSWORD)

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


def get_all_contact_links(driver):
    # Check if the file is empty (except for the headers) or create the file if not exists
    if os.path.isfile(config.PROCESSED_CONTACT_LINKS_FILE):
        with open(config.PROCESSED_CONTACT_LINKS_FILE, mode='r', newline='') as file:
            reader = csv.reader(file)
            rows = list(reader)
            # If more than just the header row exists, skip the writing process
            if len(rows) > 1:
                print(f"{config.PROCESSED_CONTACT_LINKS_FILE} is not empty. Skipping the writing process.")
                return
    else:
        # Create the file if it does not exist
        with open(config.CONTACT_LINKS_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            # Add headers if the file was just created
            writer.writerow(["Person Name", "Link"])

    # Login to CareerShift
    login_to_careershift(driver)

    # Get the contact links
    links = driver.find_elements(By.XPATH, "//a[contains(@href, '/App/Contacts/SearchDetails?personId=')]")

    # Write the contact links to the file
    with open(config.CONTACT_LINKS_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        for link in links:
            person_name = link.text.strip()
            href = link.get_attribute("href")
            writer.writerow([person_name, href])

    print(f"{len(links)} links have been written to {config.CONTACT_LINKS_FILE}")

    # Now process the written contact links and write to output_file
    with open(config.CONTACT_LINKS_FILE, mode='r', newline='') as infile, open(config.PROCESSED_CONTACT_LINKS_FILE, mode='w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        writer.writerow(["Name", "Link"])
        for row in reader:
            person_name = row[0]
            if person_name == "CONTACT DETAILS" or person_name == "Person Name":
                continue
            first_name = person_name.split()[0]
            writer.writerow([first_name, row[1]])

    print(f"Processed contact links have been written to {config.PROCESSED_CONTACT_LINKS_FILE}")

    # Delete the CONTACT_LINKS_FILE after processing
    if os.path.isfile(config.CONTACT_LINKS_FILE):
        os.remove(config.CONTACT_LINKS_FILE)
        print(f"{config.CONTACT_LINKS_FILE} has been deleted after processing.")


def get_info_from_links(driver):

    get_all_contact_links(driver)

    links = []
    names = []
    temp_file = NamedTemporaryFile(mode='w', delete=False, newline='')

    with open(config.PROCESSED_CONTACT_LINKS_FILE, mode='r', newline='') as infile, temp_file:
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

    with open(config.CONTACT_INFO_FILE, mode='a', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["Name", "Company", "Email", "isSent"])
        for row in extracted_data:
            writer.writerow([row[0], row[1], row[2], 'N'])

    os.replace(temp_file.name, config.PROCESSED_CONTACT_LINKS_FILE)


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


def send_emails():
    resume_file = config.RESUME  # Update this with the actual path to your resume

    # Read the HTML template
    with open('email.html', 'r') as file:
        html_template = file.read()

    with open(config.CONTACT_INFO_FILE, mode='r', newline='') as infile:
        reader = csv.DictReader(infile)
        rows = list(reader)  # Load all rows into memory

    # Set up the server
    server = smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT)
    server.starttls()
    server.login(config.EMAIL_ADDRESS, config.EMAIL_PASSWORD)

    for row in rows:
        if row.get('isSent') == 'N':  # Only send to contacts who haven't been emailed yet
            recipient = row['Name']
            company = row['Company']
            email = row['Email']
            yoe = config.YEARS_OF_EXPERIENCE
            role = config.DESIRED_ROLE


            if email == "No email found":  # Skip if no email is available
                continue

            # Create a multipart message
            msg = MIMEMultipart()
            msg['From'] = config.EMAIL_ADDRESS
            msg['To'] = email
            msg['Subject'] = f"{role} with {yoe} YoE looking to contribute your team's success at {company}"

            # Customize the HTML message
            html_message = (html_template
                            .replace('{{Recipient}}', recipient)
                            .replace('{{My_Name}}', config.MY_NAME)
                            .replace('{{Mass_Email_Message}}', config.MASS_EMAIL_MESSAGE)
                            .replace('{{LinkedIn_URL}}', config.MY_LINKEDIN_URL)
                            .replace('{{Github_URL}}', config.MY_GITHUB_URL))

            # Attach the HTML message
            msg.attach(MIMEText(html_message, 'html'))

            # Attach the resume
            attachment = open(resume_file, 'rb')
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={resume_file.split("/")[-1]}')
            msg.attach(part)
            attachment.close()

            # Send the email
            server.send_message(msg)
            print(f"Email sent to {recipient} at {email}")

            # Mark as sent
            row['isSent'] = 'Y'

    # Close the server connection
    server.quit()

    # Update the CSV file with the email status
    with open(config.CONTACT_INFO_FILE, mode='w', newline='') as outfile:
        fieldnames = ['Name', 'Company', 'Email', 'isSent']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
