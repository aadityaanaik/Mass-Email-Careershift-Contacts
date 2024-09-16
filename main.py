import time
from processor import get_info_from_links, send_emails
from demo_config import driver


def main():
    try:
        # Extract info from links and save to CSV
        get_info_from_links(driver)

    finally:
        driver.quit()

    # Send emails to the 49 contacts
    send_emails()


if __name__ == "__main__":
    main()
