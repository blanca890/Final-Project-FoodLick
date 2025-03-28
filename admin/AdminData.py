import tkinter as ttk
import ttkbootstrap as ttk
from ttkbootstrap import Style
from ttkbootstrap.dialogs import Messagebox
import os
from PIL import Image, ImageTk
from admin.AdminGUI import GUIAdmin
import json


class DataAdmin:

    def __init__(self):
        self.admin_credentials = {
            "admin1": "admin1",
            "admin2": "admin2",
            "admin3": "admin3",
        }

    def validate_admin(self, username, password):
        """Validate admin or cashier credentials and return the role."""
        # Check admin credentials
        if self.admin_credentials.get(username) == password:
            return "admin"  # Return role as admin

        # Check cashier credentials in cashiers.json
        try:
            with open("JSON/cashiers.json", "r") as file:  # Updated path
                cashiers_data = json.load(file)
                for cashier in cashiers_data.values():
                    if cashier["username"] == username and cashier["password"] == password:
                        return "cashier"  # Return role as cashier
        except FileNotFoundError:
            pass  # If the file doesn't exist, no cashiers are available

        return None  # Return None if no match is found