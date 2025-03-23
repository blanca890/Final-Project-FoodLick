from struct import pack
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

    def add_to_order(self, item_name, price, addons=None):
        """Add selected item with add-ons to order summary."""
        try:
            # Convert price from string to float
            item_price = float(price.strip("$"))
            total_item_price = item_price

            # Process add-ons
            if addons:
                for addon_name, addon_price in addons:
                    total_item_price += float(addon_price.strip("$"))

            # Add to order list
            self.order.append((item_name, total_item_price, addons))
            self.total_price += total_item_price

        except Exception as e:
            print(f"Error in add_to_order: {e}")

    def delete_order(self, index):
        """Remove selected item from order summary."""
        try:
            if 0 <= index < len(self.order):
                _, item_price, _ = self.order.pop(index)
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
        for item, price, addons in self.order:
            receipt_text += f"{item}: ${price:.2f}\n"
            if addons:
                for addon, addon_price in addons:
                    receipt_text += f"   ➜ {addon}: ${addon_price}\n"

        receipt_text += f"\nTotal: ${self.total_price:.2f}"
        Messagebox.show_info(receipt_text, "Checkout Complete")

    def save_receipt(self):
        """Save the receipt to a file."""
        if not self.order:
            Messagebox.show_error("No order to save!", "Error")
            return

        try:
            with open("receipt.txt", "w") as file:
                file.write("🛒 Supermarket Receipt\n\n")
                for item, price, addons in self.order:
                    file.write(f"{item}: ${price:.2f}\n")
                    if addons:
                        for addon, addon_price in addons:
                            file.write(f"   ➜ {addon}: ${addon_price}\n")

                file.write(f"\nTotal: ${self.total_price:.2f}")

            Messagebox.show_info("Receipt saved successfully!", "Success")
        except Exception as e:
            Messagebox.show_error(f"Error saving receipt: {e}", "Error")

    def update_menu(self, category):
        """Clear menu & update items based on selected category."""
        # TODO: Implement update_menu logic
        self.categories.delete(0, 'end')  # Assuming you're using a Listbox named menu_listbox

        # Get items from the selected category
        items = self.categories.get(category, [])

        # Populate the menu with the new items
        for item in items:
            self.categories.insert('end', item)

    def display_items(self, category):
        """Dynamically display items with images, names, and prices."""
        try:
            self.items = self.categories[category]
            self.images = []

            for item, price in self.items:
                img_path = os.path.join(os.path.dirname(__file__), "img/Pizza.jpg")
                img = Image.open(img_path)
                img = img.resize((120, 120))
                img = ImageTk.PhotoImage(img)
                self.images.append((img, item, price))

            return self.images
        except Exception as e:
            print(f"Error in display_items: {e}")

    def update_order(self, item_index, new_quantity=None, new_price=None):
        """Update selected item details in order summary."""
        # TODO: Implement update_order logic
        if 0 <= item_index < len(self.order_items):
            item = self.order_items[item_index]
            original_item = item.copy()  # For logging

            if new_quantity is not None:
                item['quantity'] = new_quantity
            if new_price is not None:
                item['price'] = new_price

            print(f"Item updated from {original_item} to {item}")
        else:
            print("Invalid item index. Update failed.")

    def apply_discount(self):
        """Allow applying a discount code or percentage discount."""
        #TODO: discount codes
        discount_codes = {
        'SAVE10': 10,   # 10% off
        'SAVE20': 20,   # 20% off
        'HALFOFF': 50   # 50% off
        }

    # Prompt user to enter the discount code
        discount_code = input("Enter your discount code: ").strip().upper()
    
    # Check if the entered code is valid
        if discount_code in discount_codes:
            discount = discount_codes[discount_code]
            print(f"✅ Discount code '{discount_code}' applied: {discount}% off")

            if 0 < discount <= 100:
                discount_amount = (discount / 100) * self.total_cost
                self.total_cost -= discount_amount
                print(f"💰 You saved ${discount_amount:.2f}! New total: ${self.total_cost:.2f}")
            else:
                print("Invalid discount percentage.")
        else:
            print("Invalid discount code.")


