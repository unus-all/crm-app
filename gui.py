# -*- coding: UTF-8 -*-

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sv_ttk
import database
from ctypes import windll
import help
from tkcalendar import DateEntry
import locale


class Products:
    def __init__(self, parent, data):
        self.product_name_e = None
        self.product_category_e = None
        self.product_price_e = None
        self.product_unit_e = None
        self.product_quantity_e = None
        self.product_tva_e = None
        self.product_stamp_e = None
        self.data = data
        self.my_tree = None
        self.selected_product = None
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self.setup_ui()

    def setup_ui(self):
        tree_frame = ttk.Frame(self.frame)
        tree_frame.pack(fill=tk.X, expand=True, padx=20, pady=5)

        self.my_tree = ttk.Treeview(tree_frame, selectmode="extended", height=5)
        self.my_tree.pack(side=tk.RIGHT, fill=tk.X, expand=True)

        scroll_frame = ttk.Frame(tree_frame)
        scroll_frame.pack(side=tk.RIGHT, fill=tk.Y)

        tree_scroll = ttk.Scrollbar(scroll_frame, orient="vertical", command=self.my_tree.yview)
        tree_scroll.pack(side=tk.LEFT, fill="y")

        self.my_tree.config(yscrollcommand=tree_scroll.set)

        cols = ("stamp_tax", "vat_tax", "price", "quantity", "category", "product", "id")
        self.my_tree['columns'] = cols

        self.my_tree.column("#0", width=0, stretch=tk.NO)
        self.my_tree.column("id", width=0, stretch=tk.NO)
        self.my_tree.column("product", anchor=tk.CENTER)
        self.my_tree.column("category", anchor=tk.CENTER)
        self.my_tree.column("quantity", anchor=tk.CENTER)
        self.my_tree.column("price", anchor=tk.CENTER)
        self.my_tree.column("vat_tax", anchor=tk.CENTER)
        self.my_tree.column("stamp_tax", anchor=tk.CENTER)

        self.my_tree.heading("#0", text="", anchor=tk.W)
        self.my_tree.heading("product", anchor=tk.CENTER, text="السلعة")
        self.my_tree.heading("category", anchor=tk.CENTER, text="النوع")
        self.my_tree.heading("price", anchor=tk.CENTER, text="السعر")
        self.my_tree.heading("quantity", anchor=tk.CENTER, text="الكمية")
        self.my_tree.heading("vat_tax", anchor=tk.CENTER, text="الضريبة المضافة")
        self.my_tree.heading("stamp_tax", anchor=tk.CENTER, text="ضريبة الطابع")
        self.my_tree.bind('<ButtonRelease-1>', lambda event: self.select_product()
                          if self.my_tree.identify_region(event.x, event.y) != "heading" else None)
        self.my_tree.bind('<Motion>', 'break')

        for record in self.data:
            self.my_tree.insert(parent='', index='end', text='',
                                values=(record[5], f"% {record[4]}", record[3],
                                        f"{str(record[6]).replace(".", ",")} {record[7]}", record[2], record[1],
                                        record[0]))

        data_frame = ttk.LabelFrame(self.frame, text="", labelanchor=tk.NE)
        data_frame.pack(fill="x", expand=True, padx=20, pady=5)

        data_frame.grid_columnconfigure(0, weight=1)
        data_frame.grid_columnconfigure(1, weight=1)
        data_frame.grid_columnconfigure(2, weight=1)
        data_frame.grid_columnconfigure(3, weight=1)

        product_name_l = ttk.Label(data_frame, text="السلعة")
        self.product_name_e = ttk.Entry(data_frame, font=normal_text, justify="right")
        product_name_l.grid(row=0, column=3, padx=10, pady=10)
        self.product_name_e.grid(row=0, column=2, padx=10, pady=10)

        product_category_l = ttk.Label(data_frame, text="النوع")
        self.product_category_e = ttk.Entry(data_frame, font=normal_text, justify="right")
        product_category_l.grid(row=1, column=3, padx=10, pady=10)
        self.product_category_e.grid(row=1, column=2, padx=10, pady=10)

        product_price_l = ttk.Label(data_frame, text="السعر (دج)")
        self.product_price_e = ttk.Entry(data_frame, font=normal_text, justify="right")
        product_price_l.grid(row=1, column=1, padx=10, pady=10)
        self.product_price_e.grid(row=1, column=0, padx=10, pady=10)

        product_quantity_l = ttk.Label(data_frame, text="الكمية")
        self.product_quantity_e = ttk.Entry(data_frame, font=normal_text, justify="right")
        product_quantity_l.grid(row=2, column=3, padx=10, pady=10)
        self.product_quantity_e.grid(row=2, column=2, padx=10, pady=10)

        product_unit_l = ttk.Label(data_frame, text="وحدة القياس")
        self.product_unit_e = ttk.Entry(data_frame, font=normal_text, justify="right")
        self.product_unit_e.insert(0, "كغ")
        product_unit_l.grid(row=2, column=1, padx=10, pady=10)
        self.product_unit_e.grid(row=2, column=0, padx=10, pady=10)

        product_tva_l = ttk.Label(data_frame, text="(%) الضريبة المضافة")
        self.product_tva_e = ttk.Combobox(data_frame, font=normal_text, justify="right", values=["0", "9", "19"])
        self.product_tva_e.current(0)
        product_tva_l.grid(row=3, column=3, padx=10, pady=10)
        self.product_tva_e.grid(row=3, column=2, padx=10, pady=10)

        product_stamp_l = ttk.Label(data_frame, text="ضريبة الطابع")
        self.product_stamp_e = ttk.Combobox(data_frame, font=normal_text, justify="right", values=["نعم", "لا"],
                                            state='readonly')
        self.product_stamp_e.current(1)
        product_stamp_l.grid(row=3, column=1, padx=10, pady=10)
        self.product_stamp_e.grid(row=3, column=0, padx=10, pady=10)

        buttons_frame = ttk.LabelFrame(self.frame, text="", labelanchor=tk.NE)
        buttons_frame.pack(fill="x", expand=tk.YES, padx=20)

        remove_button = ttk.Button(buttons_frame, text="حذف منتج", style="danger.TButton")
        remove_button.grid(row=0, column=0, padx=10, pady=10)

        update_button = ttk.Button(buttons_frame, text="تحديث منتج", style="warning.TButton",
                                   command=self.update_product)
        update_button.grid(row=0, column=1, padx=10, pady=10)

        add_button = ttk.Button(buttons_frame, text="إضافة منتج", style="success.TButton", command=self.add_product)
        add_button.grid(row=0, column=2, padx=10, pady=10)

        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)
        buttons_frame.grid_columnconfigure(2, weight=1)

    def validation(self):
        errors = []
        if not help.is_arabic(self.product_name_e.get()):
            errors.append("اسم السلعة يجب أن يكون باللغة العربية")
        if not help.is_arabic(self.product_category_e.get()):
            errors.append("نوع السلعة يجب أن يكون باللغة العربية")
        if not help.is_valid_price(self.product_price_e.get()):
            errors.append("تحقق من أن السعر صحيح")
        if not help.is_valid_quantity(self.product_quantity_e.get()):
            errors.append("تحقق من أن الكمية صحيحة")
        if not help.is_arabic(self.product_unit_e.get()):
            errors.append("وحدة القياس يجب أن تكون باللغة العربية")
        try:
            float(self.product_tva_e.get())
            # Input can be converted to a floating-point number
        except ValueError:
            errors.append("الضريبة المضافة يجب أن تكون عدد حقيقي")
        return errors

    def clear_entries(self):
        self.selected_product = None
        self.product_name_e.delete(0, tk.END)
        self.product_category_e.delete(0, tk.END)
        self.product_quantity_e.delete(0, tk.END)
        self.product_price_e.delete(0, tk.END)
        self.product_unit_e.delete(0, tk.END)
        self.product_unit_e.insert(0, "كغ")
        self.product_tva_e.set("0")
        self.product_stamp_e.set("لا")

    def select_product(self):
        values = self.my_tree.item(self.my_tree.focus(), 'values')
        print(values)
        self.clear_entries()
        self.selected_product = values[6]
        print(self.selected_product)
        self.product_name_e.insert(0, values[5])
        self.product_category_e.insert(0, values[4])
        self.product_quantity_e.insert(0, values[3].split(' ')[0].replace(".", ","))
        self.product_price_e.insert(0, values[2])
        self.product_tva_e.set(values[1].split(' ')[1])
        self.product_stamp_e.set(values[0])

    def add_product(self):
        errors = self.validation()
        if errors:
            messagebox.showerror("خطأ", "\n".join(errors), parent=self.parent)
        else:
            if any(product[1] == self.product_name_e.get() and product[2] == self.product_category_e.get() for product
                   in self.data):
                messagebox.showwarning("تحذير", "السلعة بالاسم والنوع المدخلين موجودة بالفعل في قاعدة البيانات",
                                       parent=self.parent)
            else:
                data = {
                    "name": self.product_name_e.get(),
                    "category": self.product_category_e.get(),
                    "price": self.product_price_e.get(),
                    "vat_tax": self.product_tva_e.get(),
                    "stamp_tax": self.product_stamp_e.get(),
                    "available_quantity": self.product_quantity_e.get().replace(",", "."),
                    "unit": self.product_unit_e.get()
                }
                msg = db.add_product(data)
                if msg.startswith("تم"):
                    self.my_tree.delete(*self.my_tree.get_children())
                    self.data = db.get_products()

                    # Insert the updated data into the Treeview
                    for product in self.data:
                        self.my_tree.insert(parent='', index='end', text='', values=(
                            product[5], f"% {product[4]}", product[3],
                            f"{str(product[6]).replace(".", ",")} {product[7]}",
                            product[2], product[1], product[0]))

                    self.clear_entries()

                    messagebox.showinfo("", msg)
                else:
                    messagebox.showerror("", msg)

    def update_product(self):
        errors = self.validation()
        if errors:
            messagebox.showerror("خطأ", "\n".join(errors), parent=self.parent)
        else:
            if any(str(product[0]) == self.selected_product for product in self.data):
                data = {
                    "name": self.product_name_e.get(),
                    "category": self.product_category_e.get(),
                    "price": self.product_price_e.get(),
                    "vat_tax": self.product_tva_e.get(),
                    "stamp_tax": self.product_stamp_e.get(),
                    "available_quantity": self.product_quantity_e.get().replace(",", "."),
                    "unit": self.product_unit_e.get(),
                    "id": self.selected_product
                }
                msg = db.update_product(data)
                if msg.startswith("تم"):
                    self.my_tree.delete(*self.my_tree.get_children())
                    self.data = db.get_products()

                    # Insert the updated data into the Treeview
                    for product in self.data:
                        self.my_tree.insert(parent='', index='end', text='', values=(
                            product[5], f"% {product[4]}", product[3],
                            f"{str(product[6]).replace(".", ",")} {product[7]}",
                            product[2], product[1], product[0]))

                    self.clear_entries()

                    messagebox.showinfo("", msg)
                else:
                    messagebox.showerror("", msg)
            else:
                messagebox.showerror("خطأ", "هذه السلعة لا توجد في قاعدة البيانات", parent=self.parent)


