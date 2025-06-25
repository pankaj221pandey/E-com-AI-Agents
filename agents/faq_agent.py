import json
from sentence_transformers import SentenceTransformer, util
from config.setting import settings
import openai

openai.api_key = settings.OPENAI_API_KEY

class FAQAgent:
    def __init__(self, knowledge_file='data/knowledge_base.json'):
        with open(knowledge_file, 'r') as f:
            self.knowledge_base = json.load(f)

        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.questions = [item['question'] for item in self.knowledge_base]
        self.answers = [item['answer'] for item in self.knowledge_base]
        self.question_embeddings = self.model.encode(self.questions, convert_to_tensor=True)

    def answer_query_openai(self, query: str) -> str | None:
        """Try answering FAQ via OpenAI using knowledge base"""
        context = "\n".join(
            [f"Q: {item['question']}\nA: {item['answer']}" for item in self.knowledge_base]
        )
        prompt = f"""
You are a customer support assistant. Use the FAQ below to answer the user's question.

FAQ:
{context}

User Question:
{query}

Answer:
"""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful FAQ assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=200
            )
            answer = response.choices[0].message.content.strip()
            return answer
        except Exception as e:
            print(f"[FAQAgent] OpenAI failed: {e}")
            return None

    def answer_query_rag(self, query: str, threshold=0.5) -> str:
        """Fallback: Use semantic similarity (RAG)"""
        query_embedding = self.model.encode(query, convert_to_tensor=True)
        cosine_scores = util.cos_sim(query_embedding, self.question_embeddings)

        best_match_idx = cosine_scores.argmax()
        best_score = cosine_scores[0][best_match_idx].item()

        if best_score >= threshold:
            return self.answers[best_match_idx]
        else:
            return "Apologies, I couldn't locate a relevant answer to your query. Please feel free to contact our support team for further assistance."

    def answer_query(self, query: str) -> str:
        """Hybrid: OpenAI first, fallback to RAG"""
        response = self.answer_query_openai(query)
        if response:
            return response
        return self.answer_query_rag(query)
