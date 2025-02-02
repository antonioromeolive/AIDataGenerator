import csv
import random
from datetime import datetime, timedelta

# -----------------------------
# Configuration and Data Setup
# -----------------------------

NUM_SALES_RECORDS = 10000  # Total number of sales records to generate

# Define categories with seasonal parameters (if any)
categories = [
    {"id": 1, "name": "Electronics", "seasonal_months": [11, 12], "seasonal_multiplier": 2.0},
    {"id": 2, "name": "Clothing", "seasonal_months": [], "seasonal_multiplier": 1.0},
    {"id": 3, "name": "Home Appliances", "seasonal_months": [], "seasonal_multiplier": 1.0},
    {"id": 4, "name": "Books", "seasonal_months": [12], "seasonal_multiplier": 1.5},
    {"id": 5, "name": "Toys", "seasonal_months": [12], "seasonal_multiplier": 2.0},
    {"id": 6, "name": "Groceries", "seasonal_months": [], "seasonal_multiplier": 1.0},
    {"id": 7, "name": "Sports", "seasonal_months": [4, 5, 6, 7], "seasonal_multiplier": 1.3},
    {"id": 8, "name": "Beauty", "seasonal_months": [], "seasonal_multiplier": 1.0},
    {"id": 9, "name": "Furniture", "seasonal_months": [], "seasonal_multiplier": 1.0},
    {"id": 10, "name": "Automotive", "seasonal_months": [], "seasonal_multiplier": 1.0},
]

# Define products for each category with realistic price ranges.
# (Each category gets five products; later one product in each category is boosted as a “top seller”.)
product_definitions = {
    "Electronics": [
        {"name": "Smartphone", "min_price": 300, "max_price": 1000},
        {"name": "Laptop", "min_price": 500, "max_price": 2000},
        {"name": "Tablet", "min_price": 150, "max_price": 800},
        {"name": "Smartwatch", "min_price": 100, "max_price": 400},
        {"name": "Headphones", "min_price": 50, "max_price": 300},
    ],
    "Clothing": [
        {"name": "T-Shirt", "min_price": 10, "max_price": 50},
        {"name": "Jeans", "min_price": 20, "max_price": 100},
        {"name": "Jacket", "min_price": 30, "max_price": 200},
        {"name": "Dress", "min_price": 20, "max_price": 150},
        {"name": "Sneakers", "min_price": 30, "max_price": 150},
    ],
    "Home Appliances": [
        {"name": "Refrigerator", "min_price": 300, "max_price": 1500},
        {"name": "Microwave", "min_price": 50, "max_price": 300},
        {"name": "Washing Machine", "min_price": 200, "max_price": 1000},
        {"name": "Air Conditioner", "min_price": 200, "max_price": 1200},
        {"name": "Vacuum Cleaner", "min_price": 30, "max_price": 500},
    ],
    "Books": [
        {"name": "Fiction Novel", "min_price": 5, "max_price": 20},
        {"name": "Non-fiction", "min_price": 10, "max_price": 30},
        {"name": "Children's Book", "min_price": 5, "max_price": 15},
        {"name": "Textbook", "min_price": 30, "max_price": 150},
        {"name": "Comic Book", "min_price": 3, "max_price": 10},
    ],
    "Toys": [
        {"name": "Action Figure", "min_price": 10, "max_price": 50},
        {"name": "Puzzle", "min_price": 5, "max_price": 20},
        {"name": "Board Game", "min_price": 15, "max_price": 60},
        {"name": "Lego Set", "min_price": 20, "max_price": 100},
        {"name": "Doll", "min_price": 10, "max_price": 50},
    ],
    "Groceries": [
        {"name": "Milk", "min_price": 1, "max_price": 3},
        {"name": "Bread", "min_price": 1, "max_price": 5},
        {"name": "Eggs", "min_price": 2, "max_price": 6},
        {"name": "Cheese", "min_price": 3, "max_price": 10},
        {"name": "Fruit Basket", "min_price": 10, "max_price": 30},
    ],
    "Sports": [
        {"name": "Football", "min_price": 10, "max_price": 40},
        {"name": "Basketball", "min_price": 10, "max_price": 40},
        {"name": "Tennis Racket", "min_price": 30, "max_price": 200},
        {"name": "Yoga Mat", "min_price": 10, "max_price": 50},
        {"name": "Running Shoes", "min_price": 40, "max_price": 150},
    ],
    "Beauty": [
        {"name": "Lipstick", "min_price": 5, "max_price": 30},
        {"name": "Perfume", "min_price": 20, "max_price": 100},
        {"name": "Skincare Set", "min_price": 20, "max_price": 150},
        {"name": "Hair Dryer", "min_price": 15, "max_price": 100},
        {"name": "Nail Polish", "min_price": 3, "max_price": 15},
    ],
    "Furniture": [
        {"name": "Sofa", "min_price": 200, "max_price": 2000},
        {"name": "Dining Table", "min_price": 150, "max_price": 1000},
        {"name": "Chair", "min_price": 50, "max_price": 300},
        {"name": "Bed", "min_price": 200, "max_price": 1500},
        {"name": "Desk", "min_price": 100, "max_price": 600},
    ],
    "Automotive": [
        {"name": "Car Tire", "min_price": 50, "max_price": 200},
        {"name": "Engine Oil", "min_price": 20, "max_price": 50},
        {"name": "Car Battery", "min_price": 50, "max_price": 150},
        {"name": "Wiper Blades", "min_price": 10, "max_price": 30},
        {"name": "Car Wax", "min_price": 5, "max_price": 20},
    ],
}

