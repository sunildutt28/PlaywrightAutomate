from ai.dom_parser import DOMParser
from ai.profile_generator import ProfileGenerator

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


def test_generate_cart_profile(page):

    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    cart_page = CartPage(page)

    # Open application
    login_page.open("https://www.saucedemo.com/")

    # Login
    login_page.login("standard_user", "secret_sauce")

    # Add product and go to cart
    inventory_page.add_backpack_to_cart()
    inventory_page.open_cart()

    # Verify cart page
    cart_page.verify_cart_loaded()

    # Generate profile
    parser = DOMParser(page)
    profiles = parser.get_elements()

    ProfileGenerator().generate(
        "cart_page",
        profiles
    )