class ProfileStore:

    def __init__(self):
        self.profiles = {}

    def save(self, element_name, profile):
        self.profiles[element_name] = profile

    def get(self, element_name):
        return self.profiles.get(element_name)

    def exists(self, element_name):
        return element_name in self.profiles