# Define a simple list of major cities with their details.
cities = [
    {"city": "New York", "state": "NY", "country": "USA", "continent": "North America"},
    {"city": "Los Angeles", "state": "CA", "country": "USA", "continent": "North America"},
    {"city": "Chicago", "state": "IL", "country": "USA", "continent": "North America"},
    {"city": "Houston", "state": "TX", "country": "USA", "continent": "North America"},
    {"city": "London", "state": "", "country": "UK", "continent": "Europe"},
    {"city": "Manchester", "state": "", "country": "UK", "continent": "Europe"},
    {"city": "Tokyo", "state": "", "country": "Japan", "continent": "Asia"},
    {"city": "Osaka", "state": "", "country": "Japan", "continent": "Asia"},
    {"city": "Berlin", "state": "", "country": "Germany", "continent": "Europe"},
    {"city": "Munich", "state": "", "country": "Germany", "continent": "Europe"},
    {"city": "Paris", "state": "", "country": "France", "continent": "Europe"},
    {"city": "Lyon", "state": "", "country": "France", "continent": "Europe"},
    {"city": "Mumbai", "state": "", "country": "India", "continent": "Asia"},
    {"city": "Delhi", "state": "", "country": "India", "continent": "Asia"},
    {"city": "Beijing", "state": "", "country": "China", "continent": "Asia"},
    {"city": "Shanghai", "state": "", "country": "China", "continent": "Asia"},
    {"city": "Sydney", "state": "", "country": "Australia", "continent": "Oceania"},
    {"city": "Melbourne", "state": "", "country": "Australia", "continent": "Oceania"},
    {"city": "Moscow", "state": "", "country": "Russia", "continent": "Europe/Asia"},
    {"city": "Saint Petersburg", "state": "", "country": "Russia", "continent": "Europe/Asia"},
    {"city": "Toronto", "state": "", "country": "Canada", "continent": "North America"},
    {"city": "Vancouver", "state": "", "country": "Canada", "continent": "North America"},
    {"city": "São Paulo", "state": "", "country": "Brazil", "continent": "South America"},
    {"city": "Rio de Janeiro", "state": "", "country": "Brazil", "continent": "South America"},
    {"city": "Seoul", "state": "", "country": "South Korea", "continent": "Asia"},
    {"city": "Busan", "state": "", "country": "South Korea", "continent": "Asia"},
    {"city": "Cairo", "state": "", "country": "Egypt", "continent": "Africa"},
    {"city": "Johannesburg", "state": "", "country": "South Africa", "continent": "Africa"},
    {"city": "Istanbul", "state": "", "country": "Turkey", "continent": "Europe/Asia"},
    {"city": "Dubai", "state": "", "country": "UAE", "continent": "Asia"},
    {"city": "Singapore", "state": "", "country": "Singapore", "continent": "Asia"},
]

