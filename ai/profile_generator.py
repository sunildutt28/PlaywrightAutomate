import json
import os


class ProfileGenerator:

    def generate(self, page_name, profiles):

        data = {}

        for profile in profiles:

            key = (
                profile.element_id
                if profile.element_id
                else profile.tag
            )

            data[key] = vars(profile)

        os.makedirs("profiles", exist_ok=True)

        with open(f"profiles/{page_name}.json", "w") as file:

            json.dump(
                data,
                file,
                indent=2
            )