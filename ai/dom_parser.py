from bs4 import BeautifulSoup
from ai.element_profile import ElementProfile

from bs4 import BeautifulSoup

class DOMParser:

    def __init__(self, page):
        self.page = page

    def get_dom(self):
        html = self.page.content()

        print("=" * 50)
        print(html[:1000])      # print first 1000 characters
        print("=" * 50)

        return BeautifulSoup(html, "html.parser")

    def create_profile(self, element):

        return ElementProfile(

            locator="",

            tag=element.name,

            text=element.get_text(strip=True),

            role=element.get("role", ""),

            element_id=element.get("id", ""),

            element_type=element.get("type", ""),

            aria_label=element.get("aria-label", ""),

            placeholder=element.get("placeholder", ""),

            css_class=" ".join(element.get("class", [])),

            parent_tag=element.parent.name if element.parent else ""
    )

    def get_buttons(self):

        soup = self.get_dom()

        buttons = []

        for button in soup.find_all("button"):
            buttons.append(self.create_profile(button))

        return buttons