import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from config import SMTP_SERVER, SMTP_PORT, USERNAME, PASSWORD
from config import CONTACT_INFO_FILE


def send_custom_emails():
    resume_file = 'documents/AdityaNaikResume.pdf'  # Update this with the actual path to your resume

    with open(CONTACT_INFO_FILE, mode='r', newline='') as infile:
        reader = csv.DictReader(infile)
        rows = list(reader)  # Load all rows into memory

    # Set up the server
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(USERNAME, PASSWORD)

    for row in rows:
        if row.get('isSent') == '':  # Only send to contacts who haven't been emailed yet
            name = row['Name']
            company = row['Company']
            email = row['Email']

            if email == "No email found":  # Skip if no email is available
                continue

            # Create a multipart message
            msg = MIMEMultipart()
            msg['From'] = USERNAME
            msg['To'] = email
            msg['Subject'] = f"Opportunity at {company}"

            # Customize your message here
            message = f"""Hello {name},

I am Aditya Naik, and I recently graduated from Texas A&M University with a Master’s degree in Management Information Systems. I am actively looking for full-time employment opportunities in the field of data engineering. I have attached my resume for your reference.

About Me: (More on adityanaik.info)

I am an AWS certified engineer, having previously worked in the banking industry with HSBC as a data engineer for 3+ years. In the US, I worked as a data engineer at Texas A&M University for about 2 years. I have handled, managed, and maintained petabytes of data in both roles with a combined experience of 5 years.

My experience portrays extensive knowledge of SQL, Python, Spark, Kafka, Airflow, GCP, and AWS. I have worked on distributed systems frameworks like HDFS, developed ETL pipelines using AWS Glue, processed large data sets using EMR, and optimized SQL performance tuning to improve query performance. I thrive in fast-paced environments and am adept at communicating complex technical concepts to stakeholders at all levels.

Regards,
Aditya Naik (he/him)
LinkedIn: https://www.linkedin.com/in/aadityaanaik
GitHub: https://github.com/naikvaditya"""

            # Attach the message to the email
            msg.attach(MIMEText(message, 'plain'))

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
