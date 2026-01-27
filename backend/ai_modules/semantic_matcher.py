from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class SemanticMatcher:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def match_careers(self, user_text, career_descriptions):
        user_embedding = self.model.encode([user_text])
        career_embeddings = self.model.encode(career_descriptions)

        similarities = cosine_similarity(user_embedding, career_embeddings)[0]

        results = []
        for i, score in enumerate(similarities):
            results.append((i, float(score)))

        # sort by similarity (descending)
        results.sort(key=lambda x: x[1], reverse=True)

        return results[:3]  # top 3 careers
