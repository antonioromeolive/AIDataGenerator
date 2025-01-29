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
from datetime import datetime, timedelta

# Configuration
NUM_SALES = 10000  # Adjust number of sales records as needed

# Categories and Products
categories = [
    'Electronics',
    'Clothing',
    'Home & Kitchen',
    'Books',
    'Toys & Games',
    'Sports & Outdoors',
    'Beauty & Personal Care',
    'Groceries'
]

products = [
    # Electronics
    {'name': 'Smartphone', 'category': 'Electronics', 'min_price': 500, 'max_price': 1000, 'base_weight': 2.0},
    {'name': 'Laptop', 'category': 'Electronics', 'min_price': 800, 'max_price': 2000, 'base_weight': 1.5},
    {'name': 'Headphones', 'category': 'Electronics', 'min_price': 50, 'max_price': 300, 'base_weight': 2.5},
    
    # Clothing
    {'name': 'T-Shirt', 'category': 'Clothing', 'min_price': 10, 'max_price': 30, 'base_weight': 3.0},
    {'name': 'Jeans', 'category': 'Clothing', 'min_price': 40, 'max_price': 80, 'base_weight': 2.5},
    {'name': 'Winter Jacket', 'category': 'Clothing', 'min_price': 80, 'max_price': 150, 'base_weight': 1.8},
    
    # Home & Kitchen
    {'name': 'Blender', 'category': 'Home & Kitchen', 'min_price': 40, 'max_price': 120, 'base_weight': 1.5},
    {'name': 'Cookware Set', 'category': 'Home & Kitchen', 'min_price': 100, 'max_price': 300, 'base_weight': 1.2},
    
    # Books
    {'name': 'Bestseller Novel', 'category': 'Books', 'min_price': 10, 'max_price': 25, 'base_weight': 2.0},
    {'name': 'Cookbook', 'category': 'Books', 'min_price': 15, 'max_price': 35, 'base_weight': 1.5},
    
    # Toys & Games
    {'name': 'Board Game', 'category': 'Toys & Games', 'min_price': 20, 'max_price': 50, 'base_weight': 2.2},
    {'name': 'LEGO Set', 'category': 'Toys & Games', 'min_price': 30, 'max_price': 100, 'base_weight': 2.5},
    
    # Sports & Outdoors
    {'name': 'Yoga Mat', 'category': 'Sports & Outdoors', 'min_price': 15, 'max_price': 40, 'base_weight': 1.8},
    {'name': 'Running Shoes', 'category': 'Sports & Outdoors', 'min_price': 60, 'max_price': 120, 'base_weight': 2.0},
    
    # Beauty & Personal Care
    {'name': 'Skincare Set', 'category': 'Beauty & Personal Care', 'min_price': 30, 'max_price': 80, 'base_weight': 2.2},
    {'name': 'Perfume', 'category': 'Beauty & Personal Care', 'min_price': 50, 'max_price': 150, 'base_weight': 1.5},
    
    # Groceries
    {'name': 'Organic Coffee', 'category': 'Groceries', 'min_price': 8, 'max_price': 15, 'base_weight': 3.5},
    {'name': 'Snack Box', 'category': 'Groceries', 'min_price': 5, 'max_price': 10, 'base_weight': 4.0}
]

# Stores and Countries Data
countries = [
    {
        'name': 'USA', 'continent': 'North America', 'gdp': 25e12,
        'cities': [
            {'name': 'New York', 'state': 'NY'},
            {'name': 'Los Angeles', 'state': 'CA'},
            {'name': 'Chicago', 'state': 'IL'},
            {'name': 'Houston', 'state': 'TX'},
            {'name': 'Phoenix', 'state': 'AZ'}
        ]
    },
    {
        'name': 'Japan', 'continent': 'Asia', 'gdp': 4.9e12,
        'cities': [
            {'name': 'Tokyo', 'state': 'Kanto'},
            {'name': 'Osaka', 'state': 'Kansai'}
        ]
    },
    {
        'name': 'Germany', 'continent': 'Europe', 'gdp': 4.2e12,
        'cities': [
            {'name': 'Berlin', 'state': 'Berlin'},
            {'name': 'Hamburg', 'state': 'Hamburg'},
            {'name': 'Munich', 'state': 'Bavaria'}
        ]
    },
    {
        'name': 'UK', 'continent': 'Europe', 'gdp': 3.1e12,
        'cities': [
            {'name': 'London', 'state': 'England'},
            {'name': 'Manchester', 'state': 'England'},
            {'name': 'Edinburgh', 'state': 'Scotland'}
        ]
    },
    {
        'name': 'China', 'continent': 'Asia', 'gdp': 18e12,
        'cities': [
            {'name': 'Beijing', 'state': 'Hebei'},
            {'name': 'Shanghai', 'state': 'Jiangsu'},
            {'name': 'Guangzhou', 'state': 'Guangdong'}
        ]
    },
    {
        'name': 'Brazil', 'continent': 'South America', 'gdp': 1.9e12,
        'cities': [
            {'name': 'Sao Paulo', 'state': 'SP'},
            {'name': 'Rio de Janeiro', 'state': 'RJ'}
        ]
    },
    {
        'name': 'Australia', 'continent': 'Oceania', 'gdp': 1.6e12,
        'cities': [
            {'name': 'Sydney', 'state': 'NSW'},
            {'name': 'Melbourne', 'state': 'VIC'}
        ]
    },
    {
        'name': 'South Africa', 'continent': 'Africa', 'gdp': 400e9,
        'cities': [
            {'name': 'Cape Town', 'state': 'Western Cape'},
            {'name': 'Johannesburg', 'state': 'Gauteng'}
        ]
    },
    {
        'name': 'India', 'continent': 'Asia', 'gdp': 3.4e12,
        'cities': [
            {'name': 'Mumbai', 'state': 'Maharashtra'},
            {'name': 'Delhi', 'state': 'Delhi'}
        ]
    }
]

