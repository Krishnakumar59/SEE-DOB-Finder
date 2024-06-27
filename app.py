from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.common import TimeoutException
import requests
from datetime import datetime, timedelta
from time import sleep

# Your Symbol Number
original_symbol = "02005175" # Alphabet not needed here just symbol number
# Change line 28 and 29 accordingly insert your date range

# Your target URL and XPaths
weburl = 'https://see.ntc.net.np/results/grade'
symbol_xpath = '//*[@id="webform"]/div[1]/div[1]/b/input'
dob_xpath = '//*[@id="webform"]/div[1]/div[2]/b/b/input'  # XPath for the date of birth input field
submit_xpath = '//*[@id="webform"]/div[1]/div[3]/b/b/input'  # XPath for the submit button
validate_xpath = '//*[@id="webform"]/b/b/table/tbody/tr/td/table/tbody/tr[1]/td/div[1]/h2'
validate_data = "Secondary Education Examination"
x = ""
y = "DOB Found"


# Function to iterate through dates
def iterate_dates():
    start_date = datetime(2060, 5, 1) # search range from 2060
    end_date = datetime(2065, 12, 31) # search range to 2065
    current_date = start_date
    while current_date <= end_date:
        yield current_date.strftime('%Y-%m-%d')
        current_date += timedelta(days=1)


def is_element_present(xpath):
    try:
        # Use WebDriverWait to wait for the element to be present
        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return True
    except:
        return False


driver = webdriver.Chrome()
# Start the WebDriver and open the target URL
driver.get(weburl)
sleep(3)

# Find the symbol number field and enter the symbol number
symbol_field = driver.find_element(By.XPATH, symbol_xpath)
symbol_field.send_keys(original_symbol)
# symbol_field.send_keys(test_symbol)

for date in iterate_dates():
    try:
        # Find the date of birth field
        dob_field = driver.find_element(By.XPATH, dob_xpath)

        # Clear the date of birth field
        dob_field.clear()

        # Send the new date
        dob_field.send_keys(date)
        # dob_field.send_keys(test_dob)

        # Find and click the submit button
        submit_button = driver.find_element(By.XPATH, submit_xpath)
        submit_button.click()

        # Check if we get the expected validation data or not
        try:
            ff = is_element_present(validate_xpath)
            if ff == True:
                print(date)
                # bot_sendMessage(date)
                break
        except TimeoutException:
            print(f"Validation data not found for DOB: {date}")
        except NoSuchElementException:
            print("Element not found.")

    except NoSuchElementException as e:
        print(f"Error: {e}")
        continue

sleep(3)
driver.quit()
