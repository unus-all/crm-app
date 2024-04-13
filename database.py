import sqlite3
import os


class Database:
    def __init__(self):
        try:
            self.connection = sqlite3.connect("data.db")
            print("Connected to database with success")
        except Exception as e:
            print(f"Error during opening the database: {e}")

    def create_tables(self):
        cursor = self.connection.cursor()

        # Customers table
        cursor.execute("""CREATE TABLE IF NOT EXISTS customers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, last_name TEXT, phone TEXT, address TEXT, commercial_register_number TEXT, tax_number TEXT,
        tax_item_number TEXT, statistical_id TEXT, updated_at TEXT
        )""")
        self.connection.commit()

        # Products table
        cursor.execute("""CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, category TEXT, price REAL, vat_tax REAL, stamp_tax TEXT, available_quantity REAL, unit TEXT, 
        updated_at TEXT
        )""")
        self.connection.commit()

        # Order table
        cursor.execute("""CREATE TABLE IF NOT EXISTS orders(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER, order_date TEXT, order_status INTEGER, FOREIGN KEY (customer_id) REFERENCES customers(id)
        )""")
        self.connection.commit()

        # OrderItems table
        cursor.execute("""CREATE TABLE IF NOT EXISTS order_items(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER, product_id INTEGER, quantity REAL, price_at_order_time REAL, vat_tax_at_order_time INTEGER,
        stamp_tax_at_order_time INTEGER, 
        FOREIGN KEY (order_id) REFERENCES orders(id), FOREIGN KEY (product_id) REFERENCES products(id)
        )""")

    def add_customer(self, data):
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO customers (name, last_name, phone, address, commercial_register_number, 
                                       tax_number, tax_item_number, statistical_id, updated_at) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
            """, (data["name"], data["last_name"], data["phone"], data["address"], data["commercial_register_number"],
                  data["tax_number"], data["tax_item_number"], data["statistical_id"]))
            self.connection.commit()
            print("Customer added successfully")
            return "تم إضافة الزبون بنجاح"
        except Exception as e:
            print(f"Error adding customer: {e}")
            return "حدث خطأ أثناء إضافة الزبون"

    def add_product(self, data):
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO products (name, category, price, vat_tax, stamp_tax, available_quantity, unit, updated_at) 
                VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))
            """, (data["name"], data["category"], data["price"], data["vat_tax"], data["stamp_tax"],
                  data["available_quantity"], data["unit"]))
            self.connection.commit()
            print("Product added successfully")
            return "تم إضافة السلعة بنجاح"
        except Exception as e:
            print(f"Error adding product: {e}")
            return "حدث خطأ أثناء إضافة السلعة"

    def add_order(self, data):
        pass

    def get_customers(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM customers ORDER BY updated_at DESC")
        return cursor.fetchall()

    def get_products(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM products ORDER BY updated_at DESC")
        return cursor.fetchall()

    def get_orders(self):
        return []

    def update_customer(self, data):
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
                UPDATE customers 
                SET name = ?, last_name = ?, phone = ?, address = ?, commercial_register_number = ?, 
                    tax_number = ?, tax_item_number = ?, statistical_id = ?, updated_at = datetime('now') 
                WHERE id = ?
            """, (data["name"], data["last_name"], data["phone"], data["address"], data["commercial_register_number"],
                  data["tax_number"], data["tax_item_number"], data["statistical_id"], data["id"]))
            self.connection.commit()
            print("Customer updated successfully")
            return "تم تحديث الزبون بنجاح"
        except Exception as e:
            print(f"Error updating customer: {e}")
            return "حدث خطأ أثناء تحديث الزبون"

    def update_product(self, data):
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
                    UPDATE products 
                    SET name = ?, category = ?, price = ?, vat_tax = ?, stamp_tax = ?, 
                        available_quantity = ?, unit = ?, updated_at = datetime('now') 
                    WHERE id = ?
                """, (data["name"], data["category"], data["price"], data["vat_tax"], data["stamp_tax"],
                      data["available_quantity"], data["unit"], data["id"]))
            self.connection.commit()
            print("Product updated successfully")
            return "تم تحديث السلعة بنجاح"

        except Exception as e:
            print(f"Error updating product: {e}")
            return "حدث خطأ أثناء تحديث السلعة"

    def update_order_status(self, order_id):
        pass

    def delete_customer(self, customer_id):
        pass

    def delete_product(self, product_id):
        pass

    def delete_order(self, order_id):
        pass