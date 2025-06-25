import pandas as pd
from config.setting import settings
import openai

openai.api_key = settings.OPENAI_API_KEY

class ProductRecommendationAgent:
    def __init__(self, product_file='data/product_catalog.csv'):
        self.products_df = pd.read_csv(product_file)

    def recommend_products_openai(self, query: str) -> list[dict]:
        """Use OpenAI to recommend top 3 products with basic info"""
        product_info = "\n".join([
            f"{row['product_id']}: {row['product_name']} - {row['description']} (Price: {row['price']})"
            for _, row in self.products_df.iterrows()
        ])

        prompt = f"""
You are a product recommendation engine.
The user asked: "{query}"
Based on the catalog below, recommend the top 3 relevant products.

Catalog:
{product_info}

Return your answer in JSON list format like:
[
  {{"product_id": 1001, "reason": "relevant to iPhone accessories"}},
  ...
]
"""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful recommendation engine."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=300
            )
            content = response.choices[0].message.content.strip()
            import json
            parsed = json.loads(content)
            # Match by product_id
            matched = self.products_df[self.products_df["product_id"].isin([p["product_id"] for p in parsed])]
            return matched.to_dict(orient="records")
        except Exception as e:
            print(f"[RecommendationAgent] OpenAI failed: {e}")
            return []

    def recommend_products_fallback(self, query: str) -> list[dict]:
        """Fallback method: keyword search in tags/category/product name"""
        query = query.lower()
        matches = self.products_df[
            self.products_df['tags'].str.contains(query, case=False, na=False) |
            self.products_df['category'].str.contains(query, case=False, na=False) |
            self.products_df['product_name'].str.contains(query, case=False, na=False)
        ]
        return matches.to_dict(orient='records')

    def recommend_products(self, query: str) -> list[dict]:
        """Hybrid recommender: Try OpenAI, fallback to keyword search"""
        results = self.recommend_products_openai(query)
        if results:
            return results
        return self.recommend_products_fallback(query)

    def get_related_products(self, product_id):
        """Get related products for a given product ID"""
        result = self.products_df[self.products_df['product_id'] == product_id]
        if not result.empty:
            related_ids = result.iloc[0]['related_products']
            if isinstance(related_ids, str):
                related_list = related_ids.split(",")
                return self.products_df[self.products_df['product_id'].astype(str).isin(related_list)].to_dict(orient='records')
        return []
