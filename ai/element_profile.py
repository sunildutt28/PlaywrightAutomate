from dataclasses import dataclass

"""Data class representing the profile of a web element. """

@dataclass
class ElementProfile:

    locator: str

    tag: str

    text: str

    role: str

    element_id: str

    element_type: str

    aria_label: str

    placeholder: str

    css_class: str

    parent_tag: str