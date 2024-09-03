import time
from processor import login_to_careershift, get_info_from_links
from config import driver
from send_email import send_emails


def main():
    try:
        # Login to CareerShift
        # login_to_careershift(driver)

        # Fetch contact links
        # get_contact_links(driver)

        # Extract info from links and save to CSV
        get_info_from_links(driver)

        # Send emails to contacts
        send_emails()

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
