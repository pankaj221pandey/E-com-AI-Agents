import os
import pandas as pd

# Create data directory if not exists
os.makedirs("data", exist_ok=True)

# --- Product Catalog Data (10 items) ---
product_data = [
    {
        "product_id": 1001,
        "product_name": "iPhone 15 Pro Max Case",
        "category": "Phone Accessories",
        "brand": "Spigen",
        "price": 29.99,
        "description": "Slim and rugged case with military-grade drop protection",
        "features": "drop protection, slim design",
        "tags": "case, iPhone 15, rugged",
        "rating": 4.7,
        "in_stock": True,
        "related_products": "1002,1003"
    },
    {
        "product_id": 1002,
        "product_name": "iPhone 15 Silicone Case",
        "category": "Phone Accessories",
        "brand": "Apple",
        "price": 19.99,
        "description": "Soft touch silicone with multiple color options",
        "features": "colorful, shock absorption",
        "tags": "case, iPhone 15, colorful",
        "rating": 4.5,
        "in_stock": True,
        "related_products": "1001,1003"
    },
    {
        "product_id": 1003,
        "product_name": "MagSafe Charger",
        "category": "Phone Accessories",
        "brand": "Apple",
        "price": 34.99,
        "description": "Magnetic charging pad compatible with iPhone 15",
        "features": "wireless charging, magnetic",
        "tags": "charger, MagSafe, iPhone 15",
        "rating": 4.6,
        "in_stock": True,
        "related_products": "1004"
    },
    {
        "product_id": 1004,
        "product_name": "USB-C to Lightning Cable",
        "category": "Cables & Adapters",
        "brand": "Anker",
        "price": 14.99,
        "description": "Durable 2m cable with fast charging support",
        "features": "fast charging, durable",
        "tags": "cable, USB-C, iPhone",
        "rating": 4.8,
        "in_stock": True,
        "related_products": "1003"
    },
    {
        "product_id": 1005,
        "product_name": "Apple MagSafe Wallet",
        "category": "Phone Accessories",
        "brand": "Apple",
        "price": 39.99,
        "description": "Snap-on wallet for iPhone with RFID protection",
        "features": "RFID blocking, magnetic attachment",
        "tags": "wallet, MagSafe, iPhone",
        "rating": 4.6,
        "in_stock": True,
        "related_products": "1003"
    },
    {
        "product_id": 1006,
        "product_name": "Beats Solo 3 Wireless",
        "category": "Headphones",
        "brand": "Apple",
        "price": 199.99,
        "description": "Wireless on-ear headphones with long battery life",
        "features": "Bluetooth, noise isolation",
        "tags": "headphones, Beats, wireless",
        "rating": 4.4,
        "in_stock": True,
        "related_products": "1007"
    },
    {
        "product_id": 1007,
        "product_name": "AirPods Pro 2",
        "category": "Earbuds",
        "brand": "Apple",
        "price": 249.99,
        "description": "Premium wireless earbuds with active noise cancellation",
        "features": "ANC, spatial audio",
        "tags": "earbuds, AirPods, noise cancelling",
        "rating": 4.9,
        "in_stock": True,
        "related_products": "1006"
    },
    {
        "product_id": 1008,
        "product_name": "Google Pixel Buds A-Series",
        "category": "Earbuds",
        "brand": "Google",
        "price": 119.99,
        "description": "Affordable wireless earbuds with clear sound quality",
        "features": "wireless, lightweight",
        "tags": "earbuds, Google, budget",
        "rating": 4.3,
        "in_stock": True,
        "related_products": "1007"
    },
    {
        "product_id": 1009,
        "product_name": "Samsung Galaxy S24",
        "category": "Smartphones",
        "brand": "Samsung",
        "price": 799.99,
        "description": "Flagship Android phone with AI features",
        "features": "AI camera, 5G, AMOLED display",
        "tags": "phone, Samsung, flagship",
        "rating": 4.7,
        "in_stock": True,
        "related_products": "1001,1005"
    },
    {
        "product_id": 1010,
        "product_name": "iPad Pro 12.9 inch",
        "category": "Tablets",
        "brand": "Apple",
        "price": 1099.00,
        "description": "High-performance tablet with M2 chip",
        "features": "M2 chip, Retina display, Apple Pencil support",
        "tags": "tablet, iPad, Apple",
        "rating": 4.8,
        "in_stock": True,
        "related_products": "1005,1007"
    }
]

