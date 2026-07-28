from dataclasses import dataclass


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