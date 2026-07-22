import pytest
from playwright.sync_api import sync_playwright

import os
from datetime import datetime


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield

    report = outcome.get_result()

    if report.when == "call" and report.failed:

        page = getattr(item, "page", None)

        if page:

            os.makedirs("screenshots", exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            screenshot_name = f"{item.name}_{timestamp}.png"

            page.screenshot(
                path=f"screenshots/{screenshot_name}"
            )

            print(f"\nScreenshot saved: {screenshot_name}")

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