import tkinter as ttk
import ttkbootstrap as ttk
from ttkbootstrap import Style
from ttkbootstrap.dialogs import Messagebox
import os
from PIL import Image, ImageTk
from AdminGUI import GUIAdmin


class DataAdmin:

    def __init__(self):
        self.admin_credentials = {
            "admin1" : "admin1",
            "admin2" : "admin2",
            "admin3" : "admin3",
        }

    def validate_admin(self, username, password):
        """Validate admin credentials."""
        return self.admin_credentials.get(username) == password
