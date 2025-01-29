""" MIT License - Copyright (c) 2025 Antonio Romeo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import csv
import random
import datetime
import math

# -------------------------
# CONFIGURATION
# -------------------------

NUM_SALES_RECORDS = 50000  # Total sales records to generate
PROGRESS_INTERVAL = 1000   # Print progress every X records

# Define a list of categories
# (In a more realistic setup, these could be read from a DB or a more extensive data source.)
CATEGORIES = [
    'Electronics',
    'Home & Kitchen',
    'Clothing',
    'Sports & Outdoors',
    'Beauty & Personal Care',
    'Books',
    'Toys & Games',
    'Automotive',
    'Grocery',
    'Office Products',
]

# Example products for each category (top sellers vs. bottom sellers will be handled with weighting)
# Each product has a (min_price, max_price) range and a popularity rank or weighting.
CATEGORY_PRODUCTS = {
    'Electronics': [
        ("Smartphone", (300, 1200)),
        ("Laptop", (500, 2000)),
        ("Wireless Headphones", (50, 300)),
        ("Smartwatch", (80, 400)),
        ("Gaming Console", (200, 600)),
    ],
    'Home & Kitchen': [
        ("Blender", (20, 100)),
        ("Microwave Oven", (50, 200)),
        ("Vacuum Cleaner", (60, 300)),
        ("Air Purifier", (50, 400)),
        ("Coffee Maker", (20, 200)),
    ],
    'Clothing': [
        ("T-Shirt", (5, 30)),
        ("Jeans", (20, 80)),
        ("Jacket", (40, 200)),
        ("Sneakers", (30, 150)),
        ("Dress", (25, 150)),
    ],
    'Sports & Outdoors': [
        ("Running Shoes", (40, 120)),
        ("Yoga Mat", (15, 60)),
        ("Tennis Racket", (50, 250)),
        ("Football", (10, 60)),
        ("Camping Tent", (50, 300)),
    ],
    'Beauty & Personal Care': [
        ("Shampoo", (5, 20)),
        ("Facial Cleanser", (5, 30)),
        ("Perfume", (20, 150)),
        ("Makeup Palette", (10, 80)),
        ("Electric Toothbrush", (30, 150)),
    ],
    'Books': [
        ("Mystery Novel", (5, 30)),
        ("Science Fiction Novel", (5, 35)),
        ("Cookbook", (10, 40)),
        ("Self-Help Book", (5, 25)),
        ("Biography", (8, 45)),
    ],
    'Toys & Games': [
        ("Board Game", (15, 70)),
        ("Action Figure", (10, 40)),
        ("Doll", (8, 40)),
        ("Building Blocks", (15, 60)),
        ("Card Game", (5, 30)),
    ],
    'Automotive': [
        ("Car Air Freshener", (2, 10)),
        ("Motor Oil", (10, 40)),
        ("Car Battery", (40, 120)),
        ("Windshield Wipers", (5, 25)),
        ("Car Tires", (50, 200)),
    ],
    'Grocery': [
        ("Milk", (1, 3)),
        ("Bread", (1, 4)),
        ("Organic Eggs", (2, 6)),
        ("Cheese", (2, 10)),
        ("Cereal", (2, 6)),
    ],
    'Office Products': [
        ("Printer Paper", (3, 10)),
        ("Ballpoint Pens", (1, 8)),
        ("Notebook", (2, 10)),
        ("Stapler", (4, 15)),
        ("Desk Organizer", (5, 25)),
    ],
}

# Hardcode some seasonality impacts (month-based) for categories.
# A simple approach: each category gets a dictionary mapping month -> demand multiplier
# For instance, Electronics might be in higher demand around November/December (holiday season)
SEASONALITY = {
    'Electronics': {
        11: 1.2,  # Black Friday boost
        12: 1.4,  # Holiday season
    },
    'Home & Kitchen': {
        5: 1.2,   # Summer home improvements
        6: 1.2,
    },
    'Clothing': {
        3: 1.1,   # Spring collections
        8: 1.2,   # Back-to-school/fall
        12: 1.3,  # Holiday/winter
    },
    'Sports & Outdoors': {
        4: 1.3,   # Spring sports
        5: 1.5,   # Summer sports
        6: 1.5,
        7: 1.4,
    },
    'Beauty & Personal Care': {
        4: 1.1,
        5: 1.2,
        12: 1.3,
    },
    'Books': {
        12: 1.2,  # Gifts
    },
    'Toys & Games': {
        11: 1.3,
        12: 1.6,
    },
    'Automotive': {
        7: 1.3,   # Summer travel
        8: 1.2,
    },
    'Grocery': {
        11: 1.1,  # Holidays
        12: 1.3,
    },
    'Office Products': {
        8: 1.2,   # Back to school
        9: 1.1,
    },
}

# Probability of a sale having a sales campaign
# We'll incorporate random choice of campaign names
CAMPAIGN_NAMES = [
    "10% off Black Friday",
    "Summer Sale",
    "Buy One Get One",
    "Holiday Discount",
    "Clearance Sale"
]
CAMPAIGN_PROBABILITY = 0.1  # 10% chance to have a campaign in each sale

# Weighted GDP approach for store location
# We'll keep a simple list of countries with approximate GDP weighting factors (not real data)
COUNTRIES_GDP = {
    "USA": 21.4,
    "China": 14.3,
    "Japan": 5.0,
    "Germany": 3.8,
    "India": 2.9,
    "UK": 2.7,
    "France": 2.6,
    "Italy": 2.0,
    "Canada": 1.6,
    "South Korea": 1.6,
    "Russia": 1.5,
    "Brazil": 1.4,
    "Australia": 1.4,
    "Spain": 1.3,
    "Mexico": 1.2,
}

# We also define a small helper for continent lookup
COUNTRY_CONTINENT = {
    "USA": "North America",
    "China": "Asia",
    "Japan": "Asia",
    "Germany": "Europe",
    "India": "Asia",
    "UK": "Europe",
    "France": "Europe",
    "Italy": "Europe",
    "Canada": "North America",
    "South Korea": "Asia",
    "Russia": "Europe",
    "Brazil": "South America",
    "Australia": "Australia",
    "Spain": "Europe",
    "Mexico": "North America",
}

# We want 45 stores across major cities worldwide.
# We'll randomly pick from a pool of city data for each country.
CITY_OPTIONS = {
    "USA": [
        ("New York", "NY"),
        ("Los Angeles", "CA"),
        ("Chicago", "IL"),
        ("Houston", "TX"),
        ("Phoenix", "AZ"),
    ],
    "China": [
        ("Beijing", "Beijing"),
        ("Shanghai", "Shanghai"),
        ("Guangzhou", "Guangdong"),
        ("Shenzhen", "Guangdong"),
        ("Chengdu", "Sichuan"),
    ],
    "Japan": [
        ("Tokyo", "Tokyo"),
        ("Osaka", "Osaka"),
        ("Nagoya", "Aichi"),
        ("Fukuoka", "Fukuoka"),
    ],
    "Germany": [
        ("Berlin", "Berlin"),
        ("Munich", "Bavaria"),
        ("Frankfurt", "Hesse"),
    ],
    "India": [
        ("Mumbai", "Maharashtra"),
        ("New Delhi", "Delhi"),
        ("Bengaluru", "Karnataka"),
        ("Chennai", "Tamil Nadu"),
    ],
    "UK": [
        ("London", "England"),
        ("Manchester", "England"),
        ("Edinburgh", "Scotland"),
    ],
    "France": [
        ("Paris", "Ile-de-France"),
        ("Lyon", "Auvergne-Rhone-Alpes"),
        ("Marseille", "Provence-Alpes-Cote d'Azur"),
    ],
    "Italy": [
        ("Rome", "Lazio"),
        ("Milan", "Lombardy"),
        ("Naples", "Campania"),
    ],
    "Canada": [
        ("Toronto", "ON"),
        ("Vancouver", "BC"),
        ("Montreal", "QC"),
    ],
    "South Korea": [
        ("Seoul", "Seoul"),
        ("Busan", "Busan"),
        ("Incheon", "Incheon"),
    ],
    "Russia": [
        ("Moscow", "Moscow"),
        ("Saint Petersburg", "Northwestern"),
    ],
    "Brazil": [
        ("Sao Paulo", "Sao Paulo"),
        ("Rio de Janeiro", "Rio de Janeiro"),
        ("Brasilia", "Federal District"),
    ],
    "Australia": [
        ("Sydney", "NSW"),
        ("Melbourne", "VIC"),
        ("Brisbane", "QLD"),
    ],
    "Spain": [
        ("Madrid", "Community of Madrid"),
        ("Barcelona", "Catalonia"),
        ("Valencia", "Valencia"),
    ],
    "Mexico": [
        ("Mexico City", "Distrito Federal"),
        ("Guadalajara", "Jalisco"),
        ("Monterrey", "Nuevo Leon"),
    ],
}


def generate_stores(num_stores=45):
    # We create a list of (country, weighting) from the GDP dict
    # Then we'll do a weighted selection for countries, pick random city from that country.
    all_countries = list(COUNTRIES_GDP.keys())
    total_gdp = sum(COUNTRIES_GDP.values())
    # Weighted distribution for selecting countries

    stores = []
    used_store_names = set()

    for _ in range(num_stores):
        # Weighted random pick of country
        r = random.uniform(0, total_gdp)
        cumulative = 0
        for country, gdp_val in COUNTRIES_GDP.items():
            cumulative += gdp_val
            if r <= cumulative:
                chosen_country = country
                break
        # pick random city
        if chosen_country in CITY_OPTIONS:
            city, state = random.choice(CITY_OPTIONS[chosen_country])
        else:
            # fallback
            city, state = ("Unknown City", "Unknown State")
        continent = COUNTRY_CONTINENT.get(chosen_country, "Unknown Continent")

        # Make a store name by combining city with a random number
        # ensure uniqueness
        for attempt in range(1000):
            store_name = f"{city} Store #{random.randint(1,9999)}"
            if store_name not in used_store_names:
                used_store_names.add(store_name)
                break
        stores.append((store_name, city, state, chosen_country, continent))

    return stores


def expand_products_and_categories():
    # Flatten out the product list for each category
    products = []
    cat_map = {}
    product_id = 1

    for cat_idx, category in enumerate(CATEGORIES, start=1):
        cat_map[cat_idx] = category
        product_list = CATEGORY_PRODUCTS.get(category, [])
        for (product_name, price_range) in product_list:
            products.append((product_id, product_name, cat_idx, price_range[0], price_range[1]))
            product_id += 1

    return cat_map, products


def seasonality_factor(category, month):
    if category in SEASONALITY:
        if month in SEASONALITY[category]:
            return SEASONALITY[category][month]
    return 1.0


def main():
    random.seed(42)  # For reproducibility if desired

    # Generate stores
    stores = generate_stores(45)

    # Expand categories and products
    cat_map, products = expand_products_and_categories()

    # Save categories to categories_O1.csv
    with open('categories_O1.csv', 'w', newline='', encoding='utf-8') as f_cat:
        writer = csv.writer(f_cat)
        writer.writerow(["category_id", "category_name"])
        for cat_id, cat_name in cat_map.items():
            writer.writerow([cat_id, cat_name])

    # Save products to products_O1.csv (product_id, product_name, category_id, min_price, max_price)
    with open('products_O1.csv', 'w', newline='', encoding='utf-8') as f_prod:
        writer = csv.writer(f_prod)
        writer.writerow(["product_id", "product_name", "category_id", "min_price", "max_price"])
        for p in products:
            writer.writerow(p)

    # Save stores to stores_O1.csv
    # store name, city, state, country, continent
    with open('stores_O1.csv', 'w', newline='', encoding='utf-8') as f_stores:
        writer = csv.writer(f_stores)
        writer.writerow(["store_name", "city", "state", "country", "continent"])
        for store in stores:
            writer.writerow(store)

    # We'll build a product popularity weighting
    # Let's say half of the products are top sellers with a higher probability
    # We'll simply create a distribution by assigning random popularity scores.

    product_popularity = {}
    for pid, pname, cat_id, pmin, pmax in products:
        # random popularity score 1-100, with some distribution
        popularity_score = random.randint(1, 100)
        product_popularity[pid] = popularity_score

    # We'll also build a weighting for each store based on the country GDP so that
    # stores in higher GDP countries appear more often in the dataset.
    store_gdp_weights = []
    for store in stores:
        # store is (store_name, city, state, country, continent)
        country = store[3]
        gdp_val = COUNTRIES_GDP.get(country, 1.0)
        store_gdp_weights.append(gdp_val)

    total_store_weight = sum(store_gdp_weights)

    # We'll generate the sales_data_O1.csv now
    # date, time, product name, unit price, quantity, revenue, store name, optional sales campaign

    # We'll pick random dates in a certain range, e.g., 1 year
    # from Jan 1, 2024 to Dec 31, 2024.
    start_date = datetime.date(2024, 1, 1)
    end_date = datetime.date(2024, 12, 31)
    delta_days = (end_date - start_date).days + 1

    # Pre-generate date list for efficiency?
    # or just pick random day offset

    with open('sales_data_O1.csv', 'w', newline='', encoding='utf-8') as f_sales:
        writer = csv.writer(f_sales)
        writer.writerow(["date", "time", "product_name", "unit_price", "quantity", "revenue", "store_name", "campaign"])

        for i in range(1, NUM_SALES_RECORDS + 1):
            # pick a store with weighted probability
            r = random.uniform(0, total_store_weight)
            cumulative = 0.0
            chosen_store_index = 0
            for idx, weight in enumerate(store_gdp_weights):
                cumulative += weight
                if r <= cumulative:
                    chosen_store_index = idx
                    break
            chosen_store = stores[chosen_store_index]

            # pick a product with popularity weighting
            # sum of popularity
            total_popularity = sum(product_popularity.values())
            r2 = random.uniform(0, total_popularity)
            cum2 = 0.0
            chosen_product = None
            for p in products:
                pid, pname, cat_id, pmin, pmax = p
                cum2 += product_popularity[pid]
                if r2 <= cum2:
                    chosen_product = p
                    break

            if not chosen_product:
                chosen_product = random.choice(products)
            pid, pname, cat_id, pmin, pmax = chosen_product

            # figure out date/time
            day_offset = random.randint(0, delta_days - 1)
            sale_date = start_date + datetime.timedelta(days=day_offset)
            sale_time = datetime.time(
                hour=random.randint(0, 23),
                minute=random.randint(0, 59),
                second=random.randint(0, 59)
            )

            # incorporate seasonality
            month = sale_date.month
            cat_name = cat_map[cat_id]
            s_factor = seasonality_factor(cat_name, month)

            # pick quantity in a realistic manner
            # base quantity 1-3
            # plus factor from seasonality
            base_qty = random.randint(1, 3)
            # scale up occasionally
            if random.random() < 0.05:
                base_qty += random.randint(1, 5)
            quantity = int(round(base_qty * s_factor))
            if quantity < 1:
                quantity = 1

            # pick a random unit price in [pmin, pmax]
            unit_price = round(random.uniform(pmin, pmax), 2)

            # campaign?
            campaign = ""
            if random.random() < CAMPAIGN_PROBABILITY:
                campaign = random.choice(CAMPAIGN_NAMES)

            # compute revenue
            revenue = round(unit_price * quantity, 2)

            # write the row
            writer.writerow([
                sale_date.isoformat(),
                sale_time.strftime("%H:%M:%S"),
                pname,
                unit_price,
                quantity,
                revenue,
                chosen_store[0],
                campaign,
            ])

            # progress
            if i % PROGRESS_INTERVAL == 0:
                print(f"Generated {i} sales records...")

    # Summarize
    print("Generation complete.")
    print(f"Total categories: {len(CATEGORIES)}")
    total_products = len(products)
    print(f"Total products: {total_products}")
    total_stores = len(stores)
    print(f"Total stores: {total_stores}")
    print(f"Total sales records: {NUM_SALES_RECORDS}")
    print("\ndata generation by DataGeneration-o1.py")
if __name__ == "__main__":
    main()
