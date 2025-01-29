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
from datetime import datetime, timedelta, time

# Configuration
NUM_SALES = 10000  # Adjust this number as needed

# Categories Configuration
CATEGORIES = [
    {'id': 1, 'name': 'Electronics', 'price_range': (100, 2000)},
    {'id': 2, 'name': 'Clothing', 'price_range': (20, 150)},
    {'id': 3, 'name': 'Groceries', 'price_range': (5, 50)},
    {'id': 4, 'name': 'Home & Kitchen', 'price_range': (30, 500)},
    {'id': 5, 'name': 'Books', 'price_range': (10, 40)},
    {'id': 6, 'name': 'Sports & Outdoors', 'price_range': (50, 300)},
    {'id': 7, 'name': 'Toys & Games', 'price_range': (15, 200)},
    {'id': 8, 'name': 'Beauty', 'price_range': (10, 100)},
    {'id': 9, 'name': 'Automotive', 'price_range': (50, 1000)},
]

# Seasonality Configuration
SEASONALITY = {
    'Electronics': [11, 12],  # November-December
    'Clothing': [6, 7, 8],    # Summer months
    'Sports & Outdoors': [5, 6, 7],  # Summer
    'Toys & Games': [11, 12], # Holiday season
    'Home & Kitchen': [4, 5], # Spring cleaning
    'Beauty': [3, 4, 5],      # Spring
}

# Campaign Configuration
CAMPAIGNS = [
    {'name': '10% off Black Friday', 'discount': 0.10},
    {'name': 'Summer Sale 20%', 'discount': 0.20},
    {'name': 'Holiday Special 15%', 'discount': 0.15},
    {'name': 'Spring Clearance 25%', 'discount': 0.25},
]

# Generate Stores Data
def generate_stores():
    cities = [
        # North America
        {'city': 'New York', 'state': 'NY', 'country': 'USA', 'continent': 'North America', 'gdp_weight': 25},
        {'city': 'Los Angeles', 'state': 'CA', 'country': 'USA', 'continent': 'North America', 'gdp_weight': 25},
        # Europe
        {'city': 'London', 'state': 'England', 'country': 'UK', 'continent': 'Europe', 'gdp_weight': 6},
        {'city': 'Paris', 'state': 'Île-de-France', 'country': 'France', 'continent': 'Europe', 'gdp_weight': 5},
        # Asia
        {'city': 'Tokyo', 'state': 'Tokyo', 'country': 'Japan', 'continent': 'Asia', 'gdp_weight': 8},
        {'city': 'Beijing', 'state': 'Hebei', 'country': 'China', 'continent': 'Asia', 'gdp_weight': 20},
        # Add more cities to reach 45...
    ]
    
    stores = []
    store_names = set()
    for i in range(45):
        while True:
            city = random.choice(cities)
            store_name = f"{city['city']} Store {i+1}"
            if store_name not in store_names:
                store_names.add(store_name)
                break
        stores.append({
            'store_name': store_name,
            'city': city['city'],
            'state': city['state'],
            'country': city['country'],
            'continent': city['continent'],
            'gdp_weight': city['gdp_weight']
        })
    return stores

# Generate Products Data
def generate_products():
    products = []
    product_id = 1
    for category in CATEGORIES:
        for i in range(10):  # 10 products per category
            product = {
                'id': product_id,
                'name': f"{category['name']} Product {i+1}",
                'category_id': category['id'],
                'unit_price': round(random.uniform(*category['price_range']), 2),
                'popularity': random.choices([1, 3, 5], weights=[0.2, 0.6, 0.2])[0]
            }
            products.append(product)
            product_id += 1
    return products

# Generate Sales Data
def generate_sales(stores, products):
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)
    date_range = (end_date - start_date).days
    
    store_weights = [store['gdp_weight'] for store in stores]
    store_indices = list(range(len(stores)))
    
    with open('sales_data_DS.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['date', 'time', 'product_name', 'unit_price', 
                        'quantity', 'revenue', 'store_name', 'campaign'])
        
        for i in range(NUM_SALES):
            if i % 1000 == 0:
                print(f"Generated {i} records...")
            
            # Random date and time
            random_date = start_date + timedelta(days=random.randint(0, date_range))
            random_time = time(
                random.randint(0, 23),
                random.randint(0, 59),
                random.randint(0, 59)
            )
            
            # Select store based on GDP weights
            store_idx = random.choices(store_indices, weights=store_weights, k=1)[0]
            store = stores[store_idx]
            
            # Select product with seasonality adjustment
            product_weights = []
            month = random_date.month
            for product in products:
                category = next(cat for cat in CATEGORIES if cat['id'] == product['category_id'])
                season_boost = 2 if (category['name'] in SEASONALITY and 
                                    month in SEASONALITY[category['name']]) else 1
                product_weights.append(product['popularity'] * season_boost)
            
            product_idx = random.choices(range(len(products)), weights=product_weights, k=1)[0]
            product = products[product_idx]
            
            # Apply campaign discount
            campaign = None
            unit_price = product['unit_price']
            if random.random() < 0.1:  # 10% chance of campaign
                campaign = random.choice(CAMPAIGNS)
                unit_price = round(unit_price * (1 - campaign['discount']), 2)
            
            # Generate quantity and calculate revenue
            quantity = random.randint(1, 5)
            revenue = round(unit_price * quantity, 2)
            
            writer.writerow([
                random_date.strftime('%Y-%m-%d'),
                random_time.strftime('%H:%M:%S'),
                product['name'],
                unit_price,
                quantity,
                revenue,
                store['store_name'],
                campaign['name'] if campaign else ''
            ])

# Save supporting data files
def save_supporting_data(categories, products, stores):
    # Save categories
    with open('categories_DS.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['category_id', 'category_name'])
        writer.writeheader()
        for cat in CATEGORIES:
            writer.writerow({'category_id': cat['id'], 'category_name': cat['name']})
    
    # Save products
    with open('products_DS.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['product_id', 'product_name', 'category_id', 'unit_price'])
        writer.writeheader()
        for prod in products:
            writer.writerow({
                'product_id': prod['id'],
                'product_name': prod['name'],
                'category_id': prod['category_id'],
                'unit_price': prod['unit_price']
            })
    
    # Save stores
    with open('stores_DS.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['store_name', 'city', 'state', 'country', 'continent'])
        writer.writeheader()
        for store in stores:
            writer.writerow({
                'store_name': store['store_name'],
                'city': store['city'],
                'state': store['state'],
                'country': store['country'],
                'continent': store['continent']
            })

# Main execution
def main():
    print("Generating data...")
    
    stores = generate_stores()
    products = generate_products()
    
    generate_sales(stores, products)
    save_supporting_data(CATEGORIES, products, stores)
    
    print("\nData generation complete!")
    print(f"Total categories: {len(CATEGORIES)}")
    print(f"Total products: {len(products)}")
    print(f"Total stores: {len(stores)}")
    print(f"Total sales records: {NUM_SALES}")
    print("\ndata generation by DataGeneration-deepSeek.py")
if __name__ == "__main__":
    main()