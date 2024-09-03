
# Automated Email Sending and Contact Info Scraping

## Overview

This project automates the process of scraping contact information from CareerShift and sending customized emails to the contacts. It includes the following features:

- **Scraping Contact Information**: Extracts names, emails, and company names from CareerShift and stores them in CSV files.
- **Processing CSV Data**: Cleans and processes the scraped data, removing unwanted rows and formatting the content.
- **Automated Email Sending**: Sends customized emails with your resume attached to the contacts in the processed CSV files.

## Project Structure

```plaintext
├── config.py                   # Contains configuration settings for the project, including file paths and email credentials.
├── processor.py          # Handles all processing operations, such as logging in and scraping contact info from CareerShift.
├── send_email.py          # Sends customized emails to the contacts with the specified resume attached.
├── main.py                     # The main entry point of the project. Orchestrates the entire workflow.
├── email.html         # The HTML template used for sending well-formatted emails.
├── README.md                   # Project documentation.
└── data/
    ├── contact_info.csv        # Stores the final list of contacts, including names, emails, companies and email status
    ├── contact_links.csv       # Stores raw contact links scraped from CareerShift.
    └── processed_contacts_links.csv  # Stores processed contact links, ready for further operations.
```

## Installation

### Prerequisites

- Python 3.x
- pip (Python package manager)
- Google Chrome browser
- ChromeDriver

### Python Packages

Install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

## Usage

1. **Configuration**: Set up your configuration in the `config.py` and `email_config.py` files.
2. **Run Application**: Run main.py

**Scrape Contact Information**: `processor.py` to log in to CareerShift and scrape contact information.
**Process CSV Data**: `csv_processor.py` to clean and process the scraped contact information.
**Send Emails**: `send_email.py` to send customized emails to the contacts.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the need to automate repetitive tasks and streamline the job application process.