class Customers:
    def __init__(self, parent, data):
        self.customer_name_e = None
        self.customer_lastname_e = None
        self.customer_phone_e = None
        self.customer_address_e = None
        self.customer_reg_id_e = None
        self.customer_tax_item_e = None
        self.customer_tax_num_e = None
        self.customer_statistical_id_e = None
        self.data = data
        self.my_tree = None
        self.selected_customer = None
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self.setup_ui()

    def setup_ui(self):
        tree_frame = ttk.Frame(self.frame)
        tree_frame.pack(fill=tk.X, expand=True, padx=20, pady=5)

        self.my_tree = ttk.Treeview(tree_frame, selectmode="extended", height=5)
        self.my_tree.pack(side=tk.RIGHT, fill=tk.X, expand=True)

        scroll_frame = ttk.Frame(tree_frame)
        scroll_frame.pack(side=tk.RIGHT, fill=tk.Y)

        tree_scroll = ttk.Scrollbar(scroll_frame, orient="vertical", command=self.my_tree.yview)
        tree_scroll.pack(side=tk.LEFT, fill="y")

        self.my_tree.config(yscrollcommand=tree_scroll.set)

        cols = (
            "stat_id", "tax_item_num", "tax_num", "commercial_register_number", "address", "phone", "lname", "name",
            "id")
        self.my_tree['columns'] = cols

        self.my_tree.column("#0", width=0, stretch=tk.NO)
        self.my_tree.column("id", width=0, stretch=tk.NO)
        self.my_tree.column("name", anchor=tk.CENTER)
        self.my_tree.column("lname", anchor=tk.CENTER)
        self.my_tree.column("phone", anchor=tk.CENTER)
        self.my_tree.column("address", anchor=tk.CENTER)
        self.my_tree.column("commercial_register_number", anchor=tk.CENTER)
        self.my_tree.column("tax_num", width=0, stretch=tk.NO)
        self.my_tree.column("tax_item_num", width=0, stretch=tk.NO)
        self.my_tree.column("stat_id", width=0, stretch=tk.NO)

        self.my_tree.heading("#0", text="", anchor=tk.W)
        self.my_tree.heading("name", anchor=tk.CENTER, text="الاسم")
        self.my_tree.heading("lname", anchor=tk.CENTER, text="اللقب")
        self.my_tree.heading("phone", anchor=tk.CENTER, text="رقم الهاتف")
        self.my_tree.heading("address", anchor=tk.CENTER, text="العنوان")
        self.my_tree.heading("commercial_register_number", anchor=tk.CENTER, text="رقم السجل التجاري")
        self.my_tree.bind('<ButtonRelease-1>',
                          lambda event: self.select_customer()
                          if self.my_tree.identify_region(event.x, event.y) != "heading" else None)
        # self.my_tree.bind('<Motion>', 'break')

        for record in self.data:
            self.my_tree.insert(parent='', index='end', text='',
                                values=(record[8], record[7], record[6], record[5], record[4],
                                        record[3] if record[3] != '' else "غير متوفر", record[2], record[1], record[0]))

        data_frame = ttk.LabelFrame(self.frame, text="", labelanchor=tk.NE)
        data_frame.pack(fill="x", expand=True, padx=20, pady=5)

        data_frame.grid_columnconfigure(0, weight=1)
        data_frame.grid_columnconfigure(1, weight=1)
        data_frame.grid_columnconfigure(2, weight=1)
        data_frame.grid_columnconfigure(3, weight=1)

        customer_name_l = ttk.Label(data_frame, text="الاسم")
        self.customer_name_e = ttk.Entry(data_frame, font=normal_text, justify="right")
        customer_name_l.grid(row=0, column=3, padx=10, pady=10)
        self.customer_name_e.grid(row=0, column=2, padx=10, pady=10)

        customer_lastname_l = ttk.Label(data_frame, text="اللقب")
        self.customer_lastname_e = ttk.Entry(data_frame, font=normal_text, justify="right")
        customer_lastname_l.grid(row=0, column=1, padx=10, pady=10)
        self.customer_lastname_e.grid(row=0, column=0, padx=10, pady=10)

        customer_phone_l = ttk.Label(data_frame, text="رقم الهاتف (اختياري)")
        self.customer_phone_e = ttk.Entry(data_frame, font=normal_text, justify="center")
        customer_phone_l.grid(row=1, column=3, padx=10, pady=10)
        self.customer_phone_e.grid(row=1, column=2, padx=10, pady=10)

        customer_address_l = ttk.Label(data_frame, text="العنوان")
        self.customer_address_e = ttk.Entry(data_frame, font=normal_text, justify="right")
        customer_address_l.grid(row=1, column=1, padx=10, pady=10)
        self.customer_address_e.grid(row=1, column=0, padx=10, pady=10)

        customer_reg_id_l = ttk.Label(data_frame, text="رقم السجل (بالفرنسية)")
        self.customer_reg_id_e = ttk.Entry(data_frame, font=normal_text, justify="center")
        customer_reg_id_l.grid(row=2, column=3, padx=10, pady=10)
        self.customer_reg_id_e.grid(row=2, column=2, padx=10, pady=10)

        customer_tax_num_l = ttk.Label(data_frame, text="الرقم الجبائي")
        self.customer_tax_num_e = ttk.Entry(data_frame, font=normal_text, justify="center")
        customer_tax_num_l.grid(row=2, column=1, padx=10, pady=10)
        self.customer_tax_num_e.grid(row=2, column=0, padx=10, pady=10)

        customer_tax_item_l = ttk.Label(data_frame, text="رقم مادة الضرائب")
        self.customer_tax_item_e = ttk.Entry(data_frame, font=normal_text, justify="center")
        customer_tax_item_l.grid(row=3, column=3, padx=10, pady=10)
        self.customer_tax_item_e.grid(row=3, column=2, padx=10, pady=10)

        customer_statistical_id_l = ttk.Label(data_frame, text="رقم التعريف الاحصائي")
        self.customer_statistical_id_e = ttk.Entry(data_frame, font=normal_text, justify="center")
        customer_statistical_id_l.grid(row=3, column=1, padx=10, pady=10)
        self.customer_statistical_id_e.grid(row=3, column=0, padx=10, pady=10)

        buttons_frame = ttk.LabelFrame(self.frame, text="", labelanchor=tk.NE)
        buttons_frame.pack(fill="x", expand=tk.YES, padx=20)

        remove_button = ttk.Button(buttons_frame, text="حذف زبون", style="danger.TButton")
        remove_button.grid(row=0, column=0, padx=10, pady=10)

        update_button = ttk.Button(buttons_frame, text="تحديث زبون", style="warning.TButton",
                                   command=self.update_customer)
        update_button.grid(row=0, column=1, padx=10, pady=10)

        add_button = ttk.Button(buttons_frame, text="إضافة زبون", style="success.TButton", command=self.add_customer)
        add_button.grid(row=0, column=2, padx=10, pady=10)

        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)
        buttons_frame.grid_columnconfigure(2, weight=1)

    def validation(self):
        errors = []
        if not help.is_arabic(self.customer_name_e.get()):
            errors.append("اسم الزبون يجب أن يكون باللغة العربية")
        if not help.is_arabic(self.customer_lastname_e.get()):
            errors.append("لقب الزبون يجب أن يكون باللغة العربية")
        if not help.is_phone_number(self.customer_phone_e.get()):
            errors.append("تأكد من أن رقم الهاتف صحيح")
        if not help.is_number(self.customer_tax_num_e.get()):
            errors.append("الرقم الجبائي يجب أن يتكون من أرقام فقط")
        if not help.is_number(self.customer_tax_item_e.get()):
            errors.append("رقم مادة الضرائب يجب أن يتكون من أرقام فقط")
        if not help.is_number(self.customer_statistical_id_e.get()):
            errors.append("رقم التعريف الاحصائي يجب أن يتكون من أرقام فقط")
        return errors

    def clear_entries(self):
        self.selected_customer = None
        self.customer_name_e.delete(0, tk.END)
        self.customer_lastname_e.delete(0, tk.END)
        self.customer_phone_e.delete(0, tk.END)
        self.customer_address_e.delete(0, tk.END)
        self.customer_reg_id_e.delete(0, tk.END)
        self.customer_tax_num_e.delete(0, tk.END)
        self.customer_tax_item_e.delete(0, tk.END)
        self.customer_statistical_id_e.delete(0, tk.END)

    def select_customer(self):
        values = self.my_tree.item(self.my_tree.focus(), 'values')
        print(values)
        self.clear_entries()
        self.selected_customer = values[8]
        print(self.selected_customer)
        self.customer_name_e.insert(0, values[7])
        self.customer_lastname_e.insert(0, values[6])
        self.customer_phone_e.insert(0, values[5] if values[5] != "غير متوفر" else "")
        self.customer_address_e.insert(0, values[4])
        self.customer_reg_id_e.insert(0, values[3])
        self.customer_tax_num_e.insert(0, values[2])
        self.customer_tax_item_e.insert(0, values[1])
        self.customer_statistical_id_e.insert(0, values[0])

    def add_customer(self):
        errors = self.validation()
        if errors:
            messagebox.showerror("خطأ", "\n".join(errors), parent=self.parent)
        else:
            if any(customer[5] == self.customer_reg_id_e.get() for customer in self.data):
                messagebox.showwarning("تحذير", "تأكد من رقم السجل لأنه موجود في قاعدة البيانات", parent=self.parent)
            else:
                data = {
                    "name": self.customer_name_e.get(),
                    "last_name": self.customer_lastname_e.get(),
                    "phone": self.customer_phone_e.get(),
                    "address": self.customer_address_e.get(),
                    "commercial_register_number": self.customer_reg_id_e.get(),
                    "tax_number": self.customer_tax_num_e.get(),
                    "tax_item_number": self.customer_tax_item_e.get(),
                    "statistical_id": self.customer_statistical_id_e.get()
                }
                msg = db.add_customer(data)
                if msg.startswith("تم"):
                    self.my_tree.delete(*self.my_tree.get_children())
                    self.data = db.get_customers()

                    # Insert the updated data into the Treeview
                    for customer in self.data:
                        self.my_tree.insert(parent='', index='end', text='',
                                            values=(customer[8], customer[7], customer[6], customer[5], customer[4],
                                                    customer[3] if customer[3] != '' else "غير متوفر", customer[2],
                                                    customer[1], customer[0]))

                    self.clear_entries()

                    messagebox.showinfo("", msg)
                else:
                    messagebox.showerror("", msg)

    def update_customer(self):
        errors = self.validation()
        if errors:
            messagebox.showerror("خطأ", "\n".join(errors), parent=self.parent)
        else:
            if any(str(customer[0]) == self.selected_customer for customer in self.data):
                data = {
                    "name": self.customer_name_e.get(),
                    "last_name": self.customer_lastname_e.get(),
                    "phone": self.customer_phone_e.get(),
                    "address": self.customer_address_e.get(),
                    "commercial_register_number": self.customer_reg_id_e.get(),
                    "tax_number": self.customer_tax_num_e.get(),
                    "tax_item_number": self.customer_tax_item_e.get(),
                    "statistical_id": self.customer_statistical_id_e.get(),
                    "id": self.selected_customer
                }
                msg = db.update_customer(data)
                if msg.startswith("تم"):
                    self.my_tree.delete(*self.my_tree.get_children())
                    self.data = db.get_customers()

                    # Insert the updated data into the Treeview
                    for customer in self.data:
                        self.my_tree.insert(parent='', index='end', text='',
                                            values=(customer[8], customer[7], customer[6], customer[5], customer[4],
                                                    customer[3] if customer[3] != '' else "غير متوفر", customer[2],
                                                    customer[1], customer[0]))

                    self.clear_entries()

                    messagebox.showinfo("", msg)
                else:
                    messagebox.showerror("", msg)
            else:
                messagebox.showerror("خطأ", "هذا الزبون لا يوجد في قاعدة البيانات", parent=self.parent)


