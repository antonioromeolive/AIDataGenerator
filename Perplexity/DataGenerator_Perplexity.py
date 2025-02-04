import csv
import random
from datetime import datetime, timedelta
from faker import Faker

# Initialize Faker for generating fake data
fake = Faker()

# Constants
NUM_RECORDS = 10000
NUM_CATEGORIES = 10
NUM_PRODUCTS = 50
NUM_STORES = 45

# Product categories and their corresponding products
categories = {
    "Electronics": ["Smartphone", "Laptop", "Tablet", "Headphones", "Smartwatch"],
    "Clothing": ["T-shirt", "Jeans", "Jacket", "Dress", "Shoes"],
    "Home Appliances": ["Refrigerator", "Microwave", "Washing Machine", "Vacuum Cleaner"],
    "Books": ["Fiction", "Non-Fiction", "Children's Books", "Textbooks"],
    "Toys": ["Action Figure", "Board Game", "Puzzle", "Doll"],
}

# Store information
stores = []
store_names = set()

# Generate unique store names and their details
def generate_stores():
    cities = [
        ("New York", "NY", "USA"),
        ("London", "", "UK"),
        ("Tokyo", "", "Japan"),
        ("Berlin", "", "Germany"),
        ("Paris", "", "France"),
        ("Sydney", "", "Australia"),
        ("Toronto", "ON", "Canada"),
        ("Mumbai", "", "India"),
        ("São Paulo", "", "Brazil"),
        ("Cape Town", "", "South Africa"),
        # Add more cities as needed
    ]
    
    continents = {
        'North America': ['USA', 'Canada', 'Mexico'],
        'Europe': ['UK', 'Germany', 'France', 'Italy'],
        'Asia': ['Japan', 'India', 'China'],
        'Australia': ['Australia'],
        'South America': ['Brazil', 'Argentina'],
        'Africa': ['South Africa', 'Nigeria']
    }

    for city, state, country in cities:
        continent = next((k for k, v in continents.items() if country in v), "")
        store_name = f"{fake.company()} Store"
        
        while store_name in store_names:
            store_name = f"{fake.company()} Store"
        
        stores.append([store_name, city, state, country, continent])
        store_names.add(store_name)

generate_stores()

# Save stores to CSV
with open('stores_Perplexity.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Store Name", "City", "State", "Country", "Continent"])
    writer.writerows(stores)

# Generate product categories and products
product_categories = []
products = []

for category_name, product_list in categories.items():
    product_categories.append([category_name])
    for product in product_list:
        products.append({
            'name': product,
            'category': category_name,
            'min_price': random.uniform(10.0, 500.0),
            'max_price': random.uniform(501.0, 1500.0)
        })

# Save categories to CSV
with open('categories_Perplexity.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Category Name"])
    writer.writerows(product_categories)

# Save products to CSV with their categories
with open('products_Perplexity.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Product Name", "Category"])
    for product in products:
        writer.writerow([product['name'], product['category']])

# Generate sales data with seasonality and campaigns
sales_data = []
campaigns = ["10% off Black Friday", "Summer Sale", None]
gdp_weights = {
    'USA': 21.43,
    'UK': 2.83,
    'Japan': 4.97,
    'Germany': 4.84,
    'France': 2.78,
}

def generate_sales_data():
    for i in range(NUM_RECORDS):
        date = fake.date_between(start_date='-2y', end_date='today')
        time = fake.time()
        
        # Select a random product and its price range
        product = random.choice(products)
        unit_price = random.uniform(product['min_price'], product['max_price'])
        
        # Determine quantity sold based on seasonality (e.g., higher during holidays)
        quantity_sold = random.randint(1, 20) if date.month in [11, 12] else random.randint(1, 5)
        
        revenue = unit_price * quantity_sold
        
        # Select a random store
        store_info = random.choice(stores)
        
        # Determine sales campaign randomly
        campaign_name = random.choice(campaigns)
        
        sales_data.append([
            date,
            time,
            product['name'],
            round(unit_price, 2),
            quantity_sold,
            round(revenue, 2),
            store_info[0],
            campaign_name,
        ])
        
        if (i + 1) % 1000 == 0:
            print(f"Generated {i + 1} records...")

generate_sales_data()

# Save sales data to CSV
with open('sales_data_Perplexity.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Date", "Time", "Product Name", "Unit Price", 
                     "Quantity Sold", "Revenue", 
                     "Store Name", "Sales Campaign"])
    writer.writerows(sales_data)

# Summary of generated data
print("Data Generation Complete!")
print(f"Total Categories: {len(categories)}")
print(f"Total Products: {len(products)}")
print(f"Total Stores: {len(stores)}")
print(f"Total Sales Records: {len(sales_data)}")
print("\nData generation by DataGenerator_Perplexity.py")
