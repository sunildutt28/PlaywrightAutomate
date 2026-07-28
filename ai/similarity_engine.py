from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim


class SimilarityEngine:

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def profile_to_text(self, profile):

        return (
            f"Tag: {profile.tag}. "
            f"Role: {profile.role}. "
            f"Type: {profile.element_type}. "
            f"ID: {profile.element_id}. "
            f"Placeholder: {profile.placeholder}. "
            f"Class: {profile.css_class}. "
            f"Parent: {profile.parent_tag}. "
            f"Text: {profile.text}."
        )

    def compare(self, profile1, profile2):

        text1 = self.profile_to_text(profile1)

        text2 = self.profile_to_text(profile2)

        embedding1 = self.model.encode(
            text1,
            convert_to_tensor=True
        )

        embedding2 = self.model.encode(
            text2,
            convert_to_tensor=True
        )

        score = cos_sim(
            embedding1,
            embedding2
        ).item()

        return score