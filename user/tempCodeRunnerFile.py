    def animate_title_color(self):
        """Animate the title label's color."""
        current_color = self.banner_label.cget("foreground")
        new_color = "blue" if current_color == "black" else "black"
        self.banner_label.config(foreground=new_color)
        self.root.after(10, self.animate_title_color)  # Repeat every 500ms
