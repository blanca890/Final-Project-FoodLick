from tkinter import *
from PIL import Image, ImageTk
import os
import ttkbootstrap as ttk  # Import ttkbootstrap for modern styling

def Create():
    pass

def Read():
    pass

def Update():
    pass

def Delete():
    pass

def Exit():
    pass

def create_file():
    pass

def read_file():
    pass

def update_file():
    pass

def delete_file():
    pass

# Create the main window with ttkbootstrap styling
sc = ttk.Window(themename="superhero")  # Choose a theme (e.g., "superhero", "darkly", "flatly")
sc.geometry("900x400+400+200")
sc.title("FoodLick")

compFont = ("Arial", 14)

try:
    # Ensure the image file exists
    image_path = os.path.join("img", "Banner.jpg")
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    # Open and resize the image
    LogoTopBanner = Image.open(image_path)
    LogoTopBanner = LogoTopBanner.resize((710, 100), Image.Resampling.LANCZOS)
    LogoTopBanner = ImageTk.PhotoImage(LogoTopBanner)

    logo_right = os.path.join("img", "Logo.png")
    if not os.path.exists(logo_right):
        raise FileNotFoundError(f"Image file not found: {logo_right}")
    
    LogoRight = Image.open(logo_right)
    LogoRight = LogoRight.resize((100, 100), Image.Resampling.LANCZOS)
    LogoRight = ImageTk.PhotoImage(LogoRight)

    # Create a frame to hold the banner and the exit button
    top_frame = ttk.Frame(sc, bootstyle="secondary")
    top_frame.pack(fill=X, pady=10)

    # Add the Exit button to the left side of the frame
    exit_button = ttk.Button(top_frame, text="Exit", command=sc.destroy, bootstyle="danger")
    exit_button.pack(side=LEFT, padx=10, anchor="w")

    # Display the image in a Label widget beside the button
    LogoTopBannerLabel = Label(top_frame, image=LogoTopBanner, borderwidth=2, relief="solid")
    LogoTopBannerLabel.image = LogoTopBanner
    LogoTopBannerLabel.pack(side=LEFT, padx=10)

    # Display the logo on the right side
    LogoRightLbl = Label(top_frame, image=LogoRight)
    LogoRightLbl.image = LogoRight
    LogoRightLbl.pack(side=RIGHT, padx=10)

    # On the left side, create a rectangle frame for the menus and the data
    left_frame = ttk.Frame(sc, bootstyle="secondary")
    left_frame.pack(fill=Y, side=LEFT, padx=10)

    # Create a frame for the dropdown button and center it
    dropdown_frame = ttk.Frame(left_frame, bootstyle="secondary", width=200, height=100)
    dropdown_frame.pack_propagate(False)
    dropdown_frame.pack(pady=100, padx=10, anchor="center")

    # Create a frame for the dropdown button at the top center
    menu_frame = ttk.Frame(sc, bootstyle="secondary")
    menu_frame.pack(fill=X, pady=10)  # Place the frame at the top with padding

    # Create the dropdown button inside the menu frame
    dropdownbtn = ttk.Menubutton(
        menu_frame, 
        text="Menu", 
        bootstyle="success-outline",  # Use a modern outline style
        width=20
    )
    dropdownbtn.pack(pady=10)  # Center the button vertically within the frame

    # Configure the dropdown menu
    dropdownbtn.menu = Menu(dropdownbtn, tearoff=0)  # Disable the tear-off feature for a cleaner look
    dropdownbtn["menu"] = dropdownbtn.menu
    dropdownbtn.menu.add_command(label="🍝 Pasta", command=Create)  # Add emojis for a modern touch
    dropdownbtn.menu.add_command(label="🍗 Chicken", command=Create)
    dropdownbtn.menu.add_command(label="🍕 Pizza", command=Create)
    dropdownbtn.menu.add_command(label="🍜 Lomi", command=Create)
    dropdownbtn.menu.add_separator()  # Add a separator for better organization
    dropdownbtn.menu.add_command(label="❌ Exit", command=sc.destroy)
except FileNotFoundError as fnf_error:
    print(fnf_error)
    error_label = ttk.Label(sc, text="Image file not found!", font=compFont, bootstyle="danger")
    error_label.pack()
except Exception as e:
    print(f"Error loading image: {e}")
    error_label = ttk.Label(sc, text="Error loading image", font=compFont, bootstyle="danger")
    error_label.pack()

sc.mainloop()