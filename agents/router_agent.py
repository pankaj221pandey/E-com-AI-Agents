import openai
import json
from config.setting import settings

openai.api_key = settings.OPENAI_API_KEY

class RouterAgent:
    def __init__(self):
        self.available_intents = ["order", "product_recommendation", "faq", "greeting"]
        self.intent_keywords = {
             "order": [
                "order", "status", "shipping", "deliver", "shipment", "where is my order",
                "track", "tracking", "dispatched", "shipped", "arriving", "arrival", "expected"
            ],
            "product_recommendation": [
                "recommend", "suggest", "best", "case", "buy", "accessories", "products",
                "popular", "trending", "new", "top", "deal", "which", "available", "options", "find me"
            ],
            "faq": [
                "return", "policy", "refund", "warranty", "discount", "offers", "support",
                "help", "contact", "how do I", "guarantee", "cancel", "replace", "exchange", "terms", "question"
            ],
            "greeting": ["hi", "hello", "hey", "good morning", "good evening", "how are you", "what's up"]

        }

    def classify_intent_openai(self, query: str) -> list[str]:
        """Use OpenAI to classify user query into one or more intents"""
        prompt = f"""
You are an intent classification agent. Classify the user query into one or more of the following intents:
- order
- product_recommendation
- faq

Return only a JSON array of detected intents like ["order", "faq"].

Examples:

User: "Where is my order? The order ID is ORD12345."
Output: ["order"]

User: "I don’t like the product. What’s your return policy?"
Output: ["order", "faq"]

User: "Suggest a good case for iPhone 15 Pro"
Output: ["product_recommendation"]

User: "{query}"
Output:
"""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for intent classification."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0,
                max_tokens=100
            )

            result = response.choices[0].message.content.strip()
            intents = json.loads(result)

            # Validate output
            if isinstance(intents, list):
                return [i for i in intents if i in self.available_intents]
        except Exception as e:
            print(f"[RouterAgent] OpenAI failed: {e}")

        return None  # trigger fallback

    def classify_intent_fallback(self, query: str) -> list[str]:
        """Fallback keyword-based classification"""
        query = query.lower()
        matched = set()
        for intent, keywords in self.intent_keywords.items():
            if any(kw in query for kw in keywords):
                matched.add(intent)
        return list(matched)

    def classify_intent(self, query: str) -> list[str]:
        """Use OpenAI, fallback to static rules if needed"""
        intents = self.classify_intent_openai(query)
        if intents is None or not intents:
            return self.classify_intent_fallback(query)
        return intents

    def route_query(self, query: str) -> list[str]:
        return self.classify_intent(query)
