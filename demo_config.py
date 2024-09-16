from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Path to the ChromeDriver executable (Make sure to update this based on your system)
# You can download ChromeDriver from: https://sites.google.com/a/chromium.org/chromedriver/downloads
CHROME_DRIVER_PATH = '/path/to/your/chromedriver'  # Update this path accordingly

# Data file paths
# CSV file containing contact information
CONTACT_INFO_FILE = 'data/contact_info.csv'
# CSV file to store collected contact links
CONTACT_LINKS_FILE = 'data/contact_links.csv'
# CSV file to store processed contact links (after sending emails)
PROCESSED_CONTACT_LINKS_FILE = 'data/processed_contacts_links.csv'
# Path to your resume (replace with your file path)
RESUME = 'documents/YourResume.pdf'  # Update this to point to your resume

# Login credentials (DO NOT share your credentials publicly)
# Update these with your own credentials for login
USERNAME = "your_email@example.com"  # Update with your careershift login id
PASSWORD = "your_password_here"  # Update with your password (keep this secure)

# Email configuration (used for sending emails)
EMAIL_ADDRESS = "your_email@example.com"  # Your email address
# Note: For Gmail, you need to generate an app password and use it here (
# https://support.google.com/accounts/answer/185833)
EMAIL_PASSWORD = "your_app_password_here"  # App password for your email (NOT your usual password)

# Search URL: Update this URL with the page you want to scrape from CareerShift or any other source
SEARCH_URL = "https://www.careershift.com/App/Contacts/Search?searchId=your_search_id_here"  # Update the search URL

# Initialize WebDriver
# Ensure the ChromeDriver is properly installed and configured
service = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service)

# SMTP configuration for sending emails
SMTP_SERVER = 'smtp.gmail.com'  # Gmail SMTP server
SMTP_PORT = 587  # SMTP port for Gmail

# Email template customization
# Your name and contact information
MY_NAME = "Your Name"  # Update with your name
MY_LINKEDIN_URL = "https://www.linkedin.com/in/yourprofile"  # Update with your LinkedIn profile
MY_GITHUB_URL = "https://github.com/yourgithub"  # Update with your GitHub profile
YEARS_OF_EXPERIENCE = "" #Update with the number of years of industry experience
DESIRED_ROLE = "" # Update with your desired role (Eg. Software Engineer/ Data Engineer/ Data Analyst/ Product
# Manager etc.) according to your preference

# The main message for the email (can be customized as needed)
MASS_EMAIL_MESSAGE = """
"""  # Add your personalized message
