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
        customer_id INTEGER, order_date TEXT, order_status INTEGER, updated_at TEXT,
        FOREIGN KEY (customer_id) REFERENCES customers(id)
        )""")
        self.connection.commit()

        # OrderItems table
        cursor.execute("""CREATE TABLE IF NOT EXISTS order_items(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER, product_name TEXT, product_category TEXT, quantity REAL, price_at_order_time REAL,
        vat_tax_at_order_time REAL, stamp_tax_at_order_time REAL, 
        FOREIGN KEY (order_id) REFERENCES orders(id)
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
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
                        INSERT INTO orders (customer_id, order_date, order_status, updated_at) 
                        VALUES (?, ?, ?, datetime('now'))
                    """, (data["customer_id"], data["order_date"], data["order_status"]))

            current_id = cursor.lastrowid

            for item in data["cart"]:
                vat_tax = item["quantity"]*item["price_at_order_time"]*item["vat_tax_at_order_time"]/100
                stamp_tax = item["quantity"]*item["price_at_order_time"]/100 if item["stamp_tax_at_order_time"] is True else 0
                cursor.execute("""INSERT INTO order_items (order_id, product_name, product_category, quantity,
                                        price_at_order_time, vat_tax_at_order_time, stamp_tax_at_order_time) 
                                        VALUES (?, ?, ?, ?, ?, ?, ?)""", (
                                        current_id, item["product_name"], item["product_category"], item["quantity"],
                                        item["price_at_order_time"], vat_tax, stamp_tax))

            self.connection.commit()

            print("Order added successfully")
            return "تم إضافة الطلب بنجاح"
        except Exception as e:
            print(f"Error adding order: {e}")
            return "حدث خطأ أثناء إضافة الطلب"

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

    def update_product_quantity(self, cart):
        cursor = self.connection.cursor()
        try:
            for data in cart:
                # Fetch the current available quantity
                cursor.execute("SELECT available_quantity FROM products WHERE id = ?", (data["id"],))
                current_quantity = cursor.fetchone()[0]

                # Calculate the new available quantity by subtracting the specified quantity
                new_quantity = max(0, current_quantity - data["quantity"])

                # Update the product's available quantity
                cursor.execute("""
                                UPDATE products 
                                SET available_quantity = ?, updated_at = datetime('now') 
                                WHERE id = ?
                            """, (new_quantity, data["id"]))

            self.connection.commit()
            print("Products updated successfully")
            return "تم تحديث السلع بنجاح"

        except Exception as e:
            print(f"Error updating products: {e}")
            return "حدث خطأ أثناء تحديث السلع"

    def delete_order(self, order_id):
        pass