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

    def center_popup(self, popup, width, height):
        """Center a popup window on the screen."""
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        popup.geometry(f"{width}x{height}+{x}+{y}")

    def manage_items(self):

        manage_window = tk.Toplevel(self.root)
        manage_window.title("Manage Items")
        self.center_popup(manage_window, 400, 300)  # Center the popup
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
        self.center_popup(add_window, 400, 600)  # Center the popup
        add_window.resizable(False, False)
        ttk.Label(add_window, text="Add New Item", font=("Montserrat", 16)).pack(pady=10)

        # Item name
        ttk.Label(add_window, text="Item Name:", font=("Montserrat", 12)).pack(pady=5)
        item_name_entry = ttk.Entry(add_window, font=("Montserrat", 12))
        item_name_entry.pack(pady=5)

        # Item price
        ttk.Label(add_window, text="Item Price:", font=("Montserrat", 12)).pack(pady=5)
        item_price_entry = ttk.Entry(add_window, font=("Montserrat", 12))
        item_price_entry.pack(pady=5)

        # Category (Combobox)
        ttk.Label(add_window, text="Category:", font=("Montserrat", 12)).pack(pady=5)
        category_combobox = ttk.Combobox(add_window, font=("Montserrat", 12), state="readonly")
        category_combobox.pack(pady=5)

        # Load categories from items.json
        try:
            with open("items.json", "r") as file:
                items_data = json.load(file)
                categories = list(items_data.keys())
                category_combobox["values"] = categories
        except FileNotFoundError:
            categories = []
            category_combobox["values"] = categories

        # Upload image
        ttk.Label(add_window, text="Upload Image:", font=("Montserrat", 12)).pack(pady=5)
        image_path_label = ttk.Entry(add_window, font=("Montserrat", 12))
        image_path_label.pack(pady=5)

        def upload_image():
            file_path = filedialog.askopenfilename(title="Select an image", filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
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
                category_combobox.get().strip(),
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
        
        category = category.strip().title()

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
        update_window = tk.Toplevel(self.root)
        update_window.title("Update Item")
        self.center_popup(update_window, 400, 600)  # Center the popup
        update_window.resizable(False, False)

        ttk.Label(update_window, text="Update Item", font=("Montserrat", 16)).pack(pady=10)
        category_combobox = ttk.Combobox(update_window, font=("Montserrat", 12))
        category_combobox.pack(pady=5)

        try:
            with open("JSON/items.json", "r") as file:  # Updated path
                items_data = json.load(file)
                categories = list(items_data.keys())
                category_combobox["values"] = categories
        except FileNotFoundError:
            Messagebox.show_error("Error", "No items found!")
            return

        ttk.Label(update_window, text="Select Item:", font=("Montserrat", 12)).pack(pady=5)
        item_combobox = ttk.Combobox(update_window, font=("Montserrat", 12), state="readonly")
        item_combobox.pack(pady=5)

        def load_items(event):
            selected_category = category_combobox.get()
            if selected_category in items_data:
                items = [item["name"] for item in items_data[selected_category]]
                item_combobox["values"] = items

        category_combobox.bind("<<ComboboxSelected>>", load_items)

        ttk.Label(update_window, text="Item Name:", font=("Montserrat", 12)).pack(pady=5)
        item_name_entry = ttk.Entry(update_window, font=("Montserrat", 12))
        item_name_entry.pack(pady=5)

        ttk.Label(update_window, text="Item Price:", font=("Montserrat", 12)).pack(pady=5)
        item_price_entry = ttk.Entry(update_window, font=("Montserrat", 12))
        item_price_entry.pack(pady=5)

        ttk.Label(update_window, text="Upload New Image:", font=("Montserrat", 12)).pack(pady=5)
        image_path_label = ttk.Entry(update_window, font=("Montserrat", 12))
        image_path_label.pack(pady=5)

        def upload_image():
            file_path = filedialog.askopenfilename(title="Select an image", filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
            if file_path:
                image_path_label.delete(0, tk.END)
                image_path_label.insert(0, file_path)

        upload_button = ttk.Button(update_window, text="Upload", command=upload_image, bootstyle="primary")
        upload_button.pack(pady=5)

        def load_item_details(event):
            selected_category = category_combobox.get()
            selected_item = item_combobox.get()
            if selected_category in items_data:
                for item in items_data[selected_category]:
                    if item["name"] == selected_item:
                        item_name_entry.delete(0, tk.END)
                        item_name_entry.insert(0, item["name"])
                        item_price_entry.delete(0, tk.END)
                        item_price_entry.insert(0, item["price"])
                        image_path_label.delete(0, tk.END)
                        image_path_label.insert(0, item["image"])
                        break

        item_combobox.bind("<<ComboboxSelected>>", load_item_details)

        def save_updated_item():
            selected_category = category_combobox.get()
            selected_item = item_combobox.get()
            new_name = item_name_entry.get().strip()
            new_price = item_price_entry.get().strip()
            new_image_path = image_path_label.get().strip()

            if not selected_category or not selected_item or not new_name or not new_price or not new_image_path:
                Messagebox.show_error("Error", "All fields are required!")
                return

            try:
                new_price = float(new_price)
            except ValueError:
                Messagebox.show_error("Error", "Price must be a valid number!")
                return

            for item in items_data[selected_category]:
                if item["name"] == selected_item:
                    item["name"] = new_name
                    item["price"] = new_price
                    if new_image_path:
                        image_filename = os.path.basename(new_image_path)
                        image_destination = os.path.join("img", image_filename)
                        os.makedirs("img", exist_ok=True)
                        with open(new_image_path, "rb") as src, open(image_destination, "wb") as dest:
                            dest.write(src.read())
                        item["image"] = image_destination
                    break

            with open("JSON/items.json", "w") as file:  # Updated path
                json.dump(items_data, file, indent=4)

            Messagebox.show_info("Success", f"Item '{selected_item}' updated successfully!")
            update_window.destroy()

        save_button = ttk.Button(update_window, text="Save Changes", command=save_updated_item, bootstyle="success")
        save_button.pack(pady=20)

    def delete_item(self):
        delete_window = tk.Toplevel(self.root)
        delete_window.title("Delete Item")
        self.center_popup(delete_window, 400, 300)  # Center the popup
        delete_window.resizable(False, False)

        ttk.Label(delete_window, text="Delete Item", font=("Montserrat", 16)).pack(pady=10)

        category_combobox = ttk.Combobox(delete_window, font=("Montserrat", 12))
        category_combobox.pack(pady=5)

        try:
            with open("items.json", "r") as file:
                items_data = json.load(file)
                categories = list(items_data.keys())
                category_combobox["values"] = categories
        except FileNotFoundError:
            Messagebox.show_error("Error", "No items found!")
            return

        ttk.Label(delete_window, text="Select Item:", font=("Montserrat", 12)).pack(pady=5)
        item_combobox = ttk.Combobox(delete_window, font=("Montserrat", 12), state="readonly")
        item_combobox.pack(pady=5)

        def load_items(event):
            selected_category = category_combobox.get()
            if selected_category in items_data:
                items = [item["name"] for item in items_data[selected_category]]
                item_combobox["values"] = items

        category_combobox.bind("<<ComboboxSelected>>", load_items)

        def delete_selected_item():
            selected_category = category_combobox.get()
            selected_item = item_combobox.get()

            if not selected_category or not selected_item:
                Messagebox.show_error("Error", "Please select a category and an item to delete!")
                return

            for item in items_data[selected_category]:
                if item["name"] == selected_item:
                    items_data[selected_category].remove(item)
                    break

            with open("items.json", "w") as file:
                json.dump(items_data, file, indent=4)

            Messagebox.show_info("Success", f"Item '{selected_item}' deleted successfully!")
            delete_window.destroy()

        delete_button = ttk.Button(delete_window, text="Delete Item", command=delete_selected_item, bootstyle="danger")
        delete_button.pack(pady=20)

    def manage_users(self):
        manage_users_window = tk.Toplevel(self.root)
        manage_users_window.title("Manage Users")
        self.center_popup(manage_users_window, 400, 400)  # Center the popup
        manage_users_window.resizable(False, False)

        ttk.Label(manage_users_window, text="Manage Users", font=("Montserrat", 16)).pack(pady=10)

        button_frame = ttk.Frame(manage_users_window)
        button_frame.pack(pady=20)

        add_cashier_button = ttk.Button(button_frame, text="Add Cashier", command=self.add_cashier, bootstyle="primary")
        add_cashier_button.grid(row=0, column=0, padx=20, pady=10)

        remove_cashier_button = ttk.Button(button_frame, text="Remove Cashier", command=self.remove_cashier, bootstyle="danger")
        remove_cashier_button.grid(row=0, column=1, padx=20, pady=10)

    def add_cashier(self):
        add_cashier_window = tk.Toplevel(self.root)
        add_cashier_window.title("Add Cashier")
        self.center_popup(add_cashier_window, 400, 400)  # Center the popup
        add_cashier_window.resizable(False, False)

        ttk.Label(add_cashier_window, text="Add Cashier", font=("Montserrat", 16)).pack(pady=10)

        ttk.Label(add_cashier_window, text="Cashier Name:", font=("Montserrat", 12)).pack(pady=5)
        name_entry = ttk.Entry(add_cashier_window, font=("Montserrat", 12))
        name_entry.pack(pady=5)

        ttk.Label(add_cashier_window, text="Cashier ID:", font=("Montserrat", 12)).pack(pady=5)
        id_entry = ttk.Entry(add_cashier_window, font=("Montserrat", 12))
        id_entry.pack(pady=5)

        ttk.Label(add_cashier_window, text="Username:", font=("Montserrat", 12)).pack(pady=5)
        username_entry = ttk.Entry(add_cashier_window, font=("Montserrat", 12))
        username_entry.pack(pady=5)

        ttk.Label(add_cashier_window, text="Password:", font=("Montserrat", 12)).pack(pady=5)
        password_entry = ttk.Entry(add_cashier_window, font=("Montserrat", 12), show="*")
        password_entry.pack(pady=5)

        def save_cashier():
            name = name_entry.get().strip()
            cashier_id = id_entry.get().strip()
            username = username_entry.get().strip()
            password = password_entry.get().strip()

            if not name or not cashier_id or not username or not password:
                Messagebox.show_error("Error", "All fields are required!")
                return

            cashier_file = "JSON/cashiers.json"  # Updated path
            try:
                with open(cashier_file, "r") as file:
                    cashiers_data = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                cashiers_data = {}  # Initialize if file is missing or invalid

            if cashier_id in cashiers_data:
                Messagebox.show_error("Error", "Cashier ID already exists!")
                return

            cashiers_data[cashier_id] = {"name": name, "username": username, "password": password}

            try:
                with open(cashier_file, "w") as file:
                    json.dump(cashiers_data, file, indent=4)
                Messagebox.show_info("Success", f"Cashier '{name}' added successfully!")
                add_cashier_window.destroy()
            except Exception as e:
                Messagebox.show_error("Error", f"Failed to save cashier: {e}")

        save_button = ttk.Button(add_cashier_window, text="Save", command=save_cashier, bootstyle="success")
        save_button.pack(pady=10)

    def remove_cashier(self):
        remove_cashier_window = tk.Toplevel(self.root)
        remove_cashier_window.title("Remove Cashier")
        self.center_popup(remove_cashier_window, 400, 300)  # Center the popup
        remove_cashier_window.resizable(False, False)

        ttk.Label(remove_cashier_window, text="Remove Cashier", font=("Montserrat", 16)).pack(pady=10)

        # Cashier ID and Name (Combobox)
        ttk.Label(remove_cashier_window, text="Select Cashier:", font=("Montserrat", 12)).pack(pady=5)
        cashier_combobox = ttk.Combobox(remove_cashier_window, font=("Montserrat", 12), state="readonly")
        cashier_combobox.pack(pady=5)

        # Load cashier IDs and names from cashiers.json
        try:
            cashier_file = "JSON/cashiers.json"  # Updated path
            with open(cashier_file, "r") as file:
                cashiers_data = json.load(file)
                cashier_entries = [f"{cashier_id} - {cashier_info['name']}" for cashier_id, cashier_info in cashiers_data.items()]
                cashier_combobox["values"] = cashier_entries
        except FileNotFoundError:
            cashier_entries = []
            cashier_combobox["values"] = cashier_entries

        def delete_cashier():
            selected_entry = cashier_combobox.get().strip()
            if not selected_entry:
                Messagebox.show_error("Error", "Please select a cashier!")
                return

            # Extract the cashier ID from the selected entry
            cashier_id = selected_entry.split(" - ")[0]

            cashier_file = "JSON/cashiers.json"  # Updated path
            try:
                with open(cashier_file, "r") as file:
                    cashiers_data = json.load(file)
            except FileNotFoundError:
                Messagebox.show_error("Error", "No cashiers found!")
                return

            if cashier_id not in cashiers_data:
                Messagebox.show_error("Error", "Cashier ID not found!")
                return

            del cashiers_data[cashier_id]

            with open(cashier_file, "w") as file:
                json.dump(cashiers_data, file, indent=4)

            Messagebox.show_info("Success", f"Cashier with ID '{cashier_id}' removed successfully!")
            remove_cashier_window.destroy()

        delete_button = ttk.Button(remove_cashier_window, text="Delete", command=delete_cashier, bootstyle="danger")
        delete_button.pack(pady=10)

    def view_reports(self):
        """Place Holder for viewing reports"""
        Messagebox.show_info("View Reports", "This feature is under development.")

    def logout(self, root):
        """Logout the admin user."""
        root.destroy()

