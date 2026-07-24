from conftest import page
from utils.logger import logger
from playwright.sync_api import expect

class LoginPage:


    def __init__(self, page):
        self.page = page

        self.username = self.page.locator("[data-test='username']")
        self.password = self.page.locator("[data-test='password']")
        self.login_button = self.page.locator("[data-test='login-button']")
        self.error_message = self.page.locator("[data-test='error']")


    def open(self, url):
        logger.info(f"Opening URL: {url}")
        self.page.goto(url)

    def login(self, username, password):
        logger.info(f"Logging in as {username}")
        self.username.fill(username)
        self.password.fill(password)
        self.login_button.click()
        

    

    def verify_error_message(self, expected_message):
        expect(self.error_message).to_have_text(expected_message)