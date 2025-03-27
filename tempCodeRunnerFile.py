import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox
from PIL import Image, ImageTk
from ttkbootstrap import Style
import os

class AdminLogin:
    def __init__(self, root, logic, on_success):
        """
        Initialize the AdminLogin popup.
        :param root: The root Tkinter window.
        :param logic: The logic instance for admin validation.
        :param on_success: Callback function to execute on successful login.
        """
        self.root = root
        self.logic = logic
        self.on_success = on_success
        self.create_login_popup()

    def create_login_popup(self):
        """Create the admin login popup."""
        popup = tk.Toplevel(self.root)
        popup.title("Admin Login")
        popup.geometry("300x200")
        popup.grab_set()

        ttk.Label(popup, text="Admin Username:", font=("Montserrat", 12)).pack(pady=10)
        username_entry = ttk.Entry(popup, font=("Montserrat", 12))
        username_entry.pack(pady=5)

        ttk.Label(popup, text="Admin Password:", font=("Montserrat", 12)).pack(pady=10)
        password_entry = ttk.Entry(popup, font=("Montserrat", 12), show="*")
        password_entry.pack(pady=5)

        def confirm_login():
            username = username_entry.get()
            password = password_entry.get()
            if self.logic.validate_admin(username, password):  # Use logic for validation
                Messagebox.show_info("Login successful!", "Welcome, Admin!")
                popup.destroy()
                self.on_success()  # Call the success callback
            else:
                Messagebox.show_error("Invalid credentials!", "Login Error")

        ttk.Button(popup, text="Login", command=confirm_login, bootstyle="success").pack(side=tk.LEFT, padx=10, pady=10)
        ttk.Button(popup, text="Cancel", command=popup.destroy, bootstyle="danger").pack(side=tk.RIGHT, padx=10, pady=10)


class GUIAdmin:
    def __init__(self, root, logic):
        self.root = root
        self.logic = logic
        self.style = Style("litera")
        self.root.title("Admin Panel")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.configure(bg="white")

        # Directly initialize the admin interface
        self.init_admin_interface()

    def init_admin_interface(self):
        """Initialize the admin interface."""
        # Create the admin panel widgets
        self.create_widgets()

    def create_widgets(self):
        """Create the admin panel widgets."""

        title_label =  ttk.Label(self.root, text="Admin Panel", font=("Montserrat", 24), background="white", anchor="center", bootstyle="primary")
        title_label.pack(pady=20)

        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=50)

        manage_users_button = ttk.Button(button_frame, text="Manage Users", command=self.manage_users, bootstyle="primary")
        manage_users_button.grid(row=0, column=0, padx=20, pady=10)

        view_reports_button = ttk.Button(button_frame, text="View Reports", command=self.view_reports, bootstyle="primary")
        view_reports_button.grid(row=0, column=1, padx=20, pady=10)

        settings_button = ttk.Button(button_frame, text="Settings", command=self.settings, bootstyle="primary")
        settings_button.grid(row=0, column=2, padx=20, pady=10)

        logout_button = ttk.Button(button_frame, text="Logout", command=self.logout, bootstyle="primary")
        logout_button.grid(row=0, column=3, padx=20, pady=10)