# Define a GDP mapping for countries (this will weight the chance of a sale happening at that store)
GDP_DICT = {
    "USA": 20,
    "UK": 5,
    "Japan": 5,
    "Germany": 5,
    "France": 4,
    "India": 10,
    "China": 15,
    "Australia": 4,
    "Russia": 3,
    "Canada": 4,
    "Brazil": 3,
    "South Korea": 4,
    "Egypt": 1,
    "South Africa": 1,
    "Turkey": 2,
    "UAE": 2,
    "Singapore": 3,
}

# List of promotional campaign names
campaign_names = [
    "10% off Black Friday",
    "Summer Sale",
    "Winter Clearance",
    "Holiday Special",
    "Spring Discount",
]

# -----------------------------
# Helper Functions
# -----------------------------

def random_date(start, end):
    """Return a random datetime between start and end."""
    delta = end - start
    int_delta = int(delta.total_seconds())
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)

def generate_products(categories, product_definitions):
    """
    Build a list of product records. Each record is a dict with:
    product_id, product_name, category_id, category, seasonal_months,
    seasonal_multiplier, min_price, max_price, popularity.
    """
    products = []
    prod_id = 1
    for cat in categories:
        cat_name = cat["name"]
        if cat_name not in product_definitions:
            continue
        # Copy list so we can later boost one as a top seller
        prod_list = product_definitions[cat_name][:]
        # First assign a base popularity weight (random between 0.5 and 1.5)
        for p in prod_list:
            p["popularity"] = random.uniform(0.5, 1.5)
        # Randomly choose one product in this category and boost its popularity to simulate a top seller
        top_seller = random.choice(prod_list)
        top_seller["popularity"] *= 2

        for p in prod_list:
            product_record = {
                "product_id": prod_id,
                "product_name": p["name"],
                "category_id": cat["id"],
                "category": cat_name,
                "seasonal_months": cat["seasonal_months"],
                "seasonal_multiplier": cat["seasonal_multiplier"],
                "min_price": p["min_price"],
                "max_price": p["max_price"],
                "popularity": p["popularity"],
            }
            products.append(product_record)
            prod_id += 1
    return products

def generate_stores(num_stores, cities):
    """
    Generate a list of unique store records. Each record is a dict with:
    store_name, city, state, country, continent.
    Store names are created by combining a random adjective and noun.
    """
    adjectives = ["Global", "Urban", "Modern", "Elite", "Prime", "Sunrise", "Aurora",
                  "Epic", "Grand", "Metro", "Infinity", "Pioneer", "Cosmic", "Royal", "Dynamic"]
    nouns = ["Mart", "Store", "Outlet", "Emporium", "Depot", "Shop", "Corner", "Bazaar", "Market", "Express"]

    stores = []
    used_names = set()

    while len(stores) < num_stores:
        name = f"{random.choice(adjectives)} {random.choice(nouns)}"
        # Ensure the store name is unique; if not, add a random number
        if name in used_names:
            name = f"{name} {random.randint(1,99)}"
        used_names.add(name)
        # Randomly assign a city from the list (cities can repeat)
        city_info = random.choice(cities)
        store_record = {
            "store_name": name,
            "city": city_info["city"],
            "state": city_info["state"],
            "country": city_info["country"],
            "continent": city_info["continent"],
        }
        stores.append(store_record)
    return stores

# -----------------------------
# Main Generation Script
# -----------------------------

