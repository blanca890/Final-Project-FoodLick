import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import Style
from ttkbootstrap.dialogs import Messagebox
from PIL import Image, ImageTk
from user.UserData import DataUser
from user.UserFunctions import FunctionUser
import os
import json

class LoginScreen:
    def __init__(self, root, style, on_login_success):
        self.root = root
        self.style = style  # Use the shared Style object
        self.on_login_success = on_login_success  # Callback to open the main app
        self.logic = FunctionUser()  # Create an instance of FunctionUser

        self.root.title("Login - Supermarket Ordering System")
        self.root.geometry("400x300")
        

        self.center_window(400,300)

        # Username Label and Entry
        self.username_label = ttk.Label(self.root, text="Username:", font=("Montserrat", 14))
        self.username_label.pack(pady=10)
        self.username_entry = ttk.Entry(self.root, font=("Montserrat", 14))
        self.username_entry.pack(pady=5)

        # Password Label and Entry
        self.password_label = ttk.Label(self.root, text="Password:", font=("Montserrat", 14))
        self.password_label.pack(pady=10)
        self.password_entry = ttk.Entry(self.root, font=("Montserrat", 14), show="*")
        self.password_entry.pack(pady=5)

        # Login Button
        self.login_button = ttk.Button(self.root, text="Login", command=self.login, bootstyle="primary", padding=10)
        self.login_button.pack(pady=20)
    
    def center_window(self,width,height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        self.root.geometry(f"{width}x{height}+{int(x)}+{int(y)}")


    def login(self):
        """Handle user and admin login."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        # Check admin credentials first
        from admin.AdminData import DataAdmin
        admin_logic = DataAdmin()
        role = admin_logic.validate_admin(username, password)
        if role == "admin":
            Messagebox.show_info("Login successful!", f"Welcome, Admin {username}!")
            self.root.after(500, lambda: self.on_login_success(username, "admin"))
            return
        elif role == "cashier":
            Messagebox.show_info("Login successful!", f"Welcome, Cashier {username}!")
            self.root.after(500, lambda: self.on_login_success(username, "user"))  # Treat cashier as user
            return

        # Validate login using FunctionUser for regular users
        if self.logic.login(username, password):
            Messagebox.show_info("Login successful!", f"Welcome, {username}!")
            self.root.after(500, lambda: self.on_login_success(username, "user"))
        else:
            Messagebox.show_error("Invalid credentials!", "Login Error")

class GUIUser:
    def __init__(self, root, logic, username):  # Add username parameter
        self.logic = logic
        self.username = username  # Store the username
        self.root = root
        self.data_user = DataUser()

        self.root.title("Supermarket Ordering System")
        self.root.geometry("1500x900")
        self.style = Style("litera")

        self.center_window_gui(1500, 900)

        # Header Frame
        self.header_frame = ttk.Frame(root, bootstyle="dark")
        self.header_frame.grid(row=0, column=0, columnspan=3, sticky="ew", padx=10, pady=10)

        # Exit Button
        self.exit_button = ttk.Button(self.header_frame, text="Logout", command=self.logout, bootstyle="danger-outline", padding=10)
        self.exit_button.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        

        # Logo
        try:
            logo_image = Image.open("img/logo.png") 
            logo_image = logo_image.resize((150, 150))
            logo_photo = ImageTk.PhotoImage(logo_image)
            self.logo_label = ttk.Label(self.header_frame, image=logo_photo, bootstyle="inverse-dark")
            self.logo_label.image = logo_photo
            self.logo_label.grid(row=0, column=2, padx=10, pady=5, sticky="e")
            self.header_frame.columnconfigure(1, weight=1)  # Give weight to the title column
            self.header_frame.columnconfigure(2, weight=0)  # No weight for spacing
            self.header_frame.columnconfigure(3, weight=0)  # No weight for logo column
        except Exception as e:
            print(f"Error loading logo: {e}")
            
        try:
            # Banner image with adjusted size
            banner_image = Image.open("img/banner.png")
            banner_image = banner_image.resize((1200, 170))  # Adjusted size to better fit window width
            banner_photo = ImageTk.PhotoImage(banner_image)
            self.banner_label = ttk.Label(
                self.header_frame,
                image=banner_photo,
                bootstyle="inverse-dark"
            )
            self.banner_label.image = banner_photo  # Keep a reference
            self.banner_label.grid(row=0, column=1, padx=10, pady=20, sticky="nsew")  # Changed sticky to fill space
        except Exception as e:
            print(f"Error loading banner: {e}")
            # Fallback to text if image fails to load
            self.banner_label = ttk.Label(
                self.header_frame,
                text="🛒 Welcome to Supermarket Ordering System!",
                font=("Montserrat", 35, "bold"),
                bootstyle="inverse-dark"
            )
            self.banner_label.grid(row=0, column=1, padx=10, pady=20, sticky="nsew")

        # Sliding Banner Animation
        self.sliding_banner = ttk.Label(
            self.header_frame,
            text="🎉 Special Discounts Available Today! 🎉",
            font=("Montserrat", 14),
            bootstyle="inverse-dark"
        )
        self.sliding_banner.place(x=1500, y=150)  
        self.animate_sliding_banner()  

        # Main Frame
        self.main_frame = ttk.Frame(root)
        self.main_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        root.rowconfigure(1, weight=1)
        root.columnconfigure(0, weight=1)

        # Sidebar Frame (Category Selection)
        self.sidebar_frame = ttk.Frame(self.main_frame, bootstyle="light", padding=10)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Add a canvas and scrollbar for the sidebar
        self.sidebar_canvas = tk.Canvas(self.sidebar_frame, width=200, height=600)  # Set fixed width and height
        self.sidebar_scrollbar = ttk.Scrollbar(self.sidebar_frame, orient=tk.VERTICAL, command=self.sidebar_canvas.yview)
        self.sidebar_inner_frame = ttk.Frame(self.sidebar_canvas, width=180)  # Set inner frame width

        # Configure the canvas and scrollbar
        self.sidebar_inner_frame.bind("<Configure>", lambda e: self.sidebar_canvas.configure(scrollregion=self.sidebar_canvas.bbox("all")))
        self.sidebar_canvas.create_window((0, 0), window=self.sidebar_inner_frame, anchor="nw")
        self.sidebar_canvas.configure(yscrollcommand=self.sidebar_scrollbar.set)

        self.sidebar_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.sidebar_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Add category buttons to the scrollable inner frame
        self.category_label = ttk.Label(self.sidebar_inner_frame, text="📌 Categories", font=("Montserrat", 14, "bold"), bootstyle="inverse-secondary")
        self.category_label.pack(pady=10)

        for category in self.logic.categories.keys():
            btn = ttk.Button(self.sidebar_inner_frame, text=category, bootstyle="success", padding=5, command=lambda c=category: self.display_items(c))
            btn.pack(fill=tk.X, pady=5)

        # Menu Frame
        self.menu_frame = ttk.Frame(self.main_frame, bootstyle="light", padding=10)
        self.menu_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create a canvas and a scrollbar for the menu frame
        self.canvas = tk.Canvas(self.menu_frame)
        self.scrollbar = ttk.Scrollbar(self.menu_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollable_menu_frame = ttk.Frame(self.canvas)

        self.scrollable_menu_frame.bind("<Configure>",lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.scrollable_menu_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Order Summary Frame
        self.summary_frame = ttk.Frame(self.main_frame, bootstyle="light", padding=10)
        self.summary_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        # Summary Listbox
        self.summary_listbox = tk.Listbox(self.summary_frame, height=12, width=30, font=("Montserrat", 12), relief=tk.SOLID, borderwidth=2)
        self.summary_listbox.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)

        # Total Price Label
        self.total_price_label = ttk.Label(
            self.summary_frame, 
            text=("Subtotal: $0.00\n"
            "Discount: $0.00\n"
            "VAT (12%): $0.00\n"
            "Tax (10%): $0.00\n" 
            "─────────────\n"
            "Final Total: $0.00"),
             font=("Montserrat", 14, "bold"), 
             bootstyle="inverse-light")
        
        self.total_price_label.pack(fill=tk.X, padx=10, pady=5)


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


        # Sliding Banner Animation
        self.sliding_banner = ttk.Label(
            self.header_frame,
            text="🎉 Special Discounts Available Today! 🎉 🎉 Special Discounts Available Today! 🎉 🎉 Special Discounts Available Today! 🎉 🎉 Special Discounts Available Today! 🎉 🎉 Special Discounts Available Today! 🎉 🎉 Special Discounts Available Today! 🎉 🎉 Special Discounts Available Today! 🎉 🎉 Special Discounts Available Today! 🎉",
            font=("Montserrat", 14),
            bootstyle="inverse-dark"
        )
        self.sliding_banner.place(x=1500, y=50) 
        self.animate_sliding_banner()

        for category in self.logic.categories.keys():
            btn = ttk.Button(self.sidebar_inner_frame, text=category, bootstyle="success", padding=5, command=lambda c=category: self.display_items(c))
            btn.pack(fill=tk.X, pady=5)
            self.add_button_hover_animation(btn)

    def animate_sliding_banner(self):
        """Animate the sliding banner."""
        current_x = self.sliding_banner.winfo_x()
        new_x = current_x - 2  
        if new_x < -self.sliding_banner.winfo_width():  
            new_x = 1500
        self.sliding_banner.place(x=new_x, y=125)  
        self.root.after(100, self.animate_sliding_banner)  

    def add_button_hover_animation(self, button):
        """Add hover animation to a button."""
        def on_enter(event):
            button.config(bootstyle="info-outline")  

        def on_leave(event):
            button.config(bootstyle="success") 

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    def center_window_gui(self,width,height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width//2) - (width//2)
        y = (screen_height//2) - (height//2)
        self.root.geometry(f"{width}x{height}+{(x)}+{y}")

    def center_popup(self, popup, width, height):
        """Center a popup window on the screen."""
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        popup.geometry(f"{width}x{height}+{x}+{y}")

    def show_centered_messagebox(self, message_type, title, message):
        """Show a centered Messagebox."""
        # Directly call the Messagebox without using a Toplevel wrapper
        if message_type == "info":
            Messagebox.show_info(message, title)
        elif message_type == "warning":
            Messagebox.show_warning(message, title)
        elif message_type == "error":
            Messagebox.show_error(message, title)

    def update_menu(self):
        """Open a popup to update the quantity and add-ons of a selected item."""
        selected_index = self.summary_listbox.curselection()
        if not selected_index:
            self.show_centered_messagebox("warning", "Warning", "Please select an item to update!")
            return

        index = selected_index[0]
        selected_text = self.summary_listbox.get(index)

        # Prevent updating add-ons or total lines
        if selected_text.startswith((" ", "-")):
            self.show_centered_messagebox("error", "Error", "Invalid item selected!")
            return

        # Create a mapping of only main items (excluding add-ons and totals)
        main_item_indices = []
        for i in range(self.summary_listbox.size()):
            text = self.summary_listbox.get(i)
            if not text.startswith((" ", "-")):
                main_item_indices.append(i)

        # Ensure the selected index is valid
        if index not in main_item_indices:
            self.show_centered_messagebox("error", "Error", "Invalid item selected!")
            return

        # Find the corresponding index in the actual order list
        order_index = main_item_indices.index(index)
        item_name, item_price, quantity, addons = self.logic.order[order_index]

        # Open a popup for updating the item
        popup = tk.Toplevel(self.root)
        popup.title(f"Update {item_name}")
        self.center_popup(popup, 400, 400)
        popup.geometry("400x400")
        popup.grab_set()

        ttk.Label(popup, text=f"Update {item_name}", font=("Montserrat", 14)).pack(pady=10)

        # Quantity update
        ttk.Label(popup, text="Quantity:", font=("Montserrat", 12)).pack(pady=5)
        quantity_var = tk.IntVar(value=quantity)
        quantity_entry = ttk.Entry(popup, textvariable=quantity_var, font=("Montserrat", 12), width=5)
        quantity_entry.pack(pady=5)

        # Add-ons update
        addons_var = []
        ttk.Label(popup, text="Update Add-ons:", font=("Montserrat", 12)).pack(pady=5)
        for addon_name, addon_price in addons:
            var = tk.IntVar(value=1) 
            chk = ttk.Checkbutton(
                popup,
                text=f"{addon_name} (+${addon_price:.2f})",
                variable=var
            )
            chk.pack(anchor='w', padx=10)
            addons_var.append((var, addon_name, addon_price))

        def confirm_update():
            new_quantity = quantity_var.get()
            if new_quantity <= 0:
                self.show_centered_messagebox("error", "Error", "Quantity must be greater than 0!")
                return

            updated_addons = [(addon_name, addon_price) for var, addon_name, addon_price in addons_var if var.get()]
            self.logic.update_order(order_index, new_quantity, updated_addons)
            self.update_summary()
            popup.destroy()

        ttk.Button(popup, text="Update", command=confirm_update, bootstyle="success").pack(side=tk.LEFT, pady=10, padx=10)
        ttk.Button(popup, text="Cancel", command=popup.destroy, bootstyle="danger").pack(side=tk.RIGHT, pady=10, padx=10)

    def display_items(self, category):
        """Dynamically display items with images, names, and prices."""
        try:
            with open("JSON/items.json", "r") as file:
                items = json.load(file)

            category_items = items.get(category, [])
            for widget in self.scrollable_menu_frame.winfo_children():
                widget.destroy()

            # Adjust the number of columns for the grid
            num_columns = 4 

            for i, item in enumerate(category_items):
                frame = ttk.Frame(self.scrollable_menu_frame, bootstyle="info", padding=20)
                frame.grid(row=i // num_columns, column=i % num_columns, padx=20, pady=20, sticky="nsew")

                # Dynamically configure column weights for even spacing
                self.scrollable_menu_frame.columnconfigure(i % num_columns, weight=1)

                try:
                    # Load and display the item image
                    img = Image.open(item["image"])
                    img = img.resize((90, 90))  
                    photo = ImageTk.PhotoImage(img)
                    lbl = ttk.Label(frame, image=photo)
                    lbl.image = photo
                    lbl.pack(pady=5)
                except Exception as e:
                    print(f"Error loading image: {e}")

                # Display item name and price
                text_label = ttk.Label(
                    frame,
                    text=f"{item['name']}\n${item['price']:.2f}",
                    font=("Montserrat", 12, "bold"),
                    bootstyle="inverse-info",
                    anchor="center",
                    justify="center"
                )
                text_label.pack(pady=5)

                # Quantity label and entry
                quantity_label = ttk.Label(frame, text="Quantity:", font=("Montserrat", 10))
                quantity_label.pack()

                quantity_entry = ttk.Entry(frame, font=("Montserrat", 10), width=5)
                quantity_entry.insert(0, "1")
                quantity_entry.pack()

                # Add to Order button
                btn = ttk.Button(
                    frame,
                    text="Add to Order",
                    bootstyle="success-outline",
                    command=lambda i=item, q=quantity_entry: self.open_addons_popup(i["name"], i["price"], int(q.get())),
                )
                btn.pack(fill=tk.X, pady=5)

        except Exception as e:
            print(f"Error in display_items: {e}")

    def open_addons_popup(self, item_name, price, quantity):
        """Open a popup window for selecting add-ons."""
        popup = tk.Toplevel(self.root)
        popup.title(f"Add-ons for {item_name}")
        self.center_popup(popup, 400, 400)  # Center the popup
        popup.geometry("400x400")
        popup.grab_set()

        addons_var = [] 
        size_var = tk.StringVar(value="Small Size")  

        # Load add-ons from the JSON file
        try:
            addons_file = os.path.join("JSON", "addons.json")  
            with open(addons_file, "r") as file:
                item_addons = json.load(file)
        except Exception as e:
            self.show_centered_messagebox("error", "Error", f"Error loading add-ons: {e}")
            popup.destroy()
            return

        # Fetch add-ons for the exact item name
        addons = item_addons.get(item_name, [])
        ttk.Label(popup, text=f"Select add-ons for {item_name}", font=("Montserrat", 14)).pack(pady=10)

        # Separate sizes and other add-ons
        sizes = [addon for addon in addons if "Size" in addon["name"]]
        other_addons = [addon for addon in addons if "Size" not in addon["name"]]

        # Display size options as radio buttons
        if sizes:
            ttk.Label(popup, text="Select Size:", font=("Montserrat", 12)).pack(pady=5)
            for size in sizes:
                ttk.Radiobutton(
                    popup,
                    text=f"{size['name']} (+${size['price']:.2f})",
                    variable=size_var,
                    value=size["name"]
                ).pack(anchor='w', padx=10)

        # Display other add-ons as checkboxes
        if other_addons:
            ttk.Label(popup, text="Select Add-ons:", font=("Montserrat", 12)).pack(pady=5)
            for addon in other_addons:
                var = tk.IntVar()
                chk = ttk.Checkbutton(
                    popup,
                    text=f"{addon['name']} (+${addon['price']:.2f})",
                    variable=var
                )
                chk.pack(anchor='w', padx=10)
                addons_var.append((var, addon))

        def confirm_addons():
            selected_addons = []

            # Process selected add-ons
            for var, addon in addons_var:
                if var.get():  # Check if the add-on is selected
                    selected_addons.append((addon['name'], addon['price']))

            # Add the selected size as an add-on
            selected_size = next((size for size in sizes if size["name"] == size_var.get()), None)
            if selected_size:
                selected_addons.append((selected_size["name"], selected_size["price"]))

            # Add item with add-ons to the order
            self.add_to_order(item_name, price, quantity, selected_addons)
            popup.destroy()

        ttk.Button(popup, text="Confirm", command=confirm_addons, bootstyle="success").pack(side=tk.LEFT, pady=10)
        ttk.Button(popup, text="Cancel", command=popup.destroy, bootstyle="danger").pack(side=tk.LEFT, pady=10)

    def add_to_order(self, item_name, price, quantity=1, addons=None):
        """Add selected item to order summary with add-ons."""
        try:
            # Convert price to float if it's not already
            item_price = float(price)

            # Calculate the total price for the item including add-ons
            total_price = item_price * quantity
            if addons:
                for addon_name, addon_price in addons:
                    total_price += float(addon_price) * quantity 

            # Add the item and its add-ons to the order
            self.logic.add_to_order(item_name, total_price, quantity, addons)
            self.update_summary()
        except Exception as e:
            print(f"Error in add_to_order: {e}")

    def delete_order(self):
        """Remove selected item from order summary."""
        try:
            selected_index = self.summary_listbox.curselection()
            if not selected_index:
                self.show_centered_messagebox("warning", "Warning", "Please select an item to delete!")
                return

            index = selected_index[0]
            selected_text = self.summary_listbox.get(index)

            # Prevent deleting add-ons or total lines
            if selected_text.startswith((" ", "-")):
                self.show_centered_messagebox("error", "Error", "Invalid item selected!")
                return

            # Create a mapping of only main items (excluding add-ons and totals)
            main_item_indices = []
            for i in range(self.summary_listbox.size()):
                text = self.summary_listbox.get(i)
                if not text.startswith((" ", "-")):
                    main_item_indices.append(i)

            # Ensure the selected index is valid
            if index not in main_item_indices:
                self.show_centered_messagebox("error", "Error", "Invalid item selected!")
                return

            # Find the corresponding index in the actual order list
            order_index = main_item_indices.index(index)

            # Delete from order and update UI
            item_name = self.logic.order[order_index][0]
            self.logic.delete_order(order_index)
            self.update_summary()
            self.show_centered_messagebox("info", "Item Removed", f"Removed {item_name} from the order.")

        except Exception as e:
            self.show_centered_messagebox("error", "Error", f"Error in deleting item: {e}")

    def clear_order(self):
        """Clear all selected items, reset total price, and clear discount."""
        self.logic.clear_order()
        self.logic.applied_discount = 0.0  # Reset discount
        self.logic.current_discount_code = None  # Clear the discount code
        self.update_summary()

    def checkout(self):
        """Calculate total price and process checkout."""
        self.logic.checkout()
        self.update_summary()

    def save_receipt(self):
        """Save the receipt to a file."""
        self.logic.save_receipt(self.username) 

    def apply_discount(self):
        """Open a popup to apply or update a discount code."""
        popup = tk.Toplevel(self.root)
        popup.title("Apply/Update Discount")
        self.center_popup(popup, 300, 200)  # Center the popup
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

        # Add a label and Combobox for the discount code
        ttk.Label(popup, text="Select Discount Code:", font=("Montserrat", 12)).pack(pady=10)
        discount_var = tk.StringVar()
        discount_combobox = ttk.Combobox(popup, textvariable=discount_var, font=("Montserrat", 12), state="readonly")
        discount_combobox['values'] = list(discount_codes.keys())
        discount_combobox.pack(pady=5)

        # Pre-select the current discount if applied
        current_discount = getattr(self.logic, "current_discount_code", None)
        if current_discount:
            discount_combobox.set(current_discount)

        # Function to validate and apply the discount
        def confirm_discount():
            code = discount_var.get().strip().upper()
            if code in discount_codes:
                discount = discount_codes[code]
                if 0 < discount <= 100:
                    discount_amount = (discount / 100) * self.logic.total_price
                    self.logic.total_price -= discount_amount
                    self.logic.applied_discount = discount_amount  # Store the discount amount
                    self.logic.current_discount_code = code  # Store the current discount code
                    self.update_summary()
                    self.show_centered_messagebox(
                        "info", "Success", f"Discount applied! {discount}% off.\nNew total: ${self.logic.total_price:.2f}"
                    )
                    popup.destroy()
                else:
                    self.show_centered_messagebox("error", "Error", "Invalid discount percentage.")
            else:
                self.show_centered_messagebox("error", "Error", "Please select a valid discount code.")

        # Add Confirm and Cancel buttons
        ttk.Button(popup, text="Apply", command=confirm_discount, bootstyle="success").pack(side=tk.LEFT, padx=10, pady=10)
        ttk.Button(popup, text="Cancel", command=popup.destroy, bootstyle="danger").pack(side=tk.RIGHT, padx=10, pady=10)

    def update_summary(self):
        """Update the order summary listbox and total price label."""
        self.summary_listbox.delete(0, tk.END)  # Clear listbox
        total_width = 25  # Adjust this width as needed for balance

        for item, item_price, quantity, addons in self.logic.order:
            # Calculate the original price of the item (excluding add-ons)
            original_price = item_price / quantity
            if addons:
                for _, addon_price in addons:
                    original_price -= addon_price  # Subtract add-on prices

            # Format the main item with its original price and quantity
            dot_count = total_width - len(item) - len(f"${original_price:.2f}") - len(f" (x{quantity})")
            dots = "." * max(dot_count, 0)  # Ensure no negative dots
            formatted_item = f"{item} (x{quantity}) {dots} ${original_price:.2f}"
            self.summary_listbox.insert(tk.END, formatted_item)

            # Add add-ons below the main item, including their quantities
            if addons:
                for addon_name, addon_price in addons:
                    addon_total_price = addon_price * quantity  # Calculate total price for the add-on
                    self.summary_listbox.insert(
                        tk.END,
                        f"   ➜ {addon_name} (x{quantity}): ${addon_total_price:.2f}"
                    )

            # Add the total price for the item (including add-ons) at the bottom
            self.summary_listbox.insert(tk.END, f"   Total for {item}: ${item_price:.2f}")
            
            # Add a divider for clarity
            self.summary_listbox.insert(tk.END, "-" * 40)

        # Add discount information if applied
        discount_amount = getattr(self.logic, "applied_discount", 0.0)
        vat_amount = self.logic.total_price * 0.12  # Example VAT calculation
        tax_amount = self.logic.total_price * 0.10  # Example tax calculation
        final_total = self.logic.total_price + vat_amount + tax_amount  # Final total with VAT and tax

        # Update the total price label
        self.total_price_label.config(
            text=f"Subtotal: ${self.logic.total_price + discount_amount:.2f}\n" +
                 f"Discount: -${discount_amount:.2f}\n" +
                 f"VAT (12%): ${vat_amount:.2f}\n" +
                 f"Tax (10%): ${tax_amount:.2f}\n" +
                 f"─────────────\n" +
                 f"Final Total: ${final_total:.2f}"
        )

    def logout(self):
        """Logout and return to the login page."""
        for widget in self.root.winfo_children():
            widget.destroy()
        from user.UserGUI import LoginScreen
        LoginScreen(self.root, self.style, self.open_main_app)  # Pass the correct callback

    def open_main_app(self, username, role):
        """Open the main application based on the role."""
        for widget in self.root.winfo_children():
            widget.destroy()
        if role == "admin":
            from admin.AdminData import DataAdmin
            logic = DataAdmin()
            from admin.AdminGUI import GUIAdmin
            GUIAdmin(self.root, logic)
        elif role == "user":
            from user.UserFunctions import FunctionUser
            logic = FunctionUser()
            GUIUser(self.root, logic, username)

if __name__ == "__main__":
    root = tk.Tk()
    style = Style("litera")
    try:
        root.iconbitmap("img/Logo.ico")
    except Exception as e:
        print(f"Error loading icon: {e}")

    # Create a dummy logic instance for testing
    class DummyLogic:
        def __init__(self):
            self.categories = {
                "Food": [],
                "Beverages": [],
                "Household Essentials": [],
                "Fresh Produce": [],
                "Meat,Poultry & Seafood": [],
                "Dairy & Eggs": [],
                "Bakery": [],
                "Pantry Staples":[],
                "Frozen Foods":[],
                "Snacks & Sweets":[],
                "Household & Cleaning Product":[],
                "Personal Care & Health":[],
                "Baby & Pet Supplies": [],
                "Alchohol & Tobacco":[]
            }
            self.order = []
            self.total_price = 0.0

        def add_to_order(self, item_name, total_price, quantity, addons):
            self.order.append((item_name, total_price, quantity, addons))
            self.total_price += total_price

        def delete_order(self, index):
            item = self.order.pop(index)
            self.total_price -= item[1]

        def clear_order(self):
            self.order = []
            self.total_price = 0.0

        def checkout(self):
            print("Checkout complete!")

        def save_receipt(self, username):
            print(f"Receipt saved for {username}!")

        def update_order(self, index, quantity, addons):
            item_name, item_price, _, _ = self.order[index]
            base_price = item_price / quantity
            new_price = base_price * quantity
            for _, addon_price in addons:
                new_price += addon_price * quantity
            self.order[index] = (item_name, new_price, quantity, addons)
            self.total_price = sum(item[1] for item in self.order)

    # Instantiate GUIUser with DummyLogic
    logic = DummyLogic()
    GUIUser(root, logic, "TestUser")

    root.mainloop()