class OrderingSystemGUI:
    def __init__(self, root):
        self.logic = OrderingSystemLogic()
        self.root = root
        self.root.title("Supermarket Ordering System")
        self.root.geometry("1170x900")
        self.style = Style("litera") 

        #  Header Frame
        self.header_frame = ttk.Frame(root, bootstyle="dark")
        self.header_frame.grid(row=0, column=0, columnspan=3, sticky="ew", padx=10, pady=10)

        # grid layout for header
        self.header_frame.columnconfigure(0, weight=1)  # Column exit button
        self.header_frame.columnconfigure(1, weight=3)  # Column banner label
        self.header_frame.columnconfigure(2, weight=1)  # Column logo

        # exit button to header
        self.exit_button = ttk.Button(self.header_frame,text="Exit",command=root.quit,bootstyle="danger-outline",padding=10)
        self.exit_button.grid(row=0, column=0, padx=10, pady=5, sticky="w")  # Align to the left

        # banner label to header
        self.banner_label = ttk.Label(
            self.header_frame,
            text="🛒 Welcome to Supermarket Ordering System!",
            font=("Montserrat", 18, "bold"),
            bootstyle="inverse-dark"
        )
        self.banner_label.grid(row=0, column=1, padx=10, pady=5, sticky="n")  # Centered in the middle column

        # Load logo image
        path_image = os.path.join(os.path.dirname(__file__), "img/Logo.png")
        logo_image = Image.open(path_image)  # Replace with the correct path to your logo image
        logo_image = logo_image.resize((100, 100))  # Resize the image as needed
        logo_photo = ImageTk.PhotoImage(logo_image)

        # logo to the header
        self.logo_label = ttk.Label(self.header_frame, image=logo_photo, bootstyle="inverse-dark")
        self.logo_label.image = logo_photo  # Keep a reference to avoid garbage collection
        self.logo_label.grid(row=0, column=2, padx=10, pady=5, sticky="e")  # Align to the right

        # 🔷 Main Content Frame 
        self.main_frame = ttk.Frame(root)
        self.main_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

        # grid layout for the main 
        root.rowconfigure(1, weight=1)  #vertically
        root.columnconfigure(0, weight=1)  #horizontally

        # 🟡 Category Selection
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

        # Menu Items 
        self.menu_frame = ttk.Frame(self.main_frame, bootstyle="light", padding=10)
        self.menu_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.display_items("Food")  # Show food items by default

        # Order Summary 
        self.summary_frame = ttk.Frame(self.main_frame, bootstyle="light", padding=10)
        self.summary_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        self.summary_label = ttk.Label(self.summary_frame, text="📝 Order Summary", font=("Montserrat", 16, "bold"),bootstyle="inverse-light")
        self.summary_label.pack(pady=5)

        self.summary_listbox = tk.Listbox(self.summary_frame, height=12, font=("Montserrat", 12), relief=tk.SOLID,borderwidth=2)
        self.summary_listbox.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)

        self.total_price_label = ttk.Label(self.summary_frame, text="Total: $0.00", font=("Montserrat", 14, "bold"),bootstyle="inverse-light")
        self.total_price_label.pack(pady=5)

        # Buttons for Actions
        self.btn_frame = ttk.Frame(self.summary_frame)
        self.btn_frame.pack(fill=tk.X, pady=5)

        self.discount_button = ttk.Button(self.btn_frame, text="Discount", bootstyle="success-outline", padding=5, command=self.apply_discount)
        self.discount_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.update_button = ttk.Button(self.btn_frame, text="Update", bootstyle="warning-outline", padding=5, command=self.update_menu)
        self.update_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.delete_button = ttk.Button(self.btn_frame, text="Delete", bootstyle="danger-outline", padding=5 , command=self.delete_order)
        self.delete_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.clear_button = ttk.Button(self.summary_frame, text="Clear Order", bootstyle="info-outline", padding=5, command=self.clear_order)
        self.clear_button.pack(fill=tk.X, padx=5, pady=5)

        self.checkout_button = ttk.Button(self.summary_frame, text="Checkout", bootstyle="primary-outline", padding=5,command=self.checkout)
        self.checkout_button.pack(fill=tk.X, padx=5, pady=5)

        self.save_receipt_button = ttk.Button(self.summary_frame, text="Save Receipt", bootstyle="success-outline",padding=5, command=self.save_receipt)
        self.save_receipt_button.pack(fill=tk.X, padx=5, pady=5)

    def update_menu(self, category):
        """Clear menu & update items based on selected category."""
        self.display_items(category)

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

    def open_addons_popup(self, item_name, price):
        """Open a popup window for selecting add-ons."""
        # TODO: Implement open_addons_popup logic
        popup = tk.Toplevel(self.root)
        popup.title(f"Add-ons for {item_name}")
        popup.geometry("400x300")
        popup.grab_set()  # Make popup modal

        addons = [
        {"name": "Extra Cheese", "price": 20},
        {"name": "Bacon", "price": 30},
        {"name": "Mushrooms", "price": 15},
        {"name": "Onions", "price": 10},
    ]
        
        addon_vars = []
        ttk.Label(popup, text="Select Add-ons:", font=("Arial",12,"bold")).pack(pady=19)

        for addon in addons:
            var = tk.IntVar()
            chk = ttk.Checkbutton(
                popup,
                text=f"{addon['name']} (+${addon['price']})",
                variable=var
            )
            chk.pack(anchor='w', padx=20)
            addon_vars.append((var, addon))
        
        def confirm_addons():
            total_addon_price = 0
            selected_addons = []

            for var, addon in addon_vars:
                if var.get():
                    total_addon_price += addon['price']
                    selected_addons.append(addon['name'])
            
            final_price = price + total_addon_price
            summary = f"Item: {item_name}\nBase Price: ${price}\n\n"
            if selected_addons:
                summary += "Add-ons:\n" + "\n".join(f"- {a}" for a in selected_addons)
                summary +=f"\n\nAdd-ons Total: ${total_addon_price}\n"
            else:
                summary += "No Add-ons Selected.\n"
            
            summary += f"\nFinal Price: ${final_price}"

            Messagebox.show_info("Order Summary", summary)
            popup.destroy()

            ttk.Button(popup, text="Confirm", command=confirm_addons),pack(pady=15)

            popup.mainloop()

    
    def add_to_order(self, item_name, price):
        """Add selected item to order summary with add-ons."""
        self.logic.add_to_order(item_name, price)  # Use logic to add item
        self.update_summary()

    def update_order(self, item_index=None, new_quantity=None, new_price=None):
        """Update selected item details in order summary."""
        # TODO: Delegate to OrderingSystemLogic
        if item_index is not None and 0 <= item_index < len(self.order_items):
            item = self.order_items[item_index]
            if new_quantity is not None:
                item['quantity'] = new_quantity
            if new_price is not None:
                item['price'] = new_price
            print(f"Updated item: {item}")
        else:
            print("Invalid item index or no update parameters provided.")

    def delete_order(self):
        """Remove selected item from order summary."""
        try:
            selected_index = self.summary_listbox.curselection()
            if selected_index:
                index = selected_index[0]
                self.logic.delete_order(index)
                self.update_summary()
            else:
                Messagebox.show_warning("Please select an item to delete!", "Warning")
        except Exception as e:
            print(f"Error in delete_order: {e}")

    def clear_order(self):
        """Clear all selected items and reset total price."""
        self.logic.clear_order()
        self.update_summary()

    def checkout(self):
        """Calculate total price and process checkout."""
        self.logic.checkout()
        self.update_summary()

    def save_receipt(self):
        """Save the receipt to a file."""
        self.logic.save_receipt()

    def apply_discount(self, discount=None, code=None):
        discount_codes = {
            'SAVEPHP10': 10,
            'SAVE20': 20,
            'HALFOFF': 50
        }

        if code:
            if code in discount_codes:
                discount = discount_codes[code]
                print(f"Code '{code}' applied: {discount}% off")
            else:
                print("Invalid code.")
                return

        if discount:
            if 0 < discount <= 100:
                discount_codes = (discount / 100) * self.total_cost
                self.total_cost -= discount_codes
                print(f"Discount applied. New total: ${self.total_cost:.2f}")
            else:
                print("Invalid discount percentage.")
        else:
            print("No discount applied.")

    def update_summary(self):
        """Update the order summary listbox and total price label."""
        # TODO: Fix formating for receipt
        self.summary_listbox.delete(0, tk.END)  # Clear listbox
        total_width = 25  # Adjust this width as needed for balance

        for item, price, addons in self.logic.order:
            dot_count = total_width - len(item) - len(f"${price:.2f}")  # Calculate dot count dynamically
            dots = "." * dot_count  # Generate dots
            formatted_item = f"{item} {dots} ${price:.2f}"  # Proper alignment
            self.summary_listbox.insert(tk.END, formatted_item)

        self.total_price_label.config(text=f"Total: ${self.logic.total_price:.2f}")  # Update total price


if __name__ == "__main__":
    root = tk.Tk()
    icon_path = os.path.join(os.path.dirname(__file__), "img", "Logo.ico")
    root.iconbitmap(icon_path)
    app = OrderingSystemGUI(root)
    root.mainloop()