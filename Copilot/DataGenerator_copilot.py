import csv
import random
import datetime
import pandas as pd

# Step 1: Generate and store detailed sales data
def generate_sales_data(num_records):
    sales_data = []
    for i in range(num_records):
        date = datetime.date.today() - datetime.timedelta(days=random.randint(0, 365))
        time = datetime.time(random.randint(0, 23), random.randint(0, 59))
        product_name = f"Product_{random.randint(1, 100)}"
        unit_price = round(random.uniform(5.0, 100.0), 2)
        quantity = random.randint(1, 20)
        revenue = round(unit_price * quantity, 2)
        store_name = f"Store_{random.randint(1, 45)}"
        campaign = random.choice(["", "10% off Black Friday", "Summer Sale"])
        
        sales_data.append([date, time, product_name, unit_price, quantity, revenue, store_name, campaign])
        
        if (i + 1) % 1000 == 0:
            print(f"{i + 1} records generated...")
    
    with open('sales_data_CP.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["date", "time", "product_name", "unit_price", "quantity", "revenue", "store_name", "campaign"])
        writer.writerows(sales_data)
    
    print(f"Total {num_records} sales records generated.")

# Step 2: Create categories and assign them to products
def generate_categories_and_products():
    categories = ["Electronics", "Clothing", "Home & Kitchen", "Sports", "Toys"]
    products = {f"Product_{i}": random.choice(categories) for i in range(1, 101)}
    
    with open('categories_CP.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["category"])
        for category in categories:
            writer.writerow([category])
    
    with open('products_CP.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["product_name", "category"])
        for product, category in products.items():
            writer.writerow([product, category])
    
    print(f"Total {len(categories)} categories and {len(products)} products gener
          ated.")

# Step 3: Generate store data
def generate_store_data():
    stores = [
        {"store_name": f"Store_{i}", "city": f"City_{i}", "state": f"State_{i}", "country": f"Country_{i}", "continent": "Continent"}
        for i in range(1, 46)
    ]
    
    with open('stores_CP.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["store_name", "city", "state", "country", "continent"])
        for store in stores:
            writer.writerow([store["store_name"], store["city"], store["state"], store["country"], store["continent"]])
    
    print(f"Total {len(stores)} stores generated.")

# Main function to run all steps
def main():
    num_records = 10000
    generate_sales_data(num_records)
    generate_categories_and_products()
    generate_store_data()
    print("Data generation completed.")
    print("\ndata generation by DataGeneration-copilot.py")

if __name__ == "__main__":
    main()