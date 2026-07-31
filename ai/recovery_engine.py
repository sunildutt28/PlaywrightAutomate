from ai.candidate_extractor import CandidateExtractor
from ai.similarity_engine import SimilarityEngine

"""RecoveryEngine class is responsible for recovering web elements using AI-based similarity matching. """

class RecoveryEngine:

    def __init__(self, page):

        self.page = page

        self.extractor = CandidateExtractor(page)

        self.similarity = SimilarityEngine()

    def recover(self, original_profile):

        candidates = self.extractor.get_all_candidates()

        best_match, score = self.similarity.find_best_match(
            original_profile,
            candidates
        )

        return best_match, score