
# Automated Contact Scraper and Email Sender

This project is an automation tool designed to scrape contact information from the CareerShift platform using Selenium and send personalized emails to those contacts using Gmail's SMTP server.

## Features
- Logs into CareerShift using Selenium WebDriver.
- Scrapes multiple pages of contacts and stores them in a CSV file.
- Sends personalized emails to contacts with an HTML template that can be customized.
- Tracks which contacts have already been emailed and skips sending duplicate emails.

## Prerequisites
- Python 3.x
- Chrome browser and ChromeDriver
- Gmail account (for sending emails)

## Setup Instructions

### 1. Clone the repository:
```bash
git clone https://github.com/aadityaanaik/Mass-Email-Careershift-Contacts.git
cd Mass-Email-Careershift-Contacts
```

### 2. Set up a Virtual Environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
```

### 3. Install Required Libraries:
```bash
pip install -r requirements.txt
```

### 4. Configure `config.py`:
Modify the `demo_config.py` file with your own credentials and file paths.

- **ChromeDriver Path**: Update the `CHROME_DRIVER_PATH` to point to the location of ChromeDriver on your system.
- **Login Credentials**: Replace `USERNAME` and `PASSWORD` with your CareerShift login credentials.
- **Email Credentials**: Replace `EMAIL_ADDRESS` and `EMAIL_PASSWORD` with your Gmail credentials. For Gmail, generate an app password (see [here](https://support.google.com/accounts/answer/185833) for instructions).
- **Preferences**: Add your desired role and years of work experience.
- **Other Configurations**: Set paths to your contact information file, processed links file, resume, and any other file dependencies.

Rename the `demo_config.py` file to `config.py`

### 5. Run the Program:
```bash
python main.py
```

This will log into CareerShift, scrape contact information, and send emails to the collected contacts.

### 6. Deactivate the Virtual Environment (if using):
```bash
deactivate
```

## Project Structure

```
├── data/                           # Directory for CSV files
│   ├── contact_info.csv            # CSV with collected contact information
│   ├── contact_links.csv           # CSV to store raw contact links
│   ├── processed_contact_links.csv # CSV for processed contact links
├── documents/
│   ├── YourResume.pdf              # Your resume file (used in the email)
├── main.py                         # Entry point of the program
├── processor.py                    # Core logic for scraping and email sending
├── email.html                      # Email structure
├── config.py                       # Configuration file for paths, credentials, and email settings
└── README.md                       # Project documentation
```

## Key Components

- **`main.py`**: The entry point of the project. Calls functions to scrape contact links and send emails.
- **`processor.py`**: Contains the main logic for scraping CareerShift using Selenium, processing the contacts, and sending emails via SMTP.
- **`config.py`**: Stores configuration values like file paths, login credentials, and email server settings.

## Dependencies
The following Python libraries are required:
- `selenium`: Used for browser automation to scrape contacts from CareerShift.
- `smtplib`: Built-in Python library for sending emails via SMTP.
- `email`: Built-in Python library for constructing email messages.
- `csv`: Built-in Python library for reading and writing CSV files.
- `jinja2` (optional): If you want to use advanced templating for emails.

## Configurations
- **CONTACT_INFO_FILE**: The path to the CSV file containing contact information.
- **CONTACT_LINKS_FILE**: The path to the CSV file where scraped contact links are stored.
- **PROCESSED_CONTACT_LINKS_FILE**: The path to the CSV file that stores processed contact links.
- **RESUME**: The path to the resume file that will be attached to emails.
- **SMTP_SERVER & SMTP_PORT**: Configured for Gmail by default.

## SMTP Configuration for Gmail
You will need to use an app password to authenticate with Gmail. Follow [these instructions](https://support.google.com/accounts/answer/185833) to generate an app password, and use that in the `EMAIL_PASSWORD` field of `config.py`.

## License
This project is licensed under the MIT License.
