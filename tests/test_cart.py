import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage

@pytest.mark.smoke
def test_add_backpack_to_cart(page, base_url):

    login = LoginPage(page)
    inventory = InventoryPage(page)
    cart = CartPage(page)

    login.open(base_url)

    login.login("standard_user", "secret_sauce")

    inventory.verify_inventory_loaded()

    inventory.add_backpack_to_cart()

    assert inventory.get_cart_count() == "1"

    inventory.open_cart()

    cart.verify_cart_loaded()

    cart.verify_product_present("Sauce Labs Backpack")

    cart.click_checkout()