from ai.element_profile import ElementProfile
import json
import os


class ProfileStore:

    def __init__(self):
        self.profiles = {}

    def load_page(self, page_name):

        file_path = os.path.join(
            "profiles",
            f"{page_name}.json"
        )

        with open(file_path, "r") as file:
            data = json.load(file)

        self.profiles = {}

        for element_name, profile_data in data.items():
            self.profiles[element_name] = ElementProfile(**profile_data)

    def get(self, element_name):
        return self.profiles.get(element_name)