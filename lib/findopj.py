import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException


class Findopj:
    def __init__(self, driver):
        self.driver = driver

    def findopj(self, pattern: str, delay: int = 10):
        """
        Find object by visibile on page
        """
        try:
            return WebDriverWait(self.driver, delay).until(
                EC.visibility_of_element_located((By.XPATH, pattern))
            )
        except UnexpectedAlertPresentException:
            time.sleep(2)
            return False
        except TimeoutException:
            return False
