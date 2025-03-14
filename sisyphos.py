import time
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
options = Options()
service = Service(executable_path=config["CHROME_WEBDRIVER_PATH"] )
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 10)  # Adjust timeout as needed

class TicketChecker:
    def __init__(self, config):
        """Initialize the TicketChecker with a WebDriver and configuration."""
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
        self.url = config["URL"]
    
    def open_page(self):
        """Open the URL in the browser."""
        self.driver.get(self.url)
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//body")))
    
    def check_tickets(self):
        """Continuously check for ticket availability and click if available."""
        while True:
            try:
                ticket_kopen_element = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//*[self::a or self::button][contains(., 'Ticket kopen')]"))
                )
                print("Tickets are available!")
                ticket_kopen_element.click()
                beepy.beep()  # Alert the user
                break  # Exit loop after clicking the button
            except TimeoutException:
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
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Close the browser and clean up resources."""
        input("Press any key to exit...")  # Prevents the script from closing automatically
        self.driver.quit()

# Example usage
if __name__ == "__main__":
    config = {"URL": "https://example.com/tickets"}  # Replace with actual URL
    checker = TicketChecker(config)
    checker.run()