def main():
    # Generate product and store records
    products = generate_products(categories, product_definitions)
    stores = generate_stores(45, cities)  # 45 unique stores

    # Write categories_O3MH.csv
    with open("categories_O3MH.csv", mode="w", newline="") as cat_file:
        writer = csv.writer(cat_file)
        writer.writerow(["category_id", "category_name", "seasonal_months", "seasonal_multiplier"])
        for cat in categories:
            months_str = ",".join(map(str, cat["seasonal_months"])) if cat["seasonal_months"] else ""
            writer.writerow([cat["id"], cat["name"], months_str, cat["seasonal_multiplier"]])

    # Write products_O3MH.csv
    with open("products_O3MH.csv", mode="w", newline="") as prod_file:
        writer = csv.writer(prod_file)
        writer.writerow(["product_id", "product_name", "category_id", "category", "min_price", "max_price", "popularity"])
        for prod in products:
            writer.writerow([prod["product_id"],
                             prod["product_name"],
                             prod["category_id"],
                             prod["category"],
                             prod["min_price"],
                             prod["max_price"],
                             round(prod["popularity"], 2)])

    # Write stores_O3MH.csv
    with open("stores_O3MH.csv", mode="w", newline="") as store_file:
        writer = csv.writer(store_file)
        writer.writerow(["store_name", "city", "state", "country", "continent"])
        for store in stores:
            writer.writerow([store["store_name"],
                             store["city"],
                             store["state"],
                             store["country"],
                             store["continent"]])

    # Prepare to generate sales data
    sales_start_date = datetime(2024, 1, 1, 0, 0, 0)
    sales_end_date = datetime(2024, 12, 31, 23, 59, 59)
    
    # Pre-calculate store weights based on country GDP
    store_weights = []
    for store in stores:
        weight = GDP_DICT.get(store["country"], 1)
        store_weights.append(weight)

    # Open sales_data_O3MH.csv for writing
    with open("sales_data_O3MH.csv", mode="w", newline="") as sales_file:
        writer = csv.writer(sales_file)
        writer.writerow(["date", "time", "product_name", "unit_price", "quantity", "revenue", "store_name", "campaign"])

        # Generate each sales record
        for i in range(1, NUM_SALES_RECORDS + 1):
            # Choose a random sale datetime within 2024
            sale_dt = random_date(sales_start_date, sales_end_date)
            sale_date_str = sale_dt.strftime("%Y-%m-%d")
            sale_time_str = sale_dt.strftime("%H:%M:%S")
            month = sale_dt.month

            # Determine effective weights for products based on base popularity and seasonal boost
            prod_weights = []
            for prod in products:
                multiplier = prod["seasonal_multiplier"] if month in prod["seasonal_months"] else 1.0
                prod_weights.append(prod["popularity"] * multiplier)
            chosen_product = random.choices(products, weights=prod_weights, k=1)[0]

            # Determine unit price for the chosen product (round to 2 decimals)
            unit_price = round(random.uniform(chosen_product["min_price"], chosen_product["max_price"]), 2)

            # Choose quantity (for Groceries, allow a larger purchase)
            if chosen_product["category"] == "Groceries":
                quantity = random.randint(1, 10)
            else:
                quantity = random.randint(1, 3)

            revenue = round(unit_price * quantity, 2)

            # Select a store weighted by the GDP of its country
            chosen_store = random.choices(stores, weights=store_weights, k=1)[0]

            # Decide whether to include a promotional campaign.
            # (For November/December use a higher probability.)
            if month in [11, 12]:
                campaign_prob = 0.15
            else:
                campaign_prob = 0.05
            campaign = random.choice(campaign_names) if random.random() < campaign_prob else ""

            # Write the sales record row
            writer.writerow([sale_date_str,
                             sale_time_str,
                             chosen_product["product_name"],
                             unit_price,
                             quantity,
                             revenue,
                             chosen_store["store_name"],
                             campaign])
            
            # Print progress every 1000 records
            if i % 1000 == 0:
                print(f"{i} sales records generated...")

    # -----------------------------
    # Summary of Generation
    # -----------------------------
    print("\n--- Generation Complete ---")
    print(f"Total Categories: {len(categories)}")
    print(f"Total Products: {len(products)}")
    print(f"Total Stores: {len(stores)}")
    print(f"Total Sales Records: {NUM_SALES_RECORDS}")

if __name__ == "__main__":
    main()
    print("\ndata generation by DataGeneration-o3-mini-high.py")
