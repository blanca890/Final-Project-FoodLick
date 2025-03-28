import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import Style
from ttkbootstrap.dialogs import Messagebox
from PIL import Image, ImageTk
import os
import json


class DataUser:

    
    def __init__(self):
        self.user_credentials = {
            "user1": {"username": "user1", "password": "password1"},
            "user2": {"username": "user2", "password": "password2"},
            "user3": {"username": "user3", "password": "password3"},
        }

    def validate_user(self, username, password):
        """Validate user login credentials."""
        # Check hardcoded credentials
        for user_id, credentials in self.user_credentials.items():
            if credentials["username"] == username and credentials["password"] == password:
                return True

        # Check dynamically added users in cashiers.json
        cashier_file = "cashiers.json"
        if os.path.exists(cashier_file):  # Ensure the file exists
            try:
                with open(cashier_file, "r") as file:
                    cashiers_data = json.load(file)
                    for cashier_id, cashier_info in cashiers_data.items():
                        if cashier_info["username"] == username and cashier_info["password"] == password:
                            return True
            except json.JSONDecodeError:
                print("Error: Invalid JSON format in cashiers.json.")
            except Exception as e:
                print(f"Error reading cashiers.json: {e}")

        return False

    def get_categories(self):
        return {
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



