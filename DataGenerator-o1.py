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
#!/usr/bin/env python3
import csv
import random
import datetime
import math

# CONFIGURATIONS
NUM_SALES_RECORDS = 10000  # Adjust as desired.

# Category definitions (category name, seasonality factor, possible discount surges, etc.)
CATEGORIES = [
    {
        'name': 'Electronics',
        'seasonality_peaks': [(11, 12)],  # Example: big surge in November, December
        'price_range': (50, 1000),  # Minimum to maximum price
    },
    {
        'name': 'Clothing',
        'seasonality_peaks': [(3, 3)],  # Spring collections in March
        'price_range': (10, 200),
    },
    {
        'name': 'Home Appliances',
        'seasonality_peaks': [(5, 8)],  # Summer months for fans, etc.
        'price_range': (30, 800),
    },
    {
        'name': 'Books',
        'seasonality_peaks': [(8, 9)],  # Back-to-school season
        'price_range': (5, 80),
    },
    {
        'name': 'Toys',
        'seasonality_peaks': [(11, 12)],  # Holiday surge
        'price_range': (5, 150),
    },
    {
        'name': 'Groceries',
        'seasonality_peaks': [(11, 11)],  # Thanksgiving in some regions
        'price_range': (2, 20),
    },
]

# Dummy categories if we want more variety, just replicate or alter data as needed.

# We will create multiple products for each category.
PRODUCTS_PER_CATEGORY = {
    'Electronics': [
        ('Smartphone', 0.7),
        ('Laptop', 0.6),
        ('Headphones', 0.4),
        ('Smart TV', 0.3),
        ('Gaming Console', 0.35),
        ('Tablet', 0.55),
    ],
    'Clothing': [
        ('T-Shirt', 0.7),
        ('Jeans', 0.6),
        ('Jacket', 0.4),
        ('Sneakers', 0.65),
        ('Dress', 0.55),
        ('Underwear', 0.3),
    ],
    'Home Appliances': [
        ('Refrigerator', 0.25),
        ('Microwave', 0.4),
        ('Blender', 0.35),
        ('Air Conditioner', 0.25),
        ('Dishwasher', 0.2),
    ],
    'Books': [
        ('Novel', 0.6),
        ('Cookbook', 0.4),
        ('Textbook', 0.3),
        ('Children Book', 0.4),
        ('Comic Book', 0.35),
    ],
    'Toys': [
        ('Action Figure', 0.5),
        ('Board Game', 0.45),
        ('Doll', 0.4),
        ('Puzzle', 0.3),
        ('Remote Car', 0.35),
    ],
    'Groceries': [
        ('Cereal', 0.7),
        ('Milk', 0.8),
        ('Eggs', 0.75),
        ('Bread', 0.9),
        ('Butter', 0.6),
        ('Frozen Pizza', 0.4),
    ],
}

# Weighted top sellers vs bottom sellers by popularity factor.
# popularity factor is used to adjust the likelihood of a product being chosen.
# Higher => more likely to appear.

