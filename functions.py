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
            "Food": [("Burger", "$5.99"), ("Pizza", "$8.99"), ("Fries", "$2.99"), ("Soda", "$1.99"), ("Beef", "$30.00"), ("Salmon", "$20.00")],
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
            # Ensure price is a float
            item_price = float(price.strip("$"))  # Convert price to float if it's a string
            total_item_price = item_price  # Start with the base price

            # Add add-ons price if any
            if addons:
                for addon_name, addon_price in addons:
                    total_item_price += float(addon_price)  # Add add-on price to the base price

            # Multiply by quantity
            total_item_price *= quantity

            # Append the item to the order
            self.order.append((item_name, total_item_price, quantity, addons))
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
            # Ensure prices are displayed consistently
            return [(None, item, f"${float(price.strip('$').split('/')[0]):.2f}") for item, price in items]
        except Exception as e:
            print(f"Error in display_items: {e}")
            return []

