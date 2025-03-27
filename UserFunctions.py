import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import Style
from ttkbootstrap.dialogs import Messagebox
from PIL import Image, ImageTk
from UserData import DataUser
import os


class FunctionUser:
    def __init__(self):
        self.order = []
        self.total_price = 0.0
        self.data_user = DataUser()
        self.categories = self.data_user.get_categories()

    def login(self, username, password):
        try:
            user_credentials = self.data_user.user_credentials
            if username in user_credentials and user_credentials[username] == password:
                return True
            else:
                Messagebox.show_error("Invalid credentials!", "Login Error")
                return False
        except Exception as e:
            Messagebox.show_error(f"Error in login: {e}", "Login Error")
            print(f"Error in login: {e}")

    def add_to_order(self, item_name, total_price, quantity=1, addons=None):
        """Add selected item with quantity and add-ons to order summary."""
        try:
            # Append the item to the order
            self.order.append((item_name, total_price, quantity, addons or []))  # Ensure addons is a list
            self.total_price += total_price  # Update the total price
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
                    receipt_text += f"   ➜ {addon}: ${float(addon_price):.2f}\n"  # Ensure addon_price is formatted

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