# We create store data: 45 unique store names in major cities worldwide.
STORE_DATA = [
    ("Tech Haven NYC", "New York", "NY", "USA", "North America"),
    ("Urban Apparel LA", "Los Angeles", "CA", "USA", "North America"),
    ("Gadget World CHI", "Chicago", "IL", "USA", "North America"),
    ("Electro Zone TOR", "Toronto", "ON", "Canada", "North America"),
    ("Metro Style PAR", "Paris", "Ile-de-France", "France", "Europe"),
    ("Fashion Hub LON", "London", "England", "UK", "Europe"),
    ("Digital Plaza BER", "Berlin", "Berlin", "Germany", "Europe"),
    ("Trendy Market TOK", "Tokyo", "Tokyo", "Japan", "Asia"),
    ("Alpha Store SYD", "Sydney", "NSW", "Australia", "Oceania"),
    ("Global Retail DXB", "Dubai", "Dubai", "UAE", "Asia"),
    ("Smart Mall SHA", "Shanghai", "Shanghai", "China", "Asia"),
    ("Electronics Hub MUM", "Mumbai", "Maharashtra", "India", "Asia"),
    ("Casual Wear SAO", "Sao Paulo", "Sao Paulo", "Brazil", "South America"),
    ("Trendy Outlet MEX", "Mexico City", "CDMX", "Mexico", "North America"),
    ("Chic Boutique ROM", "Rome", "Lazio", "Italy", "Europe"),
    ("CityMart MAD", "Madrid", "Madrid", "Spain", "Europe"),
    ("StyleStop AMS", "Amsterdam", "North Holland", "Netherlands", "Europe"),
    ("Eco Goods STO", "Stockholm", "Stockholm", "Sweden", "Europe"),
    ("Modern Tech SEL", "Seoul", "Seoul", "South Korea", "Asia"),
    ("MegaMart JNB", "Johannesburg", "Gauteng", "South Africa", "Africa"),
    ("TechnoZone HKG", "Hong Kong", "-", "Hong Kong", "Asia"),
    ("Digital Haven SIN", "Singapore", "-", "Singapore", "Asia"),
    ("Urban Market BUE", "Buenos Aires", "Buenos Aires", "Argentina", "South America"),
    ("Lifestyle Store ZRH", "Zurich", "Zurich", "Switzerland", "Europe"),
    ("Elite Shop VIE", "Vienna", "Vienna", "Austria", "Europe"),
    ("SmartChoice GVA", "Geneva", "Geneva", "Switzerland", "Europe"),
    ("TrendSpot MIL", "Milan", "Lombardy", "Italy", "Europe"),
    ("ShopWorld BCN", "Barcelona", "Catalonia", "Spain", "Europe"),
    ("Bazaar BKK", "Bangkok", "Bangkok", "Thailand", "Asia"),
    ("Global Goods KUL", "Kuala Lumpur", "-", "Malaysia", "Asia"),
    ("City Emporium CAI", "Cairo", "Cairo", "Egypt", "Africa"),
    ("Pacific Retail AKL", "Auckland", "Auckland", "New Zealand", "Oceania"),
    ("Urban Basics MTL", "Montreal", "QC", "Canada", "North America"),
    ("Tech Central BRU", "Brussels", "Brussels", "Belgium", "Europe"),
    ("Innova Market LUX", "Luxembourg", "-", "Luxembourg", "Europe"),
    ("Revive Shop LIS", "Lisbon", "Lisbon", "Portugal", "Europe"),
    ("Concept Store HEL", "Helsinki", "Uusimaa", "Finland", "Europe"),
    ("Mega Deals OSL", "Oslo", "Oslo", "Norway", "Europe"),
    ("Boutique BUD", "Budapest", "Central Hungary", "Hungary", "Europe"),
    ("Tech House PRG", "Prague", "Prague", "Czech Republic", "Europe"),
    ("CityStyle DUB", "Dublin", "Leinster", "Ireland", "Europe"),
    ("Metro Depot WAW", "Warsaw", "Masovian", "Poland", "Europe"),
    ("Shop Express ATH", "Athens", "Attica", "Greece", "Europe"),
]

# If we need more or fewer, adjust the above. Exactly 45 entries are included.

# GDP weighting: we can define approximate GDP or an index for each country.
GDP_INDEX = {
    'USA': 21.4,
    'Canada': 1.6,
    'France': 2.6,
    'UK': 2.8,
    'Germany': 3.8,
    'Japan': 5.1,
    'Australia': 1.4,
    'UAE': 0.42,
    'China': 14.3,
    'India': 2.8,
    'Brazil': 1.8,
    'Mexico': 1.2,
    'Italy': 2.0,
    'Spain': 1.4,
    'Netherlands': 0.9,
    'Sweden': 0.54,
    'South Korea': 1.6,
    'South Africa': 0.35,
    'Hong Kong': 0.37,
    'Singapore': 0.37,
    'Argentina': 0.45,
    'Switzerland': 0.71,
    'Austria': 0.46,
    'Thailand': 0.52,
    'Malaysia': 0.36,
    'Egypt': 0.3,
    'New Zealand': 0.21,
    'Belgium': 0.52,
    'Luxembourg': 0.71,
    'Portugal': 0.24,
    'Finland': 0.27,
    'Norway': 0.4,
    'Hungary': 0.16,
    'Czech Republic': 0.25,
    'Ireland': 0.42,
    'Poland': 0.59,
    'Greece': 0.22,
}

# If a country is not in the dictionary, we can assume a default GDP index
DEFAULT_GDP_INDEX = 0.3

# Probability of a special campaign
CAMPAIGN_PROBABILITY = 0.05
CAMPAIGNS = [
    "10% off Black Friday",
    "Summer Sale",
    "Holiday Deal",
    "Weekend Special",
]

# HELPER FUNCTIONS

def get_random_date_time():
    # Let's generate random date between 2022-01-01 and 2023-12-31 for example.
    start_date = datetime.date(2022, 1, 1)
    end_date = datetime.date(2023, 12, 31)

    time_between = end_date - start_date
    days_between = time_between.days

    random_num = random.randint(0, days_between)
    random_date = start_date + datetime.timedelta(days=random_num)

    random_hour = random.randint(0, 23)
    random_minute = random.randint(0, 59)
    random_second = random.randint(0, 59)

    return random_date, datetime.time(random_hour, random_minute, random_second)


