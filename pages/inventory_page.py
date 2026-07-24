from pages.base_page import BasePage


class InventoryPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

        self.inventory_title = ".title"
        self.cart_badge = ".shopping_cart_badge"

        self.backpack = "[data-test='add-to-cart-sauce-labs-backpack']"

    def verify_inventory_loaded(self):
        self.wait_for(self.inventory_title)

    def add_backpack_to_cart(self):
        self.click(self.backpack)

    def get_cart_count(self):

        if self.is_visible(self.cart_badge):
            return self.get_text(self.cart_badge)

        return "0"