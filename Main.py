import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import Style
from ttkbootstrap.dialogs import Messagebox
from PIL import Image, ImageTk
import os


class OrderingSystemLogic:
    def __init__(self):
        self.order = []
        self.total_price = 0.0
        self.categories = {
            "Food": [("Burger", "$5.99"), ("Pizza", "$8.99"), ("Fries", "$2.99"), ("Soda", "$1.99"), ("Beef", "$30"), ("Salmon", "$20")],
            "Beverages": [("Coffee", "$3.99"), ("Tea", "$2.49"), ("Juice", "$4.99"), ("Milk", "$2.99")],
            "Household Essentials": [("Detergent", "$6.99"), ("Tissues", "$3.49"), ("Broom", "$8.99"), ("Sponge", "$2.49")],
            "Fresh Produce": [("Apples", "$2.99/lb"), ("Bananas", "$1.49/lb"), ("Carrots", "$1.99/lb"), ("Lettuce", "$1.79")],
            "Meat, Poultry & Seafood": [("Chicken Breast", "$5.99/lb"), ("Beef Steak", "$12.99/lb"), ("Salmon", "$15.99/lb"), ("Pork Chops", "$6.99/lb")],
            "Dairy & Eggs": [("Milk", "$3.49"), ("Cheddar Cheese", "$4.99"), ("Yogurt", "$1.29"), ("Eggs", "$2.99/dozen")],
            "Bakery": [("White Bread", "$2.49"), ("Croissant", "$1.99"), ("Chocolate Cake", "$9.99"), ("Muffins", "$3.99")],
            "Pantry Staples": [("Rice", "$3.99/5lb"), ("Pasta", "$1.99"), ("Tomato Sauce", "$2.49"), ("Cooking Oil", "$6.99")],
            "Frozen Foods": [("Frozen Vegetables", "$4.99"), ("Frozen Pizza", "$7.99"), ("Ice Cream", "$5.99"), ("Frozen Chicken Nuggets", "$8.49")],
            "Snacks & Sweets": [("Chips", "$2.99"), ("Chocolate Bar", "$1.99"), ("Popcorn", "$3.49"), ("Trail Mix", "$4.99")],
            "Household & Cleaning Products": [("Laundry Detergent", "$9.99"), ("Dishwashing Liquid", "$4.99"), ("Paper Towels", "$5.49"), ("Disinfectant Wipes", "$6.99")],
            "Personal Care & Health": [("Toothpaste", "$3.49"), ("Shampoo", "$6.99"), ("Hand Soap", "$2.99"), ("Pain Reliever", "$7.99")],
            "Baby & Pet Supplies": [("Baby Formula", "$19.99"), ("Diapers", "$14.99"), ("Dog Food", "$24.99"), ("Cat Litter", "$10.99")],
            "Alcohol & Tobacco": [("Beer", "$8.99/6-pack"), ("Wine", "$12.99/bottle"), ("Whiskey", "$29.99/bottle"), ("Cigarettes", "$10.99/pack")]
        }

    def add_to_order(self, item_name, price, quantity=1, addons=None):
        """Add selected item with quantity and add-ons to order summary."""
        try:
            item_price = float(price.strip("$").split("/")[0])  # Extract numeric value
            total_item_price = item_price * quantity

            if addons:
                for addon_name, addon_price in addons:
                    total_item_price += float(addon_price) * quantity

            self.order.append((item_name, total_item_price, quantity, addons))  # Include quantity
            self.total_price += total_item_price
        except Exception as e:
            print(f"Error in add_to_order: {e}")

    def delete_order(self, index):
        """Remove selected item from order summary."""
        try:
            if 0 <= index < len(self.order):
                _, item_price, _, _ = self.order.pop(index)
                self.total_price -= item_price
        except Exception as e:
            print(f"Error in delete_order: {e}")

    def clear_order(self):
        """Clear all selected items and reset total price."""
        self.order.clear()
        self.total_price = 0.0

    def checkout(self):
        """Calculate total price and process checkout."""
        if not self.order:
            Messagebox.show_error("Your cart is empty!", "Checkout Error")
            return

        receipt_text = "🛒 Supermarket Receipt\n\n"
        for item, price, quantity, addons in self.order:
            receipt_text += f"{item} (x{quantity}): ${price:.2f}\n"
            if addons:
                for addon, addon_price in addons:
                    receipt_text += f"   ➜ {addon}: ${addon_price:.2f}\n"

        receipt_text += f"\nTotal: ${self.total_price:.2f}"
        Messagebox.show_info(receipt_text, "Checkout Complete")

    def save_receipt(self):
        """Save the receipt to a file."""
        if not self.order:
            Messagebox.show_error("No order to save!", "Error")
            return

        try:
            with open("receipt.txt", "w", encoding="utf-8") as file:
                file.write("🛒 Supermarket Receipt\n\n")
                for item, price, quantity, addons in self.order:
                    file.write(f"{item} (x{quantity}): ${price:.2f}\n")
                    if addons:
                        for addon, addon_price in addons:
                            file.write(f"   ➜ {addon}: ${addon_price:.2f}\n")

                file.write(f"\nTotal: ${self.total_price:.2f}")

            Messagebox.show_info("Receipt saved successfully!", "Success")
        except Exception as e:
            Messagebox.show_error(f"Error saving receipt: {e}", "Error")

    def display_items(self, category):
        """Dynamically display items with images, names, and prices."""
        try:
            items = self.categories.get(category, [])
            return [(None, item, price) for item, price in items]  # Placeholder for images
        except Exception as e:
            print(f"Error in display_items: {e}")
            return []


class OrderingSystemGUI:
    def __init__(self, root):
        self.logic = OrderingSystemLogic()
        self.root = root
        self.root.title("Supermarket Ordering System")
        self.root.geometry("1170x900")
        self.style = Style("litera")

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
        logo_image = Image.open("img/logo.png")
        logo_image = logo_image.resize((100, 100))
        logo_photo = ImageTk.PhotoImage(logo_image)
        self.logo_label = ttk.Label(self.header_frame, image=logo_photo, bootstyle="inverse-dark")
        self.logo_label.image = logo_photo
        self.logo_label.grid(row=0, column=2, padx=10, pady=5, sticky="e")

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
                {"name": "Extra Cheese", "price": 20},
                {"name": "Bacon", "price": 30},
                {"name": "Lettuce", "price": 10},
                {"name": "Tomato", "price": 10},
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
            total_addon_price = 0
            selected_addons = []

            # Process selected add-ons
            for var, addon in addons_var:
                if var.get():  # Check if the add-on is selected
                    total_addon_price += addon['price']
                    selected_addons.append((addon['name'], addon['price']))

            # Calculate final price
            base_price = float(price.strip("$"))
            final_price = (base_price + total_addon_price) * quantity

            # Add item with add-ons to the order
            self.add_to_order(item_name, f"${final_price:.2f}", quantity, selected_addons)
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

        for item, price, quantity, addons in self.logic.order:  # Unpack four elements
            # Format the main item with quantity
            dot_count = total_width - len(item) - len(f"${price:.2f}") - len(f" (x{quantity})")
            dots = "." * max(dot_count, 0)  # Ensure no negative dots
            formatted_item = f"{item} (x{quantity}) {dots} ${price:.2f}"  # Include quantity in the display
            self.summary_listbox.insert(tk.END, formatted_item)

            # Add add-ons below the main item
            if addons:
                for addon_name, addon_price in addons:
                    self.summary_listbox.insert(tk.END, f"   ➜ {addon_name}: ${addon_price:.2f}")

        # Update the total price label
        self.total_price_label.config(text=f"Total: ${self.logic.total_price:.2f}")


if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap("img/Logo.ico")
    app = OrderingSystemGUI(root)
    root.mainloop()

    