def get_seasonality_multiplier(category_name, month):
    """Return a factor (e.g. 1.0 means normal, 1.5 means 50% surge) based on category's seasonality."""
    for cat in CATEGORIES:
        if cat['name'] == category_name:
            for peak_start, peak_end in cat['seasonality_peaks']:
                if peak_start <= month <= peak_end:
                    return 1.5  # 50% more likely in peak
    return 1.0


def choose_store_by_gdp_weighting(stores):
    # Weighted random choice based on GDP index.
    # store: (store_name, city, state, country, continent)
    # We get the GDP weight. We'll do a cumulative distribution.

    total_weight = 0.0
    weights = []
    for s in stores:
        ctry = s[3]
        gdp_val = GDP_INDEX.get(ctry, DEFAULT_GDP_INDEX)
        weights.append(gdp_val)
        total_weight += gdp_val

    rand_val = random.random() * total_weight
    cumulative = 0.0
    for i, s in enumerate(stores):
        cumulative += weights[i]
        if rand_val < cumulative:
            return s
    return stores[-1]  # Fallback


def main():

    # 1. Write categories to categories_O1.csv
    with open('categories_O1.csv', mode='w', newline='', encoding='utf-8') as cat_file:
        writer = csv.writer(cat_file)
        writer.writerow(['category_name'])
        for c in CATEGORIES:
            writer.writerow([c['name']])

    # 2. Write products to products_O1.csv along with category
    # We'll flatten the PRODUCTS_PER_CATEGORY structure.
    products_list = []  # (product_name, category_name, popularity_factor)
    for cat, prod_tuples in PRODUCTS_PER_CATEGORY.items():
        for pt in prod_tuples:
            products_list.append((pt[0], cat, pt[1]))

    with open('products_O1.csv', mode='w', newline='', encoding='utf-8') as prod_file:
        writer = csv.writer(prod_file)
        writer.writerow(['product_name', 'category_name'])
        for p in products_list:
            writer.writerow([p[0], p[1]])

    # 3. Write store data to stores_O1.csv
    with open('stores_O1.csv', mode='w', newline='', encoding='utf-8') as store_file:
        writer = csv.writer(store_file)
        writer.writerow(['store_name', 'city', 'state', 'country', 'continent'])
        for s in STORE_DATA:
            writer.writerow(list(s))

    # Prepare popularity weighting for products.
    total_pop = sum([p[2] for p in products_list])
    # We'll create a cumulative distribution over these products.
    cumulative_pop = []
    running_sum = 0
    for p in products_list:
        running_sum += p[2]
        cumulative_pop.append((running_sum, p))

    def choose_product():
        r = random.random() * total_pop
        for cp, product in cumulative_pop:
            if r <= cp:
                return product
        return cumulative_pop[-1][1]

    # 4. Generate sales data in sales_data_O1.csv
    # Fields: date, time, product name, unit price, quantity, revenue, store name, campaign
    with open('sales_data_O1.csv', mode='w', newline='', encoding='utf-8') as sales_file:
        writer = csv.writer(sales_file)
        writer.writerow(['date', 'time', 'product_name', 'unit_price', 'quantity', 'revenue', 'store_name', 'campaign'])
        for i in range(NUM_SALES_RECORDS):
            random_date, random_time = get_random_date_time()
            # choose product
            product_name, category_name, popularity_factor = choose_product()

            # get seasonality multiplier
            multiplier = get_seasonality_multiplier(category_name, random_date.month)

            # further adjust probability but since we already decided on product, let's reflect that in quantity
            # random quantity from 1 to 5, then multiply by some factor if seasonality is high
            base_quantity = random.randint(1, 5)
            quantity = int(math.ceil(base_quantity * multiplier))

            # get price range
            cat_obj = next(c for c in CATEGORIES if c['name'] == category_name)
            min_price, max_price = cat_obj['price_range']
            unit_price = round(random.uniform(min_price, max_price), 2)

            # store
            store_record = choose_store_by_gdp_weighting(STORE_DATA)
            store_name = store_record[0]

            # campaign?
            campaign = ""
            if random.random() < CAMPAIGN_PROBABILITY:
                campaign = random.choice(CAMPAIGNS)

            # revenue
            revenue = round(unit_price * quantity, 2)

            writer.writerow([
                random_date.isoformat(),
                random_time.isoformat(timespec='seconds'),
                product_name,
                unit_price,
                quantity,
                revenue,
                store_name,
                campaign
            ])

            if (i+1) % 1000 == 0:
                print(f"Generated {i+1} sales records...")

    # Summary
    print("--- Generation Summary ---")
    print(f"Total categories: {len(CATEGORIES)}")
    print(f"Total products: {len(products_list)}")
    print(f"Total stores: {len(STORE_DATA)}")
    print(f"Total sales records generated: {NUM_SALES_RECORDS}")

if __name__ == "__main__":
    main()
