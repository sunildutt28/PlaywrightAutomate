from pages.base_page import BasePage
from ai.element_profile import ElementProfile
import pytest


def test_click_recovery(page, base_url):

    page.goto(base_url)

    base_page = BasePage(page)

    profile = ElementProfile(
        locator="#user-name",
        tag="input",
        text="",
        role="",
        element_id="user-name",
        element_type="text",
        aria_label="",
        placeholder="Username",
        css_class="form_input",
        parent_tag="div"
    )

    # Store the profile
    base_page.profile_store.save(
    "username",
    profile
)

    base_page.click_with_recovery(
    "login_page",
    "username",
    "#user-names"   # Wrong locator to trigger recovery
)