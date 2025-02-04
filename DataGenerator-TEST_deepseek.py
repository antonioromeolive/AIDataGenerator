import unittest
import csv
import os
from datetime import datetime
from collections import defaultdict
import Deepseek.DataGenerator_deepSeek as DataGenerator_deepSeek

class TestSalesDataGenerator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Generate test data
        cls.stores = generate_stores()
        cls.products = generate_products()
        generate_sales(cls.stores, cls.products)
        save_supporting_data(CATEGORIES, cls.products, cls.stores)
        
        # Load generated data for validation
        cls.load_generated_data()

    @classmethod
    def load_generated_data(cls):
        # Load stores data
        with open('stores.csv') as f:
            reader = csv.DictReader(f)
            cls.stores_data = list(reader)

        # Load products data
        with open('products.csv') as f:
            reader = csv.DictReader(f)
            cls.products_data = list(reader)

        # Load categories data
        with open('categories.csv') as f:
            reader = csv.DictReader(f)
            cls.categories_data = list(reader)

        # Load sales data
        with open('sales_data.csv') as f:
            reader = csv.DictReader(f)
            cls.sales_data = list(reader)

    # Helper methods
    def get_category_price_range(self, category_id):
        for cat in CATEGORIES:
            if cat['id'] == int(category_id):
                return cat['price_range']
        return (0, 0)

    def validate_date(self, date_str):
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def validate_time(self, time_str):
        try:
            datetime.strptime(time_str, '%H:%M:%S')
            return True
        except ValueError:
            return False

    # Test cases
    def test_store_generation(self):
        """Test store data generation"""
        # Test number of stores
        self.assertEqual(len(self.stores_data), 45)
        
        # Test uniqueness of store names
        store_names = [store['store_name'] for store in self.stores_data]
        self.assertEqual(len(store_names), len(set(store_names)))

        # Test required fields
        for store in self.stores_data:
            self.assertIn('city', store)
            self.assertIn('country', store)
            self.assertIn('continent', store)

    def test_product_generation(self):
        """Test product data generation"""
        # Test number of products (10 per category)
        expected_products = len(CATEGORIES) * 10
        self.assertEqual(len(self.products_data), expected_products)

        # Test price ranges
        for product in self.products_data:
            category_id = product['category_id']
            min_price, max_price = self.get_category_price_range(category_id)
            price = float(product['unit_price'])
            self.assertTrue(min_price <= price <= max_price)

    def test_sales_data_quality(self):
        """Test sales data validity"""
        # Test required fields
        required_fields = ['date', 'time', 'product_name', 
                         'unit_price', 'quantity', 'revenue']
        for sale in self.sales_data:
            for field in required_fields:
                self.assertIn(field, sale)
                self.assertTrue(sale[field])  # Check for empty values

        # Test date/time validity
        for sale in self.sales_data:
            self.assertTrue(self.validate_date(sale['date']))
            self.assertTrue(self.validate_time(sale['time']))

        # Test revenue calculation
        for sale in self.sales_data:
            expected = float(sale['unit_price']) * int(sale['quantity'])
            self.assertAlmostEqual(float(sale['revenue']), expected, places=2)

    def test_campaign_application(self):
        """Test campaign discounts are applied correctly"""
        campaign_count = 0
        for sale in self.sales_data:
            if sale['campaign']:
                campaign_count += 1
                original_price = next(
                    (float(p['unit_price']) for p in self.products_data 
                     if p['product_name'] == sale['product_name']), None)
                discounted_price = float(sale['unit_price'])
                self.assertLess(discounted_price, original_price)
        
        # Check campaign application rate (~10%)
        campaign_rate = campaign_count / len(self.sales_data)
        self.assertTrue(0.08 <= campaign_rate <= 0.12)

    def test_seasonality_impact(self):
        """Test seasonal products show increased sales"""
        seasonal_data = defaultdict(int)
        for sale in self.sales_data:
            product = next(p for p in self.products_data 
                          if p['product_name'] == sale['product_name'])
            category = next(c for c in CATEGORIES 
                           if c['id'] == int(product['category_id']))
            month = datetime.strptime(sale['date'], '%Y-%m-%d').month
            if category['name'] in SEASONALITY:
                if month in SEASONALITY[category['name']]:
                    seasonal_data[category['name']] += 1

        # Check minimum seasonal boost
        for category, months in SEASONALITY.items():
            seasonal_sales = seasonal_data.get(category, 0)
            total_sales = len([s for s in self.sales_data 
                              if any(p['product_name'] == s['product_name'] 
                                     for p in self.products_data 
                                     if int(p['category_id']) == 
                                        next(c['id'] for c in CATEGORIES 
                                            if c['name'] == category))])
            seasonal_ratio = seasonal_sales / total_sales
            expected_ratio = len(months) / 12 * 2  # Double weight during season
            self.assertGreater(seasonal_ratio, expected_ratio * 0.8)

    def test_gdp_weighting(self):
        """Test store selection follows GDP weighting"""
        store_sales = defaultdict(int)
        for sale in self.sales_data:
            store_sales[sale['store_name']] += 1

        # Get GDP weights from original stores
        store_weights = {s['store_name']: s['gdp_weight'] for s in self.stores}
        total_weight = sum(float(s['gdp_weight']) for s in self.stores)
        
        # Calculate correlation between weights and sales
        weight_vs_sales = []
        for store, sales in store_sales.items():
            weight = store_weights[store]
            weight_vs_sales.append((weight, sales))

        # Simple check that higher weight stores have more sales
        sorted_pairs = sorted(weight_vs_sales, key=lambda x: x[0], reverse=True)
        top_third = sum(p[1] for p in sorted_pairs[:15])
        bottom_third = sum(p[1] for p in sorted_pairs[-15:])
        self.assertGreater(top_third, bottom_third)

    def test_file_creation(self):
        """Test all required files are created with proper headers"""
        required_files = [
            ('categories.csv', ['category_id', 'category_name']),
            ('products.csv', ['product_id', 'product_name', 'category_id', 'unit_price']),
            ('stores.csv', ['store_name', 'city', 'state', 'country', 'continent']),
            ('sales_data.csv', ['date', 'time', 'product_name', 'unit_price',
                              'quantity', 'revenue', 'store_name', 'campaign'])
        ]
        
        for filename, headers in required_files:
            with self.subTest(filename=filename):
                self.assertTrue(os.path.exists(filename))
                with open(filename) as f:
                    reader = csv.reader(f)
                    file_headers = next(reader)
                    self.assertEqual(file_headers, headers)

if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)
    print("\nData Quality Analysis:")
    
    # Data Quality Metrics
    total_sales = len(sales_data)
    missing_values = {field: 0 for field in sales_data[0].keys()}
    
    for sale in sales_data:
        for field, value in sale.items():
            if not value.strip():
                missing_values[field] += 1
                
    print("\nMissing Values Analysis:")
    for field, count in missing_values.items():
        print(f"{field}: {count} missing ({count/total_sales:.2%})")
    
    # Referential integrity check
    valid_products = set(p['product_name'] for p in products_data)
    invalid_products = len([s for s in sales_data if s['product_name'] not in valid_products])
    print(f"\nInvalid product references: {invalid_products} ({invalid_products/total_sales:.2%})")
    
    # Price validity check
    price_errors = 0
    for sale in sales_data:
        product = next((p for p in products_data if p['product_name'] == sale['product_name']), None)
        if product and not sale['campaign']:
            if float(sale['unit_price']) != float(product['unit_price']):
                price_errors += 1
    print(f"Price inconsistencies: {price_errors} ({price_errors/total_sales:.2%})")
    
    # Seasonal impact report
    print("\nSeasonal Impact Analysis:")
    seasonal_sales = defaultdict(int)
    for sale in sales_data:
        product = next(p for p in products_data if p['product_name'] == sale['product_name'])
        category = next(c['name'] for c in CATEGORIES if c['id'] == int(product['category_id']))
        month = datetime.strptime(sale['date'], '%Y-%m-%d').month
        seasonal_sales[(category, month)] += 1
    
    for category in SEASONALITY:
        seasonal_months = SEASONALITY[category]
        total = sum(seasonal_sales.get((category, m), 0) for m in range(1,13))
        seasonal_total = sum(seasonal_sales.get((category, m), 0) for m in seasonal_months)
        print(f"{category}: {seasonal_total/total:.2%} of sales in seasonal months")