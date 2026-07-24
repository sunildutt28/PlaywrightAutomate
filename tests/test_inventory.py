from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

def test_add_item_to_cart(page, base_url):

    login = LoginPage(page)

    inventory = InventoryPage(page)

    login.open(base_url)

    login.login("standard_user", "secret_sauce")

    inventory.verify_inventory_loaded()

    inventory.add_backpack_to_cart()

    assert inventory.get_cart_count() == "1"