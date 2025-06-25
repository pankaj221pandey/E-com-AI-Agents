# utils/rag.py

import json
from sentence_transformers import SentenceTransformer, util


class RAGHelper:
    """
    Retrieval-Augmented Generation helper to match user questions
    against a pre-loaded knowledge base using semantic similarity.
    """

    def __init__(self, knowledge_path: str = "data/knowledge_base.json"):
        self.knowledge_path = knowledge_path
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self._load_knowledge_base()

    def _load_knowledge_base(self):
        """Load knowledge base and compute embeddings."""
        try:
            with open(self.knowledge_path, "r", encoding="utf-8") as f:
                self.knowledge = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.knowledge = []

        self.questions = [item.get("question", "") for item in self.knowledge]
        self.answers = [item.get("answer", "") for item in self.knowledge]

        if self.questions:
            self.embeddings = self.model.encode(self.questions, convert_to_tensor=True)
        else:
            self.embeddings = None

    def get_answer(self, query: str, threshold: float = 0.5) -> str:
        """
        Return the most relevant answer from the knowledge base.
        
        Args:
            query (str): User's question.
            threshold (float): Minimum confidence score for a valid match.
        
        Returns:
            str: The matched answer or a default fallback response.
        """
        if not query or not self.embeddings:
            return "Apologies, I couldn't locate a relevant answer to your query. Please feel free to contact our support team for further assistance."

        query_embedding = self.model.encode(query, convert_to_tensor=True)
        scores = util.cos_sim(query_embedding, self.embeddings)

        best_idx = scores.argmax().item()
        best_score = scores[0][best_idx].item()

        if best_score >= threshold:
            return self.answers[best_idx]

        return "Apologies, I couldn't locate a relevant answer to your query. Please feel free to contact our support team for further assistance."
