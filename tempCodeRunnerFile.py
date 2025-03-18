from tkinter import *
from PIL import Image, ImageTk
import os

sc = Tk()
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
    LogoTopBanner = LogoTopBanner.resize((600, 100), Image.Resampling.LANCZOS)  # Updated resizing method
    LogoTopBanner = ImageTk.PhotoImage(LogoTopBanner)

    top_frame = Frame(sc)
    top_frame.pack(fill=X, padx=10)

    # Display the image in a Label widget
    LogoTopBannerLabel = Label(image=LogoTopBanner)
    LogoTopBannerLabel.image = LogoTopBanner
    LogoTopBannerLabel.pack()

    # Exit button beside the banner
    exit_button = Button(top_frame, text="Exit", font=compFont, command=exit, bg="red", fg="white")
    exit_button.pack(side=LEFT, padx=5)

except FileNotFoundError as fnf_error:
    print(fnf_error)
    error_label = Label(sc, text="Image file not found!", font=compFont, fg="red")
    error_label.pack()
except Exception as e:
    print(f"Error loading image: {e}")
    error_label = Label(sc, text="Error loading image", font=compFont, fg="red")
    error_label.pack()


sc.mainloop()