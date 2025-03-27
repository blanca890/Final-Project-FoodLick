import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox
from PIL import Image, ImageTk
from ttkbootstrap import Style
import json
from tkinter import filedialog
import os

class FunctionsAdmin:

    def __init__ (self, root):
        self.root = root 

    def manage_items(self):

        manage_window = tk.Toplevel(self.root)
        manage_window.title("Manage Items")
        manage_window.geometry("400x300")
        manage_window.resizable(False, False)

        ttk.Label(manage_window, text="Manage Items", font=("Montserrat", 16)).pack(pady=10)

        button_frame = ttk.Frame(manage_window)
        button_frame.pack(pady=20)

        add_item_button = ttk.Button(button_frame, text="Add Item", command=self.add_item, bootstyle="primary")
        add_item_button.grid(row=0, column=0, padx=20, pady=10)

        update_item_button = ttk.Button(button_frame, text="Update Item", command=self.update_item, bootstyle="primary")
        update_item_button.grid(row=0, column=1, padx=20, pady=10)

        delete_item_button = ttk.Button(button_frame, text="Delete Item", command=self.delete_item, bootstyle="primary")
        delete_item_button.grid(row=0, column=2, padx=20, pady=10)

    def add_item(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Item")
        add_window.geometry("400x600")
        add_window.resizable(False, False)
        ttk.Label(add_window, text="Add New Item", font=("Montserrat", 16)).pack(pady=10)

        #item name
        ttk.Label(add_window, text="Item Name:", font=("Montserrat", 12)).pack(pady=5)
        item_name_entry = ttk.Entry(add_window, font=("Montserrat", 12))
        item_name_entry.pack(pady=5)

        #item price
        ttk.Label(add_window, text="Item Price:", font=("Montserrat", 12)).pack(pady=5)
        item_price_entry = ttk.Entry(add_window, font=("Montserrat", 12))
        item_price_entry.pack(pady=5)

        #Item Category
        ttk.Label(add_window, text="Category:", font=("Montserrat", 12)).pack(pady=5)
        category_entry = ttk.Entry(add_window, font=("Montserrat", 12))
        category_entry.pack(pady=5)

        #upload image
        ttk.Label(add_window, text="Upload Image:", font=("Montserrat", 12)).pack(pady=5)
        image_path_label = ttk.Entry(add_window, font=("Montserrat", 12))
        image_path_label.pack(pady=5)

        def upload_image():
            file_path = filedialog.askopenfilename(title = "Select an image", filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
            if file_path:
                image_path_label.delete(0, tk.END)
                image_path_label.insert(0, file_path)
        
        upload_button = ttk.Button(add_window, text="Upload", command=upload_image, bootstyle="primary")
        upload_button.pack(pady=5)

        save_button = ttk.Button(
            add_window, 
            text="Save Item", 
            command=lambda: self.save_item(
                add_window, 
                item_name_entry.get().strip(), 
                item_price_entry.get().strip(), 
                category_entry.get().strip(), 
                image_path_label.get()
            ), 
            bootstyle="success"
        )
        save_button.pack(pady=10)

    def save_item(self, add_window, item_name, item_price, category, image_path):
        if not item_name or not item_price or not category or image_path == "":
            Messagebox.show_error("Error", "All fields are required!")
            return

        try:
            item_price = float(item_price)
        except ValueError:
            Messagebox.show_error("Error", "Price must be a valid number!")
            return

        self.save_to_json(item_name, item_price, category, image_path)
        self.save_to_addons_json(item_name)

        Messagebox.show_info("Success", f"Item '{item_name}' added successfully!")
        add_window.destroy()

    def save_to_json(self, item_name, item_price, category, image_path):
        item_file = "items.json"
        try:
            with open(item_file, "r") as file:
                items_data = json.load(file)
        except FileNotFoundError:
            items_data = {}

        if category not in items_data:
            items_data[category] = []

        image_filename = os.path.basename(image_path)
        image_destination = os.path.join("img", image_filename)
        os.makedirs("img", exist_ok=True)
        with open(image_path, "rb") as src, open(image_destination, "wb") as dest:
            dest.write(src.read())

        items_data[category].append({"name": item_name, "price": item_price, "image": image_destination})
        with open(item_file, "w") as file:
            json.dump(items_data, file, indent= 4)

    def save_to_addons_json(self, item_name):
        addons_file ="addons.json"
        try:
            with open(addons_file, "r") as file:
                addons_data = json.load(file)
        except FileNotFoundError:
            addons_data = {}

        addons_data[item_name]= [
            {"name": "Extra Cheese", "price":1},
            {"name": "Extra Sauce", "price": 1},
            {"name": "Extra Toppings", "price": 2},
            {"name": "Extra Meat", "price": 3},
            {"name": "Extra Veggies", "price": 2},
        ]

        with open(addons_file, "w") as file:
            json.dump(addons_data, file, indent= 4 )
        
    def update_item(self):
        """Place Holder for updating items"""
        Messagebox.show_info("Update Item", "This feature is under development.")
    def delete_item(self):
        """Place Holder for deleting items"""
        Messagebox.show_info("Delete Item", "This feature is under development.")

    def manage_users(self):
        """Place Holder for managing users"""
        Messagebox.show_info("Manage Users", "This feature is under development.")

    def view_reports(self):
        """Place Holder for viewing reports"""
        Messagebox.show_info("View Reports", "This feature is under development.")

    def logout(self, root):
        """Logout the admin user."""
        root.destroy()

