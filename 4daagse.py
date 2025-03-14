from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import beepy
from dotenv import dotenv_values

config = dotenv_values(".env")
chrome_driver_path = config["CHROME_WEBDRIVER_PATH"] 
options = Options()
options.use_chromium = True
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 10)  # Adjust timeout as needed

url = config["URL"]
driver.get(url)

try:
    # Wait for the page elements to load without using time.sleep()
    wait.until(EC.presence_of_element_located((By.XPATH, "//body")))

    while True:
        try:
            # Use WebDriverWait to wait for the "Ticket kopen" element to be clickable
            ticket_kopen_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[self::a or self::button][contains(., 'Ticket kopen')]")))
            print("Tickets are available!")
            ticket_kopen_element.click()
            beepy.beep # Alert the user
            break  # Break out of the loop after successfully clicking the button
        except TimeoutException:
            print("Tickets are not available at the moment. Checking again...")
            driver.refresh()
            wait.until(EC.presence_of_element_located((By.XPATH, "//body")))  # Wait for the page to load again

except KeyboardInterrupt:
    print("Script stopped by user.")

# Add a line to prevent the script from closing automatically
input("Press any key to exit...")  # Waits for user input before closing the browser
driver.quit()  # Make sure to quit the driver after completion to free resources