# Save product catalog
product_df = pd.DataFrame(product_data)
product_df.to_csv("data/product_catalog.csv", index=False)
print("✅ Saved: data/product_catalog.csv")

# Build lookup from product_id to product_name
product_lookup = {str(row["product_id"]): row["product_name"] for row in product_data}

# --- Orders Data (10 orders) ---
raw_order_data = [
    {"order_id": "ORD12345", "user_id": "USER9876", "product_ids": "1001", "order_date": "2025-03-15", "status": "Pending", "shipping_info": "", "expected_delivery": "", "return_policy": ""},
    {"order_id": "ORD12346", "user_id": "USER9877", "product_ids": "1002,1004", "order_date": "2025-03-10", "status": "Shipped", "shipping_info": "FedEx 9400100000000001234567", "expected_delivery": "2025-03-20", "return_policy": "30 days from delivery date"},
    {"order_id": "ORD12347", "user_id": "USER9878", "product_ids": "1003", "order_date": "2025-03-05", "status": "Delivered", "shipping_info": "Delivered on 2025-03-08", "expected_delivery": "2025-03-08", "return_policy": "Return within 14 days of delivery"},
    {"order_id": "ORD12348", "user_id": "USER9879", "product_ids": "1005", "order_date": "2025-03-01", "status": "Processing", "shipping_info": "", "expected_delivery": "", "return_policy": ""},
    {"order_id": "ORD12349", "user_id": "USER9880", "product_ids": "1007,1009", "order_date": "2025-02-28", "status": "Delivered", "shipping_info": "Delivered on 2025-03-03", "expected_delivery": "2025-03-03", "return_policy": "30 days from delivery date"},
    {"order_id": "ORD12350", "user_id": "USER9881", "product_ids": "1008", "order_date": "2025-02-25", "status": "Shipped", "shipping_info": "UPS Z123456789", "expected_delivery": "2025-03-01", "return_policy": "Return within 14 days of delivery"},
    {"order_id": "ORD12351", "user_id": "USER9882", "product_ids": "1006", "order_date": "2025-02-20", "status": "Delivered", "shipping_info": "Delivered on 2025-02-25", "expected_delivery": "2025-02-25", "return_policy": "30 days from delivery date"},
    {"order_id": "ORD12352", "user_id": "USER9883", "product_ids": "1004,1005", "order_date": "2025-02-18", "status": "Delivered", "shipping_info": "Delivered on 2025-02-22", "expected_delivery": "2025-02-22", "return_policy": "30 days from delivery date"},
    {"order_id": "ORD12353", "user_id": "USER9884", "product_ids": "1001", "order_date": "2025-02-10", "status": "Cancelled", "shipping_info": "Order cancelled by user", "expected_delivery": "", "return_policy": ""},
    {"order_id": "ORD12354", "user_id": "USER9885", "product_ids": "1009", "order_date": "2025-02-05", "status": "Delivered", "shipping_info": "Delivered on 2025-02-09", "expected_delivery": "2025-02-09", "return_policy": "30 days from delivery date"}
]

# Add product_name based on first product_id in product_ids
for order in raw_order_data:
    first_product_id = order["product_ids"].split(",")[0].strip()
    order["product_name"] = product_lookup.get(first_product_id, "Unknown Product")

# Save orders
order_df = pd.DataFrame(raw_order_data)
order_df.to_csv("data/orders.csv", index=False)
print("✅ Saved: data/orders.csv")
