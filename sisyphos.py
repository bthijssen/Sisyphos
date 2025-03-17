import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import beepy
import requests
from random import randint
from dotenv import dotenv_values

class TicketChecker:
    def __init__(self, config):
        """Initialize the TicketChecker with a WebDriver and configuration."""
        service = Service(executable_path=config["CHROME_WEBDRIVER_PATH"])
        self.driver = webdriver.Chrome(service=service)
        self.wait = WebDriverWait(self.driver, 10)
        self.url = config["URL"]
        self.config = config
    
    def open_page(self):
        """Open the URL in the browser."""
        self.driver.get(self.url)
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//body")))
    
    def check_tickets(self):
        """Continuously check for ticket availability and click if available."""
        while True:
            try:
                wait_time = randint(10,12)
                buy_ticket_element = WebDriverWait(self.driver, wait_time).until(
                    # EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Reserved')]"))
                    EC.element_to_be_clickable(
                        # this only selects the tickets without KWbN membership needed
                        ((By.XPATH, "//button[contains(text(), 'Buy ticket')]"))
                    )
                )
                print("Buy ticket element detected")
                buy_ticket_element.click()
                tickets_available_text = "Tickets are available!"
                self.send_push_notification(tickets_available_text)
                beepy.beep() # Alert the user
                print(tickets_available_text)
                break  # Exit loop after clicking the button
            except TimeoutException:
                if self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Too many attempts. Please wait a moment')]"):
                    sleep_time = 30
                    print(f"Sleeping {sleep_time} seconds")
                    time.sleep(sleep_time)
                print("Tickets are not available at the moment. Checking again...")
                self.driver.refresh()
                self.wait.until(EC.presence_of_element_located((By.XPATH, "//body")))
    
    def run(self):
        """Run the ticket checker script."""
        try:
            self.open_page()
            self.check_tickets()
        except KeyboardInterrupt:
            print("Script stopped by user.")
        except Exception as e:
            print(f"Unexpected error: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Close the browser and clean up resources."""
        input("Press any key to exit...")  # Prevents the script from closing automatically
        self.driver.quit()
        
    def send_push_notification(self, message, title="Notification"):
        url = self.config["PUSH_URL"]
        data = {
            "token": self.config["PUSH_API_TOKEN"],
            "user": self.config["PUSH_USER_KEY"],
            "message": message,
            "title": title
        }
        response = requests.post(url, data=data)
        print(response.json())  # Check the response
    
if __name__ == "__main__":
    config = dotenv_values(".env")
    options = Options() 
    checker = TicketChecker(config)
    checker.run()