from conftest import page
from utils.logger import logger
from playwright.sync_api import expect
from pages.base_page import BasePage

class LoginPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

        self.username = "[data-test='username']"
        self.password = "[data-test='password']"
        self.login_button = "[data-test='login-button']"
        self.error_message = "[data-test='error']"


    def open(self, url):
        logger.info(f"Opening URL: {url}")
        self.page.goto(url)

    def login(self):
        logger.info(f"Logging in as {self.username}")
        self.username.fill(self.username)
        self.password.fill(self.password)
        self.click(self.login_button)
        

    def verify_error_message(self, expected_message):
        expect(self.get_text(self.error_message)).to_have_text(expected_message)