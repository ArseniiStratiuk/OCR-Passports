import tkinter as tk
import sys

import customtkinter as ctk

ctk.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue".
ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light".


class Window(ctk.CTk):

    WIDTH = 1242
    HEIGHT = 720
    
    LARGE_FONT = ("Calibri", 24, "bold")
    MEDIUM_FONT = ("Calibri", 18, "bold")
    SMALL_FONT = ("Calibri", 14, "bold")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.WINDOW_CENTERING_X = int(self.winfo_screenwidth()/2 - self.WIDTH/2)
        self.WINDOW_CENTERING_Y = int(self.winfo_screenheight()/2 - self.HEIGHT/2)
        
        self.title("OCR Passport")
        self.geometry(
            f"{self.WIDTH}x{self.HEIGHT}+{self.WINDOW_CENTERING_X}+{self.WINDOW_CENTERING_Y}"
        )
        self.protocol(
            "WM_DELETE_WINDOW", self.on_closing
        )  # Call .on_closing() when app gets closed
        
    def on_closing(self, event=0):
        self.destroy()
        
        
if __name__ == "__main__":
    root = Window()
    root.mainloop()