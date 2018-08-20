from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class PopNewEbookPage(object):

    """
    Page Object Pattern for the Packthub website with new free ebook.
    """
    def __init__(self, driver):
        self.driver = driver
        self.xpathLoginButton = '//*[@id="account-bar-login-register"]/a[1]/div'
        self.xpathUserInput = '//*[@id="email"]'
        self.xpathPassInput = '//*[@id="password"]'
        self.xpathLoginSubmit = '//*[@id="edit-submit-1"]'
        self.xpathClaimEbookButton = '//*[@id="free-learning-claim"]'

        self.xpathHiddenLoginButton = '//*[@id="ppv4"]/div[7]/div[1]/div[1]/div[1]'
        self.xpathHiddenUserInput = '//*[@id="email"]'
        self.xpathHiddenPassInput = '//*[@id="password"]'
        self.xpathHiddenLoginSubmit = '//*[@id="edit-submit-1"]'

        self.xpathMenuIcon = '//*[@id="menuIcon"]'
        self.xpathNewEbook = '//*[@id="deal-of-the-day"]/div/div/div[2]/div[2]/h2'

    def login(self, username, userpass):
        print("PopNewEbookPage : login")

        try:
            self.driver.find_element(By.XPATH, self.xpathLoginButton).click()
            time.sleep(5)
            self.driver.find_element(By.XPATH, self.xpathLoginButton).click()
            self.driver.find_element(By.XPATH, self.xpathUserInput).send_keys(username)
            self.driver.find_element(By.XPATH, self.xpathPassInput).send_keys(userpass)
            self.driver.find_element(By.XPATH, self.xpathLoginSubmit).click()
            self.driver.find_element(By.XPATH, self.xpathClaimEbookButton).click()
        except Exception as e:
            # if browser to small
            try:
                self.driver.find_element(By.XPATH, self.xpathMenuIcon).click()
                time.sleep(5)
                self.driver.find_element(By.XPATH, self.xpathHiddenLoginButton).click()
                self.driver.find_element(By.XPATH, self.xpathHiddenUserInput).send_keys(username)
                self.driver.find_element(By.XPATH, self.xpathHiddenPassInput).send_keys(userpass)
                self.driver.find_element(By.XPATH, self.xpathHiddenLoginSubmit).click()
                self.driver.find_element(By.XPATH, self.xpathClaimEbookButton).click()
                time.sleep(5)
            except Exception as e:
                raise
