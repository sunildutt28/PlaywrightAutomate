import pytest
from pages.login_page import LoginPage
from test_data.login_data import LOGIN_USERS


@pytest.mark.parametrize(
    "username,password,expected_success,expected_message",
    LOGIN_USERS
)
def test_valid_login(page, base_url, username, password, expected_success, expected_message):

    login_page = LoginPage(page)

    login_page.open(base_url)

    login_page.login(username, password)

    if expected_success:
        assert "inventory" in page.url
    else:
        login_page.verify_error_message(expected_message)