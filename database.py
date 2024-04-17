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
        customer_id INTEGER, order_date TEXT, order_status INTEGER, created_at TEXT, updated_at TEXT,
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
                        INSERT INTO orders (customer_id, order_date, order_status, created_at, updated_at) 
                        VALUES (?, ?, ?, datetime('now'), datetime('now'))
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
        cursor = self.connection.cursor()
        try:
            # Execute the SQL query to retrieve orders, customer information, and products
            cursor.execute("""
                SELECT o.id AS order_id, o.order_date, o.order_status, o.created_at,
                       c.name, c.last_name, c.phone, c.address, c.commercial_register_number, c.tax_number,
                       c.tax_item_number, c.statistical_id,
                       oi.product_name, oi.product_category, oi.quantity,
                       oi.price_at_order_time, oi.vat_tax_at_order_time, oi.stamp_tax_at_order_time
                FROM orders o
                LEFT JOIN customers c ON o.customer_id = c.id
                LEFT JOIN order_items oi ON o.id = oi.order_id
                ORDER BY o.order_date DESC, o.created_at ASC
            """)

            # Fetch all rows
            rows = cursor.fetchall()

            orders_dict = {}

            # Iterate through the rows and organize the data into a dictionary of orders
            for row in rows:
                order_id = row[0]
                order_info = {
                    "id": row[0],
                    "order_date": row[1],
                    "order_status": row[2],
                    "created_at": row[3],
                    "customer_info": {
                        "name": row[4],
                        "last_name": row[5],
                        "phone": row[6],
                        "address": row[7],
                        "commercial_register_number": row[8],
                        "tax_number": row[9],
                        "tax_item_number": row[10],
                        "statistical_id": row[11]
                    },
                    "products": []
                }

                product_info = {
                    "product_name": row[12],
                    "product_category": row[13],
                    "quantity": row[14],
                    "price_at_order_time": row[15],
                    "vat_tax_at_order_time": row[16],
                    "stamp_tax_at_order_time": row[17]
                }

                # Append product information to the list of products for the current order
                order_info["products"].append(product_info)

                # Add the order information to the orders dictionary
                if order_id not in orders_dict:
                    orders_dict[order_id] = order_info
                else:
                    orders_dict[order_id]["products"].append(product_info)

            return orders_dict
        except Exception as e:
            print(f"Error fetching orders: {e}")
            return {}

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
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT order_status FROM orders WHERE id = ?", (order_id, ))
            current_status = cursor.fetchone()[0]
            new_status = "لم يتم دفع الفاتورة" if current_status == "تم دفع الفاتورة" else "تم دفع الفاتورة"
            cursor.execute("""UPDATE orders SET order_status = ?, updated_at = datetime('now') 
                                            WHERE id = ?""", (new_status, order_id))
            self.connection.commit()
            print("order status updated successfully")

        except Exception as e:
            print(f"Error updating the order status: {e}")

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
git 