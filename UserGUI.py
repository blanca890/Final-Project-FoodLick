import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import Style
from ttkbootstrap.dialogs import Messagebox
from PIL import Image, ImageTk
from UserData import DataUser
from UserFunctions import FunctionUser
import os

class LoginScreen:
    def __init__(self, root, style, on_login_success):
        self.root = root
        self.style = style  # Use the shared Style object
        self.on_login_success = on_login_success  # Callback to open the main app
        self.logic = FunctionUser()  # Create an instance of FunctionUser

        self.root.title("Login - Supermarket Ordering System")
        self.root.geometry("400x300")

        self.center_window(400,300)

        # Username Label and Entry
        self.username_label = ttk.Label(self.root, text="Username:", font=("Montserrat", 14))
        self.username_label.pack(pady=10)
        self.username_entry = ttk.Entry(self.root, font=("Montserrat", 14))
        self.username_entry.pack(pady=5)

        # Password Label and Entry
        self.password_label = ttk.Label(self.root, text="Password:", font=("Montserrat", 14))
        self.password_label.pack(pady=10)
        self.password_entry = ttk.Entry(self.root, font=("Montserrat", 14), show="*")
        self.password_entry.pack(pady=5)

        # Login Button
        self.login_button = ttk.Button(self.root, text="Login", command=self.login, bootstyle="primary", padding=10)
        self.login_button.pack(pady=20)
    
    def center_window(self,width,height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        self.root.geometry(f"{width}x{height}+{int(x)}+{int(y)}")


    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check admin credentials first
        from AdminData import DataAdmin
        admin_logic = DataAdmin()
        if admin_logic.validate_admin(username, password):
            Messagebox.show_info("Login successful!", f"Welcome, Admin {username}!")
            self.on_login_success(username, "admin")  # Pass username and role to callback
            return

        # Validate login using FunctionUser for regular users
        if self.logic.login(username, password):
            Messagebox.show_info("Login successful!", f"Welcome, {username}!")
            self.on_login_success(username, "user")  # Pass username and role to callback
        else:
            Messagebox.show_error("Invalid credentials!", "Login Error")

class GUIUser:
    def __init__(self, root, logic):  # Add logic parameter
        self.logic = logic  # Use the passed logic instance
        self.root = root
        self.data_user = DataUser()

        self.root.title("Supermarket Ordering System")
        self.root.geometry("1170x900")
        self.style = Style("litera")

        self.center_window_gui(1170,900)

        # Header Frame
        self.header_frame = ttk.Frame(root, bootstyle="dark")
        self.header_frame.grid(row=0, column=0, columnspan=3, sticky="ew", padx=10, pady=10)

        # Exit Button
        self.exit_button = ttk.Button(self.header_frame, text="Exit", command=root.quit, bootstyle="danger-outline", padding=10)
        self.exit_button.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        # Banner Label
        self.banner_label = ttk.Label(
            self.header_frame,
            text="🛒 Welcome to Supermarket Ordering System!",
            font=("Montserrat", 18, "bold"),
            bootstyle="inverse-dark"
        )
        self.banner_label.grid(row=0, column=1, padx=10, pady=5, sticky="n")
 
        # Logo
        try:
            logo_image = Image.open("img/logo.png")  # Ensure this file exists
            logo_image = logo_image.resize((100, 100))
            logo_photo = ImageTk.PhotoImage(logo_image)
            self.logo_label = ttk.Label(self.header_frame, image=logo_photo, bootstyle="inverse-dark")
            self.logo_label.image = logo_photo
            self.logo_label.grid(row=0, column=2, padx=10, pady=5, sticky="e")
        except Exception as e:
            print(f"Error loading logo: {e}")

        # Main Frame
        self.main_frame = ttk.Frame(root)
        self.main_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        root.rowconfigure(1, weight=1)
        root.columnconfigure(0, weight=1)

        # Sidebar Frame (Category Selection)
        self.sidebar_frame = ttk.Frame(self.main_frame, bootstyle="secondary", padding=10)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.category_label = ttk.Label(self.sidebar_frame, text="📌 Categories", font=("Montserrat", 14, "bold"), bootstyle="inverse-secondary")
        self.category_label.pack(pady=10)

        for category in self.logic.categories.keys():
            btn = ttk.Button(self.sidebar_frame, text=category, bootstyle="success", padding=5, command=lambda c=category: self.update_menu(c))
            btn.pack(fill=tk.X, pady=5)

        # Menu Frame
        self.menu_frame = ttk.Frame(self.main_frame, bootstyle="light", padding=10)
        self.menu_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Order Summary Frame
        self.summary_frame = ttk.Frame(self.main_frame, bootstyle="light", padding=10)
        self.summary_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        # Summary Listbox
        self.summary_listbox = tk.Listbox(self.summary_frame, height=12, font=("Montserrat", 12), relief=tk.SOLID, borderwidth=2)
        self.summary_listbox.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)

        # Total Price Label
        self.total_price_label = ttk.Label(self.summary_frame, text="Total: $0.00", font=("Montserrat", 14, "bold"), bootstyle="inverse-light")
        self.total_price_label.pack(pady=5)

        # Buttons
        self.btn_frame = ttk.Frame(self.summary_frame)
        self.btn_frame.pack(fill=tk.X, pady=5)

        self.discount_button = ttk.Button(self.btn_frame, text="Discount", bootstyle="success-outline", padding=5, command=self.apply_discount)
        self.discount_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.update_button = ttk.Button(self.btn_frame, text="Update", bootstyle="warning-outline", padding=5, command=self.update_menu)
        self.update_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.delete_button = ttk.Button(self.btn_frame, text="Delete", bootstyle="danger-outline", padding=5, command=self.delete_order)
        self.delete_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.clear_button = ttk.Button(self.summary_frame, text="Clear Order", bootstyle="info-outline", padding=5, command=self.clear_order)
        self.clear_button.pack(fill=tk.X, padx=5, pady=5)

        self.checkout_button = ttk.Button(self.summary_frame, text="Checkout", bootstyle="primary-outline", padding=5, command=self.checkout)
        self.checkout_button.pack(fill=tk.X, padx=5, pady=5)

        self.save_receipt_button = ttk.Button(self.summary_frame, text="Save Receipt", bootstyle="success-outline", padding=5, command=self.save_receipt)
        self.save_receipt_button.pack(fill=tk.X, padx=5, pady=5)


    def center_window_gui(self,width,height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width//2) - (width//2)
        y = (screen_height//2) - (height//2)
        self.root.geometry(f"{width}x{height}+{(x)}+{y}")

    def update_menu(self, category):
        """Clear menu & update items based on selected category."""
        self.display_items(category)

    def display_items(self, category):
        """Dynamically display items with images, names, and prices."""
        try:
            self.images = self.logic.display_items(category)
            for widget in self.menu_frame.winfo_children():
                widget.destroy()

            for i, (img, item, price) in enumerate(self.images):
                frame = ttk.Frame(self.menu_frame, bootstyle="info", padding=30)
                frame.grid(row=i // 3, column=i % 3, padx=20, pady=20, sticky="nsew")

                lbl = ttk.Label(frame, image=img)
                lbl.image = img
                lbl.pack()

                text_label = ttk.Label(frame, text=f"{item}\n{price}", font=("Montserrat", 12, "bold"), bootstyle="inverse-info")
                text_label.pack(pady=5)

                # Add a quantity input field
                quantity_label = ttk.Label(frame, text="Quantity:", font=("Montserrat", 10))
                quantity_label.pack()

                quantity_entry = ttk.Entry(frame, font=("Montserrat", 10), width=5)
                quantity_entry.insert(0, "1")  # Default quantity is 1
                quantity_entry.pack()

                btn = ttk.Button(
                    frame,
                    text="Add to Order",
                    bootstyle="success-outline",
                    command=lambda i=item, p=price, q=quantity_entry: self.add_to_order(i, p, int(q.get())),
                )

                if category in {"Food", "Beverages"}:
                    btn = ttk.Button(
                        frame,
                        text="Add to Order",
                        bootstyle="success-outline",
                        command=lambda i=item, p=price, q=quantity_entry: self.open_addons_popup(i, p, int(q.get())),
                    )
                btn.pack(fill=tk.X)
        except Exception as e:
            print(f"Error in display_items: {e}")

    def open_addons_popup(self, item_name, price, quantity):
        """Open a popup window for selecting add-ons."""
        popup = tk.Toplevel(self.root)
        addons_var = []  # Initialize addons_var as an empty list
        popup.title(f"Add-ons for {item_name}")
        popup.geometry("400x300")
        popup.grab_set()

        # Add-ons list
        item_addons = {
            "Burger": [
                {"name": "Extra Cheese", "price": 1},
                {"name": "Bacon", "price": 3},
                {"name": "Lettuce", "price": 0.50},
                {"name": "Tomato", "price": 5},
            ],
            "Pizza": [
                {"name": "Extra Cheese", "price": 25},
                {"name": "Pepperoni", "price": 35},
                {"name": "Mushrooms", "price": 15},
                {"name": "Olives", "price": 10},
            ],
            "Fries": [
                {"name": "Cheese Dip", "price": 15},
                {"name": "Garlic Sauce", "price": 10},
                {"name": "Chili Flakes", "price": 5},
            ],
            "Soda": [
                {"name": "With Ice", "price": 0},
                {"name": "Without Ice", "price": 0},
            ],
            "Beef": [
                {"name": "Peppercorn Sauce", "price": 8.5},
                {"name": "Fried Egg", "price": 12},
                {"name": "Extra Rice", "price": 20},
            ],
            "Salmon": [
                {"name": "Extra Rice", "price": 20},
                {"name": "Lemon Butter Dip", "price": 25},
                {"name": "Avocado Slices", "price": 15},
            ],
            "Coffee": [
                {"name": "Ice Cream", "price": 10},
                {"name": "Sea salt Cream", "price": 16},
                {"name": "Boba", "price": 12.5},
            ],
            "Tea": [
                {"name": "Honey", "price": 14},
                {"name": "Pudding", "price": 10},
                {"name": "Cheese Foam", "price": 16},
            ],
            "Juice": [
                {"name": "Fruit Bits", "price": 15},
                {"name": "Ice Cream", "price": 10},
                {"name": "Ginger Shot", "price": 8},
            ],
            "Milk": [
                {"name": "Oreo Crumbs", "price": 15},
                {"name": "Choco Syrup", "price": 11.5},
                {"name": "Cereal Toppings", "price": 10},
            ],
        }
        addons = item_addons.get(item_name, [])
        ttk.Label(popup, text=f"Select add-ons for {item_name}", font=("Montserrat", 14)).pack(pady=10)
        if addons:
            for addon in addons:
                var = tk.IntVar()
                chk = ttk.Checkbutton(
                    popup,
                    text=f"{addon['name']} (+${addon['price']})",
                    variable=var
                )
                chk.pack(anchor='w', padx=10)  # Use lowercase 'w' for west alignment
                addons_var.append((var, addon))
        else:
            ttk.Label(popup, text="No add-ons available.", font=("Montserrat", 12)).pack(pady=10)

        def confirm_addons():
            selected_addons = []

            # Process selected add-ons
            for var, addon in addons_var:
                if var.get():  # Check if the add-on is selected
                    selected_addons.append((addon['name'], addon['price']))

            # Add item with add-ons to the order
            self.add_to_order(item_name, price, quantity, selected_addons)
            popup.destroy()

        ttk.Button(popup, text="Confirm", command=confirm_addons, bootstyle="success").pack(side=tk.LEFT, pady=10)
        ttk.Button(popup, text="Cancel", command=popup.destroy, bootstyle="danger").pack(side=tk.LEFT, pady=10)

    def add_to_order(self, item_name, price, quantity=1, addons=None):
        """Add selected item to order summary with add-ons."""
        self.logic.add_to_order(item_name, price, quantity, addons)
        self.update_summary()

    def delete_order(self):
        """Remove selected item from order summary."""
        try:
            selected_index = self.summary_listbox.curselection()
            if selected_index:
                index = selected_index[0]
                self.logic.delete_order(index)
                self.update_summary()
            else:
                Messagebox.show_warning("Please select an item to delete!", "Warning")
        except Exception as e:
            print(f"Error in delete_order: {e}")

    def clear_order(self):
        """Clear all selected items and reset total price."""
        self.logic.clear_order()
        self.update_summary()

    def checkout(self):
        """Calculate total price and process checkout."""
        self.logic.checkout()
        self.update_summary()

    def save_receipt(self):
        """Save the receipt to a file."""
        self.logic.save_receipt()
        

    def apply_discount(self):
        """Open a popup to apply a discount code."""
        popup = tk.Toplevel(self.root)
        popup.title("Apply Discount")
        popup.geometry("300x200")
        popup.grab_set()

        # Discount codes dictionary
        discount_codes = {
            'SAVE10': 10,
            'SAVE20': 20,
            'SAVE30': 30,
            'SAVE40': 40,
            'HALFOFF': 50
        }

        # Add a label and entry for the discount code
        ttk.Label(popup, text="Enter Discount Code:", font=("Montserrat", 12)).pack(pady=10)
        discount_entry = ttk.Entry(popup, font=("Montserrat", 12))
        discount_entry.pack(pady=5)

        # Function to validate and apply the discount
        def confirm_discount():
            code = discount_entry.get().strip().upper()
            if code in discount_codes:
                discount = discount_codes[code]
                if 0 < discount <= 100:
                    discount_amount = (discount / 100) * self.logic.total_price
                    self.logic.total_price -= discount_amount
                    self.update_summary()  # Update the summary to reflect the new total
                    Messagebox.show_info(f"Discount applied! {discount}% off.\nNew total: ${self.logic.total_price:.2f}", "Success")
                    popup.destroy()
                else:
                    Messagebox.show_error("Invalid discount percentage.", "Error")
            else:
                Messagebox.show_error("Invalid discount code.", "Error")

        # Add Confirm and Cancel buttons
        ttk.Button(popup, text="Apply", command=confirm_discount, bootstyle="success").pack(side=tk.LEFT, padx=10, pady=10)
        ttk.Button(popup, text="Cancel", command=popup.destroy, bootstyle="danger").pack(side=tk.RIGHT, padx=10, pady=10)


    def update_summary(self):
        """Update the order summary listbox and total price label."""
        self.summary_listbox.delete(0, tk.END)  # Clear listbox
        total_width = 25  # Adjust this width as needed for balance

        for item, item_price, quantity, addons in self.logic.order:
            # Format the main item with quantity
            dot_count = total_width - len(item) - len(f"${item_price:.2f}") - len(f" (x{quantity})")
            dots = "." * max(dot_count, 0)  # Ensure no negative dots
            formatted_item = f"{item} (x{quantity}) {dots} ${item_price:.2f}"  # Use item_price directly
            self.summary_listbox.insert(tk.END, formatted_item)

            # Add add-ons below the main item
            if addons:
                for addon_name, addon_price in addons:
                    self.summary_listbox.insert(tk.END, f"   ➜ {addon_name}: ${addon_price:.2f}")

        # Update the total price label
        self.total_price_label.config(text=f"Total: ${self.logic.total_price:.2f}")
