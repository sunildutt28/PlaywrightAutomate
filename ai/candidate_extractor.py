from .dom_parser import DOMParser


class CandidateExtractor:

    def __init__(self, page):
        self.page = page
        self.parser = DOMParser(page)

    def get_all_candidates(self):

        candidates = []

        soup = self.parser.get_dom()

        for input_box in soup.find_all("input"):
            candidates.append(
            self.parser.create_profile(input_box)
        )

        for button in soup.find_all("button"):
            candidates.append(
            self.parser.create_profile(button)
            )
        for link in soup.find_all("a"):
            candidates.append(
                self.parser.create_profile(link)
            )
        for select in soup.find_all("select"):
            candidates.append(
                self.parser.create_profile(select)
            )
        for textarea in soup.find_all("textarea"):
            candidates.append(
                self.parser.create_profile(textarea)
            )

        return candidates