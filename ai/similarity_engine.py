from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim


class SimilarityEngine:

    model = None

    def __init__(self):

        if SimilarityEngine.model is None:
            print("Loading AI model...")
            SimilarityEngine.model = SentenceTransformer("all-MiniLM-L6-v2")

        self.model = SimilarityEngine.model

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
    def get_embedding(self, profile):

        text = self.profile_to_text(profile)

        return self.model.encode(
            text,
            convert_to_tensor=True
        )
    
    def compare(self, embedding1, embedding2):

        return cos_sim(embedding1, embedding2).item()

        
    def find_best_match(self, original_profile, candidates):

        best_score = -1
        best_candidate = None

        original_embedding = self.get_embedding(original_profile)

        for candidate in candidates:

            candidate_embedding = self.get_embedding(candidate)

            score = self.compare(
                original_embedding,
                candidate_embedding
            )

            print(f"{candidate.element_id} -> {score:.4f}")
            
            if score > best_score:
                best_score = score
                best_candidate = candidate

        return best_candidate, best_score