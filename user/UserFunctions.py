import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import Style
from ttkbootstrap.dialogs import Messagebox
from PIL import Image, ImageTk
from user.UserData import DataUser
import os
import datetime
import json


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

        tax_rate = 0.10  # 10% tax
        vat_rate = 0.12  # 12% VAT
        tax = self.total_price * tax_rate
        vat = self.total_price * vat_rate
        grand_total = self.total_price + tax + vat

        receipt_text = (
            "🛒 Supermarket Receipt\n\n"
            "Store Name: FoodLick Supermarket\n"
            "Contact: support@foodlick.com | +1-800-555-1234\n"
            "----------------------------------------\n"
        )
        for item, price, quantity, addons in self.order:
            receipt_text += f"{item} (x{quantity}): ${price:.2f}\n"
            if addons:
                for addon, addon_price in addons:
                    receipt_text += f"   ➜ {addon}: ${float(addon_price):.2f}\n"

        receipt_text += (
            f"\nSubtotal: ${self.total_price:.2f}\n"
            f"Tax (10%): ${tax:.2f}\n"
            f"VAT (12%): ${vat:.2f}\n"
            f"Grand Total: ${grand_total:.2f}\n"
            "----------------------------------------\n"
            "Thank you for shopping with us!\n"
            "Receipt Validity: 30 days\n"
        )
        Messagebox.show_info(receipt_text, "Checkout Complete")

    def save_receipt(self, username):
        """Save the receipt to a user-specific folder with additional details."""
        if not self.order:
            Messagebox.show_error("No order to save!", "Error")
            return

        try:
            # Load cashier data from cashiers.json
            cashier_file = os.path.join("JSON", "cashiers.json")
            with open(cashier_file, "r") as file:
                cashiers_data = json.load(file)

            # Get the cashier's name based on the username
            cashier_name = None
            for cashier in cashiers_data.values():
                if cashier["username"] == username:
                    cashier_name = cashier["name"]
                    break

            if not cashier_name:
                Messagebox.show_error("Cashier not found!", "Error")
                return

            # Create the user-specific directory
            user_receipts_dir = os.path.join("JSON", "receipts", cashier_name)
            os.makedirs(user_receipts_dir, exist_ok=True)

            # Generate a timestamped filename
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            receipt_filename = f"receipt_{timestamp}.txt"
            receipt_path = os.path.join(user_receipts_dir, receipt_filename)

            # Generate receipt details
            tax_rate = 0.10  # 10% tax
            vat_rate = 0.12  # 12% VAT
            tax = self.total_price * tax_rate
            vat = self.total_price * vat_rate
            grand_total = self.total_price + tax + vat

            # Create receipt content
            receipt_content = (
                "🛒 Supermarket Receipt\n\n"
                f"Store Name: FoodLick Supermarket\n"
                f"Contact: support@foodlick.com | +1-800-555-1234\n"
                f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                "----------------------------------------\n"
            )
            for item, price, quantity, addons in self.order:
                receipt_content += f"Item: {item}\n"
                receipt_content += f"  Quantity: {quantity}\n"
                receipt_content += f"  Base Price: ${price / quantity:.2f}\n"
                if addons:
                    receipt_content += "  Add-ons:\n"
                    for addon_name, addon_price in addons:
                        receipt_content += f"    ➜ {addon_name}: ${addon_price:.2f}\n"
                receipt_content += f"  Total Price: ${price:.2f}\n"
                receipt_content += "-" * 40 + "\n"

            receipt_content += (
                f"\nSubtotal: ${self.total_price:.2f}\n"
                f"Tax (10%): ${tax:.2f}\n"
                f"VAT (12%): ${vat:.2f}\n"
                f"Grand Total: ${grand_total:.2f}\n"
                "----------------------------------------\n"
                "Thank you for shopping with us!\n"
                "Receipt Validity: 30 days\n"
            )

            # Save receipt to file
            with open(receipt_path, "w", encoding="utf-8") as file:
                file.write(receipt_content)

            Messagebox.show_info(f"Receipt saved successfully at {receipt_path}!", "Success")
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

