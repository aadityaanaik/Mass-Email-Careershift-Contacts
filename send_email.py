import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from config import SMTP_SERVER, SMTP_PORT, EMAIL_ADDRESS, EMAIL_PASSWORD, RESUME
from config import CONTACT_INFO_FILE


def send_emails():
    resume_file = RESUME  # Update this with the actual path to your resume

    # Read the HTML template
    with open('email.html', 'r') as file:
        html_template = file.read()

    with open(CONTACT_INFO_FILE, mode='r', newline='') as infile:
        reader = csv.DictReader(infile)
        rows = list(reader)  # Load all rows into memory

    # Set up the server
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    for row in rows:
        if row.get('isSent') == 'N':  # Only send to contacts who haven't been emailed yet
            name = row['Name']
            company = row['Company']
            email = row['Email']

            if email == "No email found":  # Skip if no email is available
                continue

            # Create a multipart message
            msg = MIMEMultipart()
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = email
            msg['Subject'] = f"Data Engineer with 4+ YoE looking to contribute your team's success at {company}"

            # Customize the HTML message
            html_message = html_template.replace('{{Name}}', name)

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
            print(f"Email sent to {name} at {email}")

            # Mark as sent
            row['isSent'] = 'Y'

    # Close the server connection
    server.quit()

    # Update the CSV file with the sent status
    with open(CONTACT_INFO_FILE, mode='w', newline='') as outfile:
        fieldnames = ['Name', 'Company', 'Email', 'isSent']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
