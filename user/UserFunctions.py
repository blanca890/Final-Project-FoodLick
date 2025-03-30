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
            self.order.append((item_name, total_price, quantity, addons or []))  
            self.total_price += total_price  
        except Exception as e:
            print(f"Error in add_to_order: {e}")

    def delete_order(self, index):
        """Remove selected item from order summary."""
        try:
           
            print(f"Current order before deletion: {self.order}")
            print(f"Index to delete: {index}")

            # Ensure the index is within bounds
            if 0 <= index < len(self.order):
                # Remove the item at the given index
                item_name, item_price, quantity, addons = self.order.pop(index)
                self.total_price -= item_price  #

        
                print(f"Removed item: {item_name}")
                print(f"Updated order: {self.order}")
                print(f"Updated total price: {self.total_price:.2f}")


                Messagebox.show_info(f"Removed {item_name} from the order.", "Item Removed")
            else:

                print(f"Invalid index: {index}")
                Messagebox.show_error("Invalid item selected!", "Error")
        except Exception as e:

            print(f"Error in delete_order: {e}")
            Messagebox.show_error(f"Error in deleting item: {e}", "Error")

    def clear_order(self):
        """Clear all selected items and reset total price."""
        self.order.clear()
        self.total_price = 0.0

    def update_order(self, index, new_quantity, new_addons):
        """Update the quantity and add-ons of an item in the order."""
        try:
            item_name, item_price, old_quantity, old_addons = self.order[index]

            # Recalculate the base price of the item (excluding old add-ons)
            base_price = item_price / old_quantity
            for _, addon_price in old_addons:
                base_price -= addon_price

            # Calculate the new total price for the item
            new_total_price = base_price * new_quantity
            for _, addon_price in new_addons:
                new_total_price += addon_price * new_quantity

            # Update the order
            self.total_price -= item_price  
            self.total_price += new_total_price 
            self.order[index] = (item_name, new_total_price, new_quantity, new_addons)
        except Exception as e:
            print(f"Error in update_order: {e}")

    def checkout(self):
        """Calculate total price and process checkout."""
        if not self.order:
            Messagebox.show_error("Your cart is empty!", "Checkout Error")
            return

        tax_rate = 0.10 
        vat_rate = 0.12 
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

            # Prompt the cashier to input the customer's name
            customer_name = tk.simpledialog.askstring("Customer Name", "Enter the customer's name:")
            if not customer_name:
                Messagebox.show_error("Customer name is required!", "Error")
                return

            # Create the user-specific directory
            user_receipts_dir = os.path.join("JSON", "receipts", username)
            os.makedirs(user_receipts_dir, exist_ok=True)

            # Generate a timestamped filename with the username
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            receipt_filename = f"{username}_sale_receipt_{timestamp}.txt"
            receipt_path = os.path.join(user_receipts_dir, receipt_filename)

            # Generate receipt details
            tax_rate = 0.10  
            vat_rate = 0.12  
            tax = self.total_price * tax_rate
            vat = self.total_price * vat_rate
            grand_total = self.total_price + tax + vat

            # Create receipt content
            receipt_content = (
                "🛒 Supermarket Receipt\n\n"
                f"Store Name: FoodLick Supermarket\n"
                f"Contact: support@foodlick.com | +1-800-555-1234\n"
                f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"Cashier: {cashier_name}\n"
                f"Customer: {customer_name}\n"
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