class Bills:
    def __init__(self, parent, data):
        self.checkbox = tk.IntVar()
        self.data = data
        self.my_tree = None
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self.setup_ui()

    def setup_ui(self):
        tree_frame = ttk.Frame(self.frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)

        checkbox = ttk.Checkbutton(tree_frame, text="إظهار الفواتير التي لم يتم دفعها فقط", command=self.filter_results,
                                   variable=self.checkbox)
        checkbox.pack(padx=20, pady=10)

        cal = DateEntry(tree_frame, justify="center", background='black', foreground='white', borderwidth=1,
                        font=normal_text, showweeknumbers=False, showothermonthdays=False, selectbackground='red',
                        date_pattern="YYYY-mm-dd", firstweekday="sunday", locale="ar_DZ", weekenddays=[6, 7],
                        )
        cal.pack(padx=10, pady=10)

        self.my_tree = ttk.Treeview(tree_frame, selectmode="extended")
        self.my_tree.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        scroll_frame = ttk.Frame(tree_frame)
        scroll_frame.pack(side=tk.RIGHT, fill=tk.Y)

        tree_scroll = ttk.Scrollbar(scroll_frame, orient="vertical", command=self.my_tree.yview)
        tree_scroll.pack(side=tk.LEFT, fill="y")

        self.my_tree.config(yscrollcommand=tree_scroll.set)

        cols = ("state", "price", "date", "customer", "number", "id")
        self.my_tree['columns'] = cols

        self.my_tree.column("#0", width=0, stretch=tk.NO)
        self.my_tree.column("id", width=0, stretch=tk.NO)
        self.my_tree.column("number", anchor=tk.CENTER)
        self.my_tree.column("customer", anchor=tk.CENTER)
        self.my_tree.column("date", anchor=tk.CENTER)
        self.my_tree.column("price", anchor=tk.CENTER)
        self.my_tree.column("state", anchor=tk.CENTER)

        self.my_tree.heading("#0", text="", anchor=tk.W)
        self.my_tree.heading("number", anchor=tk.CENTER, text="الرقم")
        self.my_tree.heading("customer", anchor=tk.CENTER, text="الزبون")
        self.my_tree.heading("date", anchor=tk.CENTER, text="التاريخ")
        self.my_tree.heading("price", anchor=tk.CENTER, text="السعر الاجمالي")
        self.my_tree.heading("state", anchor=tk.CENTER, text="الحالة")
        self.my_tree.bind('<ButtonRelease-1>',
                          lambda event: self.select_customer()
                          if self.my_tree.identify_region(event.x, event.y) != "heading" else None)
        # self.my_tree.bind('<Motion>', 'break')

        for record in self.data:
            self.my_tree.insert(parent='', index='end', text='',
                                values=(record[8], record[7], record[6], record[5], record[4],
                                        record[3] if record[3] != '' else "غير متوفر", record[2], record[1], record[0]))

    def filter_results(self):
        print(self.checkbox.get())


