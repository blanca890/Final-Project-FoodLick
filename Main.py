from tkinter import *
from PIL import Image, ImageTk
import os

def Create(): ##TODO: Create a new window for the user to input the data
    pass

 #TODO:Read the data from the user
def Read():
    pass

def Update(): #TODO: Update the data
    pass

def Delete(): #TODO: Delete the data
    pass

def  Exit(): #TODO: Exit the program
    pass

def create_file()#TODO: Create a file to store the data
    pass

def read_file()#TODO: Read the data from the file
    pass

def update_file()#TODO: Update the data in the file
    pass

def delete_file()#TODO: Delete the data in the file
    pass



# Create the main window
sc = Tk()
sc.geometry("900x400+400+200")  
sc.title("FoodLick")  

compFont = ("Arial", 14)

try:
    # Ensure the image file exists
    image_path = os.path.join("img", "Banner.jpg", )
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    # Open and resize the image
    LogoTopBanner = Image.open(image_path)
    LogoTopBanner = LogoTopBanner.resize((710, 100), Image.Resampling.LANCZOS)  # Updated resizing method
    LogoTopBanner = ImageTk.PhotoImage(LogoTopBanner)

    logo_right = os.path.join("img", "Logo.png")
    if not os.path.exists(logo_right):
        raise FileNotFoundError(f"Image file not found: {logo_right}")
    
    LogoRight = Image.open(logo_right)
    LogoRight = LogoRight.resize((100, 100), Image.Resampling.LANCZOS)
    LogoRight = ImageTk.PhotoImage(LogoRight)

    # Create a frame to hold the banner and the exit button
    top_frame = Frame(sc)
    top_frame.pack(fill=X, pady=10)

    # Add the Exit button to the left side of the frame
    exit_button = Button(top_frame, text="Exit", font=compFont, command=sc.destroy, bg="red", fg="white")
    exit_button.pack(side=LEFT, padx=10, anchor="w")  # Anchor to the west (left)

    # Display the image in a Label widget beside the button
    LogoTopBannerLabel = Label(top_frame, image=LogoTopBanner)
    LogoTopBannerLabel.image = LogoTopBanner
    LogoTopBannerLabel.pack(side=LEFT, padx=10)  # Place the banner to the right of the button

    #Display the logo on the right side
    LogoRightLbl=Label(top_frame, image=LogoRight)
    LogoRightLbl.image=LogoRight
    LogoRightLbl.pack(side=RIGHT, padx=10)
    

except FileNotFoundError as fnf_error:
    print(fnf_error)
    error_label = Label(sc, text="Image file not found!", font=compFont, fg="red")
    error_label.pack()
except Exception as e:
    print(f"Error loading image: {e}")
    error_label = Label(sc, text="Error loading image", font=compFont, fg="red")
    error_label.pack()


sc.mainloop()