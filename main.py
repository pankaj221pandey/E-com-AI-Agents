from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from agents.router_agent import RouterAgent
from agents.order_agent import OrderManagementAgent
from agents.recommendation_agent import ProductRecommendationAgent
from agents.faq_agent import FAQAgent
from utils.logger import setup_logger
from config.setting import settings
from utils.prompt_enginnering import PromptTemplates
from fastapi.middleware.cors import CORSMiddleware
import re
import math
import openai

# Init FastAPI & Logger
app = FastAPI()
logger = setup_logger("main_api")

# Load OpenAI key
openai.api_key = settings.OPENAI_API_KEY

# Load data files
product_file = settings.PRODUCT_CATALOG_PATH
orders_file = settings.ORDERS_PATH
knowledge_file = settings.KNOWLEDGE_BASE_PATH

# Initialize agents
router = RouterAgent()
order_agent = OrderManagementAgent(orders_file)
recommendation_agent = ProductRecommendationAgent(product_file)
faq_agent = FAQAgent(knowledge_file)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify frontend origin like ["http://localhost:5500"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/app", StaticFiles(directory="frontend", html=True), name="static")

# --------- Helper Functions ----------

def extract_order_id(query: str) -> str | None:
    match = re.search(r"\bORD\d{4,}\b", query, re.IGNORECASE)
    return match.group(0).upper() if match else None

def sanitize_floats(obj):
    if isinstance(obj, dict):
        return {k: sanitize_floats(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_floats(v) for v in obj]
    elif isinstance(obj, float):
        if math.isinf(obj) or math.isnan(obj):
            return None
    return obj

def generate_final_response_openai(order_info, recommendations, faq_answer, intents):
    order_info = order_info if "order" in intents else ""
    recommendations = recommendations if "product_recommendation" in intents else ""
    faq_answer = faq_answer if "faq" in intents else ""

    prompt = PromptTemplates.composite_response_prompt(
        order_info=order_info,
        recommendations=recommendations,
        faq_answer=faq_answer
    )
    try:
        result = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=300
        )
        return result.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"[OpenAI Final Response] Error: {e}")
        return None

# --------- Request/Response Schema ----------
class QueryRequest(BaseModel):
    user_id: str
    message: str


@app.get("/")
def root():
    return FileResponse("frontend/index.html")

@app.post("/query")
async def handle_user_query(payload: QueryRequest):
    user_id = payload.user_id
    user_query = payload.message

    logger.info(f"User ID: {user_id}")
    logger.info(f"User Query: {user_query}")

    intents = [i.lower() for i in router.route_query(user_query)]
    logger.info(f"Detected Intents: {intents}")

    response = {
        "user_id": user_id,
        "message": user_query,
        "intents": intents,
        "order_status": {},
        "product_recommendations": [],
        "faq_answer": "",
        "final_response": ""
    }

    if "greeting" in intents:
        response["final_response"] = "Hello! 👋 How can I assist you today? You can ask about your orders, returns, or product suggestions."
        return sanitize_floats(response)


    order_text = ""
    rec_text = ""
    faq_text = ""

    # ----------------- Order Handling -----------------
    if "order" in intents:
        order_id = extract_order_id(user_query)
        if order_id:
            result = order_agent.check_order_status(order_id)
            if "error" not in result:
                response["order_status"] = result
                order_text = (
                    f"Order ID: {result['order_id']}, "
                    f"Status: {result['status']}, "
                    f"Shipping Info: {result['shipping_info']}"
                )
            else:
                response["order_status"] = result
                response["final_response"] = f"📦 Order Issue: {result['error']}"
        else:
            results = order_agent.check_order_status_by_user_id(user_id)
            if results and "error" not in results[0]:
                response["order_status"] = results
                order_text = "\n".join([
                    f"Order ID: {r['order_id']}, Status: {r['status']}, Shipping Info: {r['shipping_info']}"
                    for r in results
                ])
            else:
                response["order_status"] = results[0]
                response["final_response"] = f"📦 Order Issue: {results[0]['error']}"

    # ----------------- Recommendation Handling -----------------
    if "product_recommendation" in intents:
        last_product = order_agent.get_last_order_product_name(user_id)
        if last_product:
            recs = recommendation_agent.recommend_products(last_product)
        else:
            recs = recommendation_agent.recommend_products(user_query)

        response["product_recommendations"] = recs
        if recs:
            rec_text = "\n".join([
                f"{r['product_name']} - {r['description']} (₹{r['price']})"
                for r in recs
            ])

    # ----------------- FAQ Handling -----------------
    if "faq" in intents:
        faq = faq_agent.answer_query(user_query)
        response["faq_answer"] = faq
        if faq:
            faq_text = faq

    if not intents and settings.ENABLE_OPENAI:
        try:
            openai_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful e-commerce assistant. Respond conversationally to user queries, even if they are casual messages like 'thanks' or 'hello'."},
                    {"role": "user", "content": user_query}
                ],
                temperature=0.5,
                max_tokens=200
            )
            response["final_response"] = openai_response.choices[0].message.content.strip()
            return sanitize_floats(response)
        except Exception as e:
            logger.error(f"[OpenAI fallback] Error: {e}")
            response["final_response"] = "I'm here to help, but something went wrong. Please try again later."
            return sanitize_floats(response)

    # ----------------- Final Response Composition -----------------
    if settings.ENABLE_OPENAI:
        final = generate_final_response_openai(order_text, rec_text, faq_text, intents)
        if final:
            response["final_response"] = final
        else:
        # Fallback response if OpenAI fails
            if order_text or rec_text or faq_text:
                fallback_parts = []
                if order_text:
                    fallback_parts.append(f"📦 {order_text}")
                if rec_text:
                    fallback_parts.append(f"🛍️ {rec_text}")
                if faq_text:
                    fallback_parts.append(f" {faq_text}")
                if fallback_parts:
                     response["final_response"] = "\n\n".join(fallback_parts)
            else:
                response["final_response"] = (
                    "I'm sorry, I couldn't find relevant information for your query. "
                    "Feel free to ask about your orders, return policy, or product suggestions."
                )
    else:
       if not response["final_response"]:  # fallback if OpenAI fails or returns empty
        fallback_parts = []
        if order_text:
            fallback_parts.append(f"📦 {order_text}")
        if rec_text:
            fallback_parts.append(f"🛍️ {rec_text}")
        if faq_text:
            fallback_parts.append(f"❓ {faq_text}")

        response["final_response"] = "\n\n".join(fallback_parts) if fallback_parts else "I'm here to help, but I need a bit more info."


    return sanitize_floats(response)
