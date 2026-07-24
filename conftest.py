import pytest
from playwright.sync_api import sync_playwright
from utils.logger import logger

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

from config import BROWSER, URLS

def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default=BROWSER,
        help="Browser to run tests: chromium, firefox or webkit"
    )
    parser.addoption(
        "--env",
        action="store",
        default="qa",
        help="Environment for the application"
    )

@pytest.fixture
def page(request):

    with sync_playwright() as p:

        from config import HEADLESS
        from config import SLOW_MO
        selected_browser = request.config.getoption("--browser")
        
        
        logger.info(f"Selected Browser: {selected_browser}")

        if selected_browser == "chromium":
            browser = p.chromium.launch(
                headless=HEADLESS,
                slow_mo=SLOW_MO
            )

        elif selected_browser == "firefox":
            browser = p.firefox.launch(
                headless=HEADLESS,
                slow_mo=SLOW_MO
            )

        elif selected_browser == "webkit":
            browser = p.webkit.launch(
                headless=HEADLESS,
                slow_mo=SLOW_MO
            )

        else:
            raise ValueError(
                f"Unsupported browser: {selected_browser}. "
                "Supported browsers are: chromium, firefox, webkit."
            )
        
        page = browser.new_page()

        # Store the page object with the current test
        request.node.page = page

        yield page

        browser.close()

@pytest.fixture
def base_url(request):
    selected_env = request.config.getoption("--env")
    return URLS[selected_env]