if __name__ == "__main__":
    windll.shcore.SetProcessDpiAwareness(1)
    # Set locale to Arabic (Algerian)
    locale.setlocale(locale.LC_ALL, 'ar_DZ.UTF-8')

    heading = ("Segoe UI", 16, "bold")
    bold_text = ('Segoe UI', 12, 'bold')
    normal_text = ('Segoe UI', 12, 'normal')
    label_text = ('Segoe UI', 11, 'bold')

    # Database
    db = database.Database()
    db.create_tables()

    products = db.get_products()
    customers = db.get_customers()
    bills = db.get_orders()

    print(customers)

    root = tk.Tk()
    root.geometry("1280x800")
    root.minsize(1000, 700)
    root.title("نظام الفواتير")

    root.option_add('*Ttk*direction', 'rtl')  # تعيين الاتجاه لجميع عناصر ttk

    sv_ttk.set_theme("light")

    style = ttk.Style()

    style.configure('TButton', font=bold_text)
    style.configure('Treeview', font=normal_text, rowheight=40)
    style.configure('Treeview.Heading', font=bold_text, rowheight=50)
    style.configure('TLabel', font=label_text)
    style.configure('TCombobox', justify='right')
    style.configure('TCheckbutton', font=label_text)
    style.configure('TNotebook', tabposition='ne')
    style.configure('TNotebook.Tab', font=heading)
    style.configure('danger.TButton', font=bold_text, foreground="#b53737")
    style.configure('success.TButton', font=bold_text, foreground="#008080")
    style.configure('warning.TButton', font=bold_text, foreground="#ca562c")

    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH)

    products_frame = Products(notebook, products)
    customers_frame = Customers(notebook, customers)
    bills_frame = Bills(notebook, bills)

    # Add the instance of ProductManagementApp frame to the Notebook
    notebook.add(bills_frame.frame, text="الفواتير")
    notebook.add(products_frame.frame, text="السلع")
    notebook.add(customers_frame.frame, text="الزبائن")
    notebook.add(ttk.Frame(notebook), text="طلب جديد")

    notebook.select(3)

    root.mainloop()
