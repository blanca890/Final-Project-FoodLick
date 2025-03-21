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
            "Food": [("Burger", "$5.99"), ("Pizza", "$8.99"), ("Fries", "$2.99"), ("Soda", "$1.99"), ("Beef", "$30"), ("Salmon", "$20")],
            "Beverages": [("Coffee", "$3.99"), ("Tea", "$2.49"), ("Juice", "$4.99"), ("Milk", "$2.99")],
            "Household Essentials": [("Detergent", "$6.99"), ("Tissues", "$3.49"), ("Broom", "$8.99"), ("Sponge", "$2.49")],
            "Personal Care": [("Toothpaste", "$2.99"), ("Shampoo", "$5.99"), ("Lipstick", "$9.99"), ("Razor", "$4.99")]
        }

    def add_to_order(self, item_name, price):
        """Add selected item to order summary."""
        # TODO: Implement add_to_order logic

    def delete_order(self, index):
        """Remove selected item from order summary."""
        # TODO: Implement delete_order logic

    def clear_order(self):
        """Clear all selected items and reset total price."""
        # TODO: Implement clear_order logic

    def checkout(self):
        """Calculate total price and process checkout."""
        # TODO: Implement checkout logic

    def save_receipt(self):
        """Save the receipt to a file."""
        # TODO: Implement save_receipt logic

    def update_menu(self, category):
        """Clear menu & update items based on selected category."""
        # TODO: Implement update_menu logic

    def display_items(self, category):
        """Dynamically display items with images, names, and prices."""
        try:
            self.items = self.categories[category]
            self.images = []

            for item, price in self.items:
                img_path = os.path.join(os.path.dirname(__file__), "img/Pizza.jpg")  # Use absolute path
                img = Image.open(img_path)  # Ensure the file exists at this path
                img = img.resize((120, 120))
                img = ImageTk.PhotoImage(img)
                self.images.append((img, item, price))

            return self.images
        except Exception as e:
            print(f"Error in display_items: {e}")

    def update_order(self):
        """Update selected item details in order summary."""
        # TODO: Implement update_order logic

    def apply_discount(self):
        """Allow applying a discount code or percentage discount."""
        # TODO: Implement apply_discount logic


