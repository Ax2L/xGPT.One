# ./helper/selenium/selenium_helper.py

import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

# Function to set up the Chrome WebDriver
def get_chrome_driver(chromedriver_path):
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
    return driver


# Function to list out all the files matching the criteria
def find_matching_files(directory, indicators):
    matching_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(indicator.lower() in file.lower() for indicator in indicators):
                matching_files.append(os.path.join(root, file))
    return matching_files


# Function to send content with Selenium
def send_content(driver, file_path):
    with open(file_path, "r") as file:
        content = file.read()

    # Here, you would need to implement the actual logic for sending
    # messages using the chat interface and your specific web elements.
    # For instance, find message input box, paste content, and send the message.

    # Example (replace with actual ID or selectors for your case):
    message_box = driver.find_element(By.ID, "message_input")
    message_box.send_keys(content)
    message_box.send_keys(Keys.RETURN)


# Function to wait for a specific acknowledgment message
def wait_for_acknowledgment(driver, acknowledgment_word):
    acknowledged = False
    while not acknowledged:
        # Here, you need to define the logic to check for the acknowledgment word
        # in the chat interface. This will be highly dependent on the structure
        # of the chat interface that you are automating.
        # This is just a placeholder for illustrative purposes.

        # Example (replace with actual logic for your case):
        last_msg = driver.find_element(By.XPATH, "//div[@class='last_message']")
        if acknowledgment_word in last_msg.text:
            acknowledged = True
        else:
            time.sleep(1)
        # This function should be improved - it may check more efficiently,
        # e.g., using Selenium's wait and expected conditions.
