from playwright.sync_api import expect

from ai.recovery_engine import RecoveryEngine
from ai.profile_store import ProfileStore
from utils.logger import logger
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


class BasePage:

    def __init__(self, page):

        self.page = page

        self.profile_store = ProfileStore()

        self.recovery_engine = RecoveryEngine(page)

    def click(self, locator):
        self.page.locator(locator).click()

    def click_with_recovery(
            self,
            page_name,
            element_name,
            locator):
        """Attempts to click an element using the original locator.
        If the locator fails, uses AI-based recovery to find the
        most similar element on the current page.
        """
        try:

            self.page.locator(locator).click()

            print("Normal click succeeded.")

        except  PlaywrightTimeoutError:

            print("Locator failed.")

            self.profile_store.load_page(page_name)

            profile = self.profile_store.get(element_name)

            print(f"Looking for: {element_name}")

            recovered_profile, score = self.recovery_engine.recover(profile)

            print(
                f"Recovered using "
                f"{recovered_profile.locator} with score {score}" 
            )

            self.page.locator(
                recovered_profile.locator
            ).click()
                    
    def fill(self, locator, value):
        self.page.locator(locator).fill(value)

    def fill_with_recovery(self, page_name, element_name, locator, value):
        print(">>> fill_with_recovery CALLED <<<")

        try:
            self.page.locator(locator).fill(value)
            print("Normal fill succeeded.")

        except PlaywrightTimeoutError as e:
            print(f"Locator failed: {e}")

            self.profile_store.load_page(page_name)

            profile = self.profile_store.get(element_name)

            recovered_profile, score = self.recovery_engine.recover(profile)

            print(f"Recovered using {recovered_profile.locator} with score {score}")

            self.page.locator(
                recovered_profile.locator
            ).fill(value)

    def get_text(self, locator):
        return self.page.locator(locator).text_content().strip()

    def is_visible(self, locator):
        return self.page.locator(locator).is_visible()

    def wait_for(self, locator):
        expect(self.page.locator(locator)).to_be_visible()

    def get_url(self):
        return self.page.url