from ai.element_profile import ElementProfile
import json
import os

"""ProfileStore class is responsible for loading and storing element profiles for different web pages. """

class ProfileStore:

    def __init__(self):
        self.profiles = {}
        self.current_page = None

    def load_page(self, page_name):

        
        if self.current_page == page_name:
            return

        file_path = os.path.join(
            "profiles",
            f"{page_name}.json"
        )
        print(f"Loading file: {file_path}")

        with open(file_path, "r") as file:
            data = json.load(file)

        self.profiles = {
            name: ElementProfile(**profile)
            for name, profile in data.items()
        }
        print(self.profiles.keys())

        self.current_page = page_name

    def get(self, element_name):
        return self.profiles.get(element_name)