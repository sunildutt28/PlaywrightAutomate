from playwright.sync_api import expect

from ai.recovery_engine import RecoveryEngine
from ai.profile_store import ProfileStore


class BasePage:

    def __init__(self, page):
        self.page = page
        self.profile_store = ProfileStore()

        self.recovery_engine = RecoveryEngine(page)

    def click(self, locator):
        self.page.locator(locator).click()

    def click_with_recovery(self, element_name, locator):

        try:
            self.page.locator(locator).click()


        except Exception:
            print("Normal click failed")

            print("Loading profile...")

            original_profile = self.profile_store.get(element_name)
            
            print("Starting recovery...")
            if original_profile is None:
                raise Exception(
                    f"No stored profile for '{element_name}'"
                )

            recovered_profile, score = self.recovery_engine.recover(
                original_profile
            )

            print(f"Recovered locator: {recovered_profile.locator}")

            print(f"Similarity: {score:.3f}")

            if recovered_profile is None:
                raise Exception(
                    f"Recovery failed for '{element_name}'"
                )
            print("Retrying click...")
            self.page.locator(recovered_profile.locator).click()

                    
    def fill(self, locator, value):
        self.page.locator(locator).fill(value)

    def get_text(self, locator):
        return self.page.locator(locator).text_content().strip()

    def is_visible(self, locator):
        return self.page.locator(locator).is_visible()

    def wait_for(self, locator):
        expect(self.page.locator(locator)).to_be_visible()

    def get_url(self):
        return self.page.url