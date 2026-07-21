from pages.login_page import LoginPage


def test_valid_login(page):

    login_page = LoginPage(page)

    login_page.open()

    login_page.login(
        "standard_user",
        "secret_sauce"
    )

    assert "inventory" in page.url