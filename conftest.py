import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture
def page():

    with sync_playwright() as p:

        from config import HEADLESS
        from config import SLOW_MO
        browser = p.chromium.launch(
            headless=HEADLESS,
            slow_mo=SLOW_MO
        )

        page = browser.new_page()

        yield page

        browser.close()