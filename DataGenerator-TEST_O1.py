import unittest
import os
import csv
import random
from datetime import datetime
from OpenAI_o1.DataGenerator_o1 import generate_stores, expand_products_and_categories, seasonality_factor, main, CATEGORIES, NUM_SALES_RECORDS

class TestDataGeneration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # We'll run the main function once with smaller records to keep test quick
        # Alternatively, use the existing 50k if desired.
        # Let's override to generate fewer records for testing.
        # We'll backup original and restore after.
        cls.original_sales_records = NUM_SALES_RECORDS
        # Attempt to override
        # But be mindful that it might not do anything if the script references NUM_SALES_RECORDS directly.
        # We'll patch that variable.
        import OpenAI_o1.DataGenerator_o1 as DataGenerator_o1
        DataGenerator_o1.NUM_SALES_RECORDS = 2000  # smaller run

        # Remove old CSVs if they exist
        for filename in ["categories.csv", "products.csv", "stores.csv", "sales_data.csv"]:
            if os.path.exists(filename):
                os.remove(filename)

        # Generate fresh data
        DataGenerator_o1.main()

    @classmethod
    def tearDownClass(cls):
        # Restore the original value
        import OpenAI_o1.DataGenerator_o1 as DataGenerator_o1
        DataGenerator_o1.NUM_SALES_RECORDS = cls.original_sales_records

    def test_generate_stores_function(self):
        # Test that generate_stores returns correct number of stores and correct format
        stores = generate_stores(10)
        self.assertEqual(len(stores), 10)
        for store in stores:
            self.assertEqual(len(store), 5)
            # store_name, city, state, country, continent
            self.assertIsInstance(store[0], str)
            self.assertIsInstance(store[1], str)
            self.assertIsInstance(store[2], str)
            self.assertIsInstance(store[3], str)
            self.assertIsInstance(store[4], str)

    def test_expand_products_and_categories_function(self):
        # Make sure the function returns correct structures
        cat_map, products = expand_products_and_categories()
        # cat_map should have length == len(CATEGORIES)
        self.assertEqual(len(cat_map), len(CATEGORIES))
        # products should be flattened list, ensure it has some items
        self.assertTrue(len(products) > 0)
        # check format: (product_id, product_name, cat_id, pmin, pmax)
        for p in products:
            self.assertEqual(len(p), 5)
            self.assertIsInstance(p[0], int)
            self.assertIsInstance(p[1], str)
            self.assertIsInstance(p[2], int)
            self.assertIsInstance(p[3], (float, int))
            self.assertIsInstance(p[4], (float, int))

    def test_seasonality_factor_function(self):
        # Check known values from the SEASONALITY dict
        # e.g. Electronics in November => 1.2
        f = seasonality_factor("Electronics", 11)
        self.assertAlmostEqual(f, 1.2)
        # unknown category => 1.0
        f2 = seasonality_factor("NotARealCategory", 11)
        self.assertAlmostEqual(f2, 1.0)

    def test_csv_files_created(self):
        # After running main, these files should exist
        for filename in ["categories.csv", "products.csv", "stores.csv", "sales_data.csv"]:
            self.assertTrue(os.path.exists(filename), f"{filename} should be created.")

    def test_categories_csv(self):
        # Check that categories.csv has correct header and content
        with open("categories.csv", "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)
        # first row: ["category_id", "category_name"]
        self.assertEqual(rows[0], ["category_id", "category_name"])
        # subsequent rows = number of categories
        self.assertEqual(len(rows) - 1, len(CATEGORIES))

    def test_products_csv(self):
        with open("products.csv", "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)
        # header check
        self.assertEqual(rows[0], ["product_id", "product_name", "category_id", "min_price", "max_price"])
        # ensure we have some products
        self.assertTrue(len(rows) > 1)

    def test_stores_csv(self):
        with open("stores.csv", "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)
        # header check
        self.assertEqual(rows[0], ["store_name", "city", "state", "country", "continent"])
        # check we got 45 stores (since main calls generate_stores(45))
        # minus 1 for header
        self.assertEqual(len(rows) - 1, 45)

    def test_sales_data_csv(self):
        with open("sales_data.csv", "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)
        # header
        self.assertEqual(rows[0], ["date", "time", "product_name", "unit_price", "quantity", "revenue", "store_name", "campaign"])
        # ensure we have the correct # of records
        # minus 1 for header
        data_rows = rows[1:]
        self.assertEqual(len(data_rows), 2000)  # we set it to 2000 in setUpClass

        # Spot checks on data quality
        # parse first row
        sample_row = data_rows[0]
        self.assertIsNotNone(sample_row[0])  # date
        self.assertIsNotNone(sample_row[1])  # time
        self.assertIsNotNone(sample_row[2])  # product_name
        # check numeric fields can be parsed
        try:
            float(sample_row[3])  # unit_price
            int(sample_row[4])  # quantity
            float(sample_row[5])  # revenue
        except ValueError:
            self.fail("Numeric fields do not parse correctly.")

    def test_campaign_presence(self):
        # We want to see if there is at least some campaigns in the data
        # because the probability was 0.1
        with open("sales_data.csv", "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)
        campaigns = [row[7] for row in rows[1:]]  # skip header
        # ensure some non-empty campaigns
        non_empty = sum(bool(c.strip()) for c in campaigns)
        # expect at least a few if probability is 0.1
        self.assertGreater(non_empty, 0, "Expected at least some campaign entries.")

    def test_data_distribution(self):
        # Very rough check on data distribution
        # Check that we have multiple distinct product names and store names in the sales data
        with open("sales_data.csv", "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            product_names = set()
            store_names = set()
            for row in reader:
                product_names.add(row["product_name"])
                store_names.add(row["store_name"])
        # We expect quite a few distinct products, definitely more than 1
        self.assertTrue(len(product_names) > 10)
        # We expect 45 distinct store names, but they might not all appear if we generate fewer records.
        # Check that we have a decent coverage
        self.assertTrue(len(store_names) > 20, "Expected a variety of store names in sales.")


if __name__ == "__main__":
    unittest.main()
