# 🛒 E-commerce AI Agents

An intelligent conversational assistant for E-commerce platforms built with **FastAPI**, supporting:
- 📦 Order Tracking  
- 🛍️ Product Recommendations  
- ❓ FAQs & Return Policies  

This system uses **Intent Detection**, **Retrieval-Augmented Generation (RAG)**, and **OpenAI's GPT models** to handle customer queries naturally.

## 🚀 Features

✅ **Multi-Intent Recognition** - Automatically detects user intent: `order`, `faq`, `product_recommendation`, or `greeting`  
✅ **Order Management** - Fetches order status using Order ID or User ID  
✅ **Product Recommendation** - Suggests products based on previous purchases  
✅ **FAQ Engine** - Uses RAG + OpenAI to provide answers from knowledge base  
✅ **Chat UI** - Simple chatbot widget with typing animation  
✅ **Docker Support** - Easy deployment with Docker  

## 🧠 Tech Stack

- **Backend**: FastAPI, Python 3.10  
- **AI**: OpenAI GPT, Sentence Transformers  
- **Frontend**: HTML + Vanilla JS Chat Widget  
- **Database**: CSV-based simulation  
- **Testing**: Pytest  

## ⚙️ Quick Start

### 1. Clone & Setup
```bash
git clone https://github.com/pankaj221pandey/E-com-AI-Agents.git
cd E-com-AI_Agents
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment
Create `.env` file:
```env
OPENAI_API_KEY=your_openai_key
ENABLE_OPENAI=true
ORDERS_PATH=data/orders.csv
PRODUCT_CATALOG_PATH=data/products.csv
KNOWLEDGE_BASE_PATH=data/knowledge_base.json
```

### 3. Run the App
```bash
uvicorn main:app --reload
```
Open: http://localhost:8000

## 🐳 Docker (Optional)
```bash
docker build -t e-com-ai .
docker run -dp 8000:8000 e-com-ai
```

## 💬 Try These Queries

- **Order Status**: "Where is my order?", "Track order ORD12345"
- **Recommendations**: "Suggest a case for iPhone 15", "What should I buy?"
- **FAQs**: "What is your return policy?", "Do you offer discounts?"
- **Greetings**: "Hi", "Hello", "Thanks"

## 🧪 Testing
```bash
pytest tests/test_integration.py
```
## Flow-chart
![E-com-agents-flow](https://github.com/user-attachments/assets/e7e84ccc-e68c-40cb-a95a-eb787ebf85c4)

**Developed by Pankaj Pandey** ❤️
