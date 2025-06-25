# utils/prompt_engineering.py

class PromptTemplates:
    """Template class for generating dynamic prompts for OpenAI agents."""

    @staticmethod
    def order_status_prompt(order_id: str) -> str:
        """Prompt for querying order status."""
        order_id = order_id.strip().upper()
        return f"""You are the Order Management Agent.
The user is asking about the order status for Order ID: {order_id}.
Check the order details and respond clearly with status and shipping information."""

    @staticmethod
    def product_recommendation_prompt(query: str) -> str:
        """Prompt for suggesting products based on user query."""
        query = query.strip()
        return f"""You are the Product Recommendation Agent.
The user asked: "{query}"
Based on this query, suggest 3–5 relevant products with names, features, and prices.
Focus on trending or highly rated items."""

    @staticmethod
    def faq_answer_prompt(question: str) -> str:
        """Prompt for answering user FAQs based on internal knowledge base."""
        question = question.strip()
        return f"""You are the FAQ Agent.
The user asked: "{question}"
Respond using company return/refund/shipping policies. Be accurate and polite."""

    @staticmethod
    def composite_response_prompt(order_info: str, recommendations: str, faq_answer: str):
        return f"""
You are an AI assistant that replies like a chatbot.

Please answer the user’s query using the following 3 sections (if provided).
DO NOT ignore any section.

1. Order Info:
{order_info or "No order-related info."}

2. Product Recommendations:
{recommendations or "No recommendations found."}

3. FAQ Answer:
{faq_answer or "No FAQ response found."}

Your job is to respond to the user in a friendly, short, and helpful way.
Don't repeat the user's question. Don't say “if you need anything else.”
Make it sound like a smart chatbot, not an email.

Reply now:
"""


    @staticmethod
    def error_handling_prompt(error_message: str) -> str:
        """Prompt to handle errors during response generation."""
        return f"""An error occurred while processing the request: "{error_message}".
Politely ask the user to try again or rephrase their question.
If the problem continues, suggest contacting support."""