class OrderingSystemGUI:
    def __init__(self, root):
        self.logic = OrderingSystemLogic()
        self.root = root
        self.root.title("Supermarket Ordering System")
        self.root.geometry("1170x900")
        self.style = Style("litera")  # Using Litera theme

        # 🟢 Header Frame (Using Grid for Better Alignment)
        self.header_frame = ttk.Frame(root, bootstyle="dark")
        self.header_frame.grid(row=0, column=0, columnspan=3, sticky="ew", padx=10, pady=10)

        # Configure grid layout for the header frame
        self.header_frame.columnconfigure(0, weight=1)  # Column for the exit button
        self.header_frame.columnconfigure(1, weight=3)  # Column for the banner label
        self.header_frame.columnconfigure(2, weight=1)  # Column for the logo

        # Add the exit button to the header
        self.exit_button = ttk.Button(self.header_frame,text="Exit",command=root.quit,bootstyle="danger-outline",padding=10)
        self.exit_button.grid(row=0, column=0, padx=10, pady=5, sticky="w")  # Align to the left

        # Add the banner label to the header
        self.banner_label = ttk.Label(
            self.header_frame,
            text="🛒 Welcome to Supermarket Ordering System!",
            font=("Montserrat", 18, "bold"),
            bootstyle="inverse-dark"
        )
        self.banner_label.grid(row=0, column=1, padx=10, pady=5, sticky="n")  # Centered in the middle column

        # Load the logo image
        logo_image = Image.open("img/Logo.png")  # Replace with the correct path to your logo image
        logo_image = logo_image.resize((100, 100))  # Resize the image as needed
        logo_photo = ImageTk.PhotoImage(logo_image)

        # Add the logo to the header
        self.logo_label = ttk.Label(self.header_frame, image=logo_photo, bootstyle="inverse-dark")
        self.logo_label.image = logo_photo  # Keep a reference to avoid garbage collection
        self.logo_label.grid(row=0, column=2, padx=10, pady=5, sticky="e")  # Align to the right

        # 🔷 Main Content Frame (Sidebar, Items, Summary)
        self.main_frame = ttk.Frame(root)
        self.main_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

        # Configure grid layout for the main content frame
        root.rowconfigure(1, weight=1)  # Allow the main frame to expand vertically
        root.columnconfigure(0, weight=1)  # Allow the main frame to expand horizontally

        # 🟡 Left Sidebar - Category Selection
        self.sidebar_frame = ttk.Frame(self.main_frame, bootstyle="secondary", padding=10)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.category_label = ttk.Label(self.sidebar_frame,text="📌 Categories",font=("Montserrat", 14, "bold"),bootstyle="inverse-secondary")
        self.category_label.pack(pady=10)

        self.categories = {
            "Food": [("Burger", "$5.99"), ("Pizza", "$8.99"), (" Fries", "$2.99"), (" Soda", "$1.99"), ("Beef", "$30"),("Salmon", " $20")],
            "Beverages": [("Coffee", "$3.99"), ("Tea", "$2.49"), ("Juice", "$4.99"), ("Milk", "$2.99")],
            "Household Essentials": [("Detergent", "$6.99"), ("Tissues", "$3.49"), ("Broom", "$8.99"),("Sponge", "$2.49")],
            "Personal Care": [("Toothpaste", "$2.99"), ("Shampoo", "$5.99"), ("Lipstick", "$9.99"),("Razor", "$4.99")]
        }

        for category in self.categories.keys():
            btn = ttk.Button(self.sidebar_frame, text=category, bootstyle="success", padding=5,command=lambda c=category: self.update_menu(c))
            btn.pack(fill=tk.X, pady=5)

        # 🟠 Middle Section - Menu Items (Default to Food Category)
        self.menu_frame = ttk.Frame(self.main_frame, bootstyle="light", padding=10)
        self.menu_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.display_items("Food")  # Show food items by default

        # 🔵 Right Side - Order Summary Panel
        self.summary_frame = ttk.Frame(self.main_frame, bootstyle="light", padding=10)
        self.summary_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        self.summary_label = ttk.Label(self.summary_frame, text="📝 Order Summary", font=("Montserrat", 16, "bold"),bootstyle="inverse-light")
        self.summary_label.pack(pady=5)

        self.summary_listbox = tk.Listbox(self.summary_frame, height=12, font=("Montserrat", 12), relief=tk.SOLID,borderwidth=2)
        self.summary_listbox.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)

        self.total_price_label = ttk.Label(self.summary_frame, text="Total: $0.00", font=("Montserrat", 14, "bold"),bootstyle="inverse-light")
        self.total_price_label.pack(pady=5)

        # 🟢 Buttons for Order Actions
        self.btn_frame = ttk.Frame(self.summary_frame)
        self.btn_frame.pack(fill=tk.X, pady=5)

        self.discount_button = ttk.Button(self.btn_frame, text="Discount", bootstyle="success-outline", padding=5)
        self.discount_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.update_button = ttk.Button(self.btn_frame, text="Update", bootstyle="warning-outline", padding=5)
        self.update_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.delete_button = ttk.Button(self.btn_frame, text="Delete", bootstyle="danger-outline", padding=5)
        self.delete_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # 🆕 Additional Buttons (GUI-only)
        self.clear_button = ttk.Button(self.summary_frame, text="Clear Order", bootstyle="info-outline", padding=5,command=self.clear_order)
        self.clear_button.pack(fill=tk.X, padx=5, pady=5)

        self.checkout_button = ttk.Button(self.summary_frame, text="Checkout", bootstyle="primary-outline", padding=5,command=self.checkout)
        self.checkout_button.pack(fill=tk.X, padx=5, pady=5)

        # 🆕 Save Receipt Button
        self.save_receipt_button = ttk.Button(self.summary_frame, text="Save Receipt", bootstyle="success-outline",padding=5, command=self.save_receipt)
        self.save_receipt_button.pack(fill=tk.X, padx=5, pady=5)

    def update_menu(self, category):
        """Clear menu & update items based on selected category."""
        # TODO: Delegate to OrderingSystemLogic

    def display_items(self, category):
        """Dynamically display items with images, names, and prices."""
        try:
            self.images = self.logic.display_items(category)
            for widget in self.menu_frame.winfo_children():
                widget.destroy()

            for i, (img, item, price) in enumerate(self.images):
                frame = ttk.Frame(self.menu_frame, bootstyle="info", padding=30)
                frame.grid(row=i // 3, column=i % 3, padx=20, pady=20, sticky="nsew")

                lbl = ttk.Label(frame, image=img)
                lbl.image = img
                lbl.pack()

                text_label = ttk.Label(
                    frame, text=f"{item}\n{price}", font=("Montserrat", 12, "bold"), bootstyle="inverse-info"
                )
                text_label.pack(pady=5)

                btn = ttk.Button(
                    frame,
                    text="Add to Order",
                    bootstyle="success-outline",
                    command=lambda i=item, p=price: self.add_to_order(i, p),
                )
                btn.pack(fill=tk.X)
        except Exception as e:
            print(f"Error in display_items: {e}")

    def add_to_order(self, item_name, price):
        """Add selected item to order summary."""
        # TODO: Delegate to OrderingSystemLogic

    def update_order(self):
        """Update selected item details in order summary."""
        # TODO: Delegate to OrderingSystemLogic

    def delete_order(self):
        """Remove selected item from order summary."""
        # TODO: Delegate to OrderingSystemLogic

    def clear_order(self):
        """Clear all selected items and reset total price."""
        # TODO: Delegate to OrderingSystemLogic

    def checkout(self):
        """Calculate total price and process checkout."""
        # TODO: Delegate to OrderingSystemLogic

    def save_receipt(self):
        """Save the receipt to a file."""
        # TODO: Delegate to OrderingSystemLogic

    def apply_discount(self):
        """Allow applying a discount code or percentage discount."""
        # TODO: Delegate to OrderingSystemLogic

    def update_summary(self):
        """Update the order summary listbox and total price label."""
        # TODO: Delegate to OrderingSystemLogic


if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap ("img/Logo.ico")
    app = OrderingSystemGUI(root)
    root.mainloop()