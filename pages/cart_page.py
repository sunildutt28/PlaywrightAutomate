from pages.base_page import BasePage


class CartPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

        self.cart_title = ".title"
        self.cart_item_name = ".inventory_item_name"
        self.checkout_button = "[data-test='checkout']"
        self.continue_shopping_button = "[data-test='continue-shopping']"
        self.remove_backpack_button = "[data-test='remove-sauce-labs-backpack']"

    def verify_cart_loaded(self):
        self.wait_for(self.cart_title)

    def verify_product_present(self, product_name):
        assert self.get_text(self.cart_item_name) == product_name

    def click_checkout(self):
        self.click(self.checkout_button)

    def continue_shopping(self):
        self.click(self.continue_shopping_button)

    def remove_backpack(self):
        self.click(self.remove_backpack_button)