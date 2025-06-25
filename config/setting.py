# config/settings.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    # Application Name
    APP_NAME = "E-commerce AI Agent System"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

    # LLM Settings
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")  # or 'anthropic', 'google', etc.
    LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "gpt-3.5-turbo")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ENABLE_OPENAI: bool = True


    # Data Paths
    PRODUCT_CATALOG_PATH = os.getenv("PRODUCT_CATALOG_PATH", "../data/product_catalog.csv")
    ORDERS_PATH = os.getenv("ORDERS_PATH", "../data/orders.csv")
    KNOWLEDGE_BASE_PATH = os.getenv("KNOWLEDGE_BASE_PATH", "../data/knowledge_base.json")

    # Cache
    CACHE_TTL = int(os.getenv("CACHE_TTL", "3600"))  # in seconds
    USE_CACHE = os.getenv("USE_CACHE", "True").lower() == "true"

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "logs/app.log")

    # RAG Settings
    RAG_SIMILARITY_THRESHOLD = float(os.getenv("RAG_SIMILARITY_THRESHOLD", "0.5"))
    RAG_MODEL_NAME = os.getenv("RAG_MODEL_NAME", "all-MiniLM-L6-v2")

    # Router Agent Settings
    ROUTER_KEYWORD_MATCHING_ENABLED = os.getenv("ROUTER_KEYWORD_MATCHING_ENABLED", "True").lower() == "true"
    ROUTER_INTENT_CONFIDENCE_THRESHOLD = float(os.getenv("ROUTER_INTENT_CONFIDENCE_THRESHOLD", "0.6"))

    # Async Processing
    USE_ASYNC = os.getenv("USE_ASYNC", "False").lower() == "true"

# Instantiate settings object for easy import
settings = Settings()