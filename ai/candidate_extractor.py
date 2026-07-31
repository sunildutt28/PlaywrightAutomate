from .dom_parser import DOMParser

"""CandidateExtractor class is responsible for extracting candidate web elements from the DOM. 
It uses the DOMParser to parse the page content and create profiles for various HTML elements 
such as input boxes, buttons, links, selects, and textareas. 
The extracted candidates can be used for further processing or analysis. """

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