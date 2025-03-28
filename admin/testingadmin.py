import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox
from PIL import Image, ImageTk
from admin.AdminGUI import GUIAdmin

class DummyLogic:
    """A dummy logic class to bypass admin validation."""
    def validate_admin(self, username, password):
        return True  # Always return True for testing purposes

if __name__ == "__main__":
    root = tk.Tk()
    logic = DummyLogic()
    # Instantiate the GUIAdmin class for testing
    GUIAdmin(root, logic)
    root.mainloop()