from conftest import page
from utils.logger import logger
from playwright.sync_api import expect
from pages.base_page import BasePage

class LoginPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

        self.username = "[data-test='username']"
        self.password = "[data-test='passwords1']"
        self.login_button = "[data-test='login-button']"
        self.error_message = "[data-test='error']"


    def open(self, url):
        logger.info(f"Opening URL: {url}")
        self.page.goto(url)

    def login(self, username, password):
        #self.fill(self.username, username)
        self.fill_with_recovery(
            "login_page",
            "username",
            self.username,
            username
        )
        self.fill_with_recovery(
            "login_page",
            "password",
            self.password,
            password
            )
        self.click_with_recovery("login_page", "login_button", self.login_button)

    def verify_error_message(self, expected_message):
        expect(self.page.locator(self.error_message)).to_have_text(expected_message)