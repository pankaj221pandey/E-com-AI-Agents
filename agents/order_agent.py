# agents/order_agent.py

import pandas as pd
from utils.prompt_enginnering import PromptTemplates

class OrderManagementAgent:
    def __init__(self, orders_file: str):
        self.orders_file = orders_file
        self.df = pd.read_csv(self.orders_file)

        # Clean NaN and inf values to prevent JSON serialization issues
        self.df.replace([float('inf'), float('-inf')], None, inplace=True)
        self.df.fillna("", inplace=True)

    def check_order_status(self, order_id: str) -> dict:
        order_id = order_id.strip().upper()
        match = self.df[self.df['order_id'].str.upper() == order_id]

        prompt = PromptTemplates.order_status_prompt(order_id)
        print("📦 Order Prompt:\n", prompt)  # For debug/logging — can be removed

        if not match.empty:
            row = match.iloc[0]
            return {
                "order_id": row['order_id'],
                "status": row['status'],
                "shipping_info": row['shipping_info'] or "Not available yet"
            }
        return {"error": "Order not found."}

    def check_order_status_by_user_id(self, user_id: str) -> list[dict]:
        user_id = user_id.strip()
        match = self.df[self.df['user_id'].str.strip() == user_id]

        if match.empty:
            return [{"error": "No orders found for this user."}]

        return [
            {
                "order_id": row['order_id'],
                "status": row['status'],
                "shipping_info": row['shipping_info'] or "Not available yet"
            }
            for _, row in match.iterrows()
        ]

    def get_last_order_product_name(self, user_id: str) -> str | None:
        user_id = user_id.strip()
        user_orders = self.df[self.df['user_id'].str.strip() == user_id]

        if user_orders.empty:
            return None

        if "order_date" in user_orders.columns:
            user_orders = user_orders.sort_values(by="order_date", ascending=False)

        last_order = user_orders.iloc[0]
        return last_order.get("product_name") or None