# Seasonality Configuration
category_seasonality = {
    'Electronics': {'peak_months': [11, 12], 'multiplier': 2.0},
    'Clothing': {'peak_months': [6, 7], 'multiplier': 1.8},
    'Home & Kitchen': {'peak_months': [4], 'multiplier': 1.5},
    'Books': {'peak_months': [11, 12], 'multiplier': 1.4},
    'Toys & Games': {'peak_months': [12], 'multiplier': 2.2},
    'Sports & Outdoors': {'peak_months': [5, 6], 'multiplier': 1.6},
    'Beauty & Personal Care': {'peak_months': [11, 12], 'multiplier': 1.7},
    'Groceries': {'peak_months': [], 'multiplier': 1.0}  # No seasonality
}

# Sales Campaigns
campaigns = [
    {
        'name': '10% off Black Friday',
        'start_date': datetime(2023, 11, 24),
        'end_date': datetime(2023, 11, 27)
    },
    {
        'name': 'Summer Sale',
        'start_date': datetime(2023, 6, 1),
        'end_date': datetime(2023, 6, 30)
    },
    {
        'name': 'Back to School',
        'start_date': datetime(2023, 8, 15),
        'end_date': datetime(2023, 9, 15)
    },
    {
        'name': 'Cyber Monday',
        'start_date': datetime(2023, 11, 27),
        'end_date': datetime(2023, 11, 27)
    },
    {
        'name': 'Holiday Special',
        'start_date': datetime(2023, 12, 15),
        'end_date': datetime(2023, 12, 31)
    }
]

# Rest of the code remains the same as previous version...
# [Include all the functions (generate_categories, generate_products, generate_stores, generate_sales_data, main) 
#  from the original code here without changes]

def generate_categories():
    with open('categories_DS.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['category_name'])
        writer.writerows([[c] for c in categories])

def generate_products():
    with open('products_DS.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['product_name', 'category_name'])
        writer.writerows([[p['name'], p['category']] for p in products])

def generate_stores():
    stores = []
    for country in countries:
        for city_info in country['cities']:
            stores.append({
                'store_name': f"{city_info['name']} Store",
                'city': city_info['name'],
                'state': city_info.get('state', ''),
                'country': country['name'],
                'continent': country['continent'],
                'gdp': country['gdp']
            })
    
    # Calculate store weights
    for store in stores:
        country = next(c for c in countries if c['name'] == store['country'])
        store['gdp_weight'] = country['gdp'] / len(country['cities'])
    
    with open('stores_DS.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=stores[0].keys())
        writer.writeheader()
        writer.writerows(stores)
    return stores

def generate_sales_data(stores):
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)
    date_range = (end_date - start_date).days

    with open('sales_data_DS.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'date', 'time', 'product_name', 'unit_price',
            'quantity', 'revenue', 'store_name', 'sales_campaign'
        ])
        writer.writeheader()

        for i in range(NUM_SALES):
            if (i + 1) % 1000 == 0:
                print(f'Generated {i + 1} records...')

            # Generate sale details
            sale_date = start_date + timedelta(days=random.randint(0, date_range))
            current_month = sale_date.month
            
            # Select product with seasonality
            product_weights = []
            for p in products:
                season = category_seasonality[p['category']]
                multiplier = season['multiplier'] if season['peak_months'] and current_month in season['peak_months'] else 1.0
                product_weights.append(p['base_weight'] * multiplier)
            
            product = random.choices(products, weights=product_weights, k=1)[0]
            
            # Select store with GDP weighting
            store = random.choices(stores, weights=[s['gdp_weight'] for s in stores], k=1)[0]
            
            # Generate pricing and quantity
            unit_price = round(random.uniform(product['min_price'], product['max_price']), 2)
            quantity = random.randint(1, 10)
            revenue = round(unit_price * quantity, 2)
            
            # Determine campaign
            campaign = None
            if random.random() < 0.1:
                active_campaigns = []
                for c in campaigns:
                    if c['start_date'] and c['end_date']:
                        if c['start_date'] <= sale_date <= c['end_date']:
                            active_campaigns.append(c['name'])
                    else:
                        active_campaigns.append(c['name'])
                if active_campaigns:
                    campaign = random.choice(active_campaigns)
            
            # Write record
            writer.writerow({
                'date': sale_date.strftime('%Y-%m-%d'),
                'time': f"{random.randint(8, 20):02d}:{random.randint(0, 59):02d}",
                'product_name': product['name'],
                'unit_price': unit_price,
                'quantity': quantity,
                'revenue': revenue,
                'store_name': store['store_name'],
                'sales_campaign': campaign or ''
            })

def main():
    print("Generating categories...")
    generate_categories()
    
    print("Generating products...")
    generate_products()
    
    print("Generating stores...")
    stores = generate_stores()
    
    print("Generating sales data...")
    generate_sales_data(stores)
    
    print("\nSummary Statistics:")
    print(f"Total categories: {len(categories)}")
    print(f"Total products: {len(products)}")
    print(f"Total stores: {len(stores)}")
    print(f"Total sales records: {NUM_SALES}")

if __name__ == '__main__':
    main()