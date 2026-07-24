from pages.base_page import BasePage


class InventoryPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

        self.inventory_title = ".title"
        self.cart_badge = ".shopping_cart_badge"

        self.backpack = "[data-test='add-to-cart-sauce-labs-backpack']"
        self.shopping_cart = ".shopping_cart_link"

        self.bike_light = "[data-test='add-to-cart-sauce-labs-bike-light']"

    def verify_inventory_loaded(self):
        self.wait_for(self.inventory_title)

    def add_backpack_to_cart(self):
        self.click(self.backpack)

    def get_cart_count(self):

        if self.is_visible(self.cart_badge):
            return self.get_text(self.cart_badge)

        return "0"
    def add_bike_light_to_cart(self):
        self.click(self.bike_light)

    def open_cart(self):
        self.click(self.shopping_cart)