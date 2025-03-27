import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox
from PIL import Image, ImageTk
from ttkbootstrap import Style
import os

class FunctionsAdmin:
    def manage_items(self):
        """Place Holder for managing items"""
        Messagebox.show_info("Manage Items", "This feature is under development.")

    def manage_users(self):
        """Place Holder for managing users"""
        Messagebox.show_info("Manage Users", "This feature is under development.")

    def view_reports(self):
        """Place Holder for viewing reports"""
        Messagebox.show_info("View Reports", "This feature is under development.")

    def logout(self, root):
        """Logout the admin user."""
        root.destroy()

