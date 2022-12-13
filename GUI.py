import tkinter as tk
import os
import sys

import customtkinter as ctk
from PIL import Image

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
        
        self.iconbitmap(os.path.join(sys.path[0]+"\Icons", "Check_MRZ_Light.ico"))
        
        self.WINDOW_CENTERING_X = int(self.winfo_screenwidth()/2 - self.WIDTH/2)
        self.WINDOW_CENTERING_Y = int(self.winfo_screenheight()/2 - self.HEIGHT/2)
        
        self.title("OCR Passport")
        self.geometry(
            f"{self.WIDTH}x{self.HEIGHT}+{self.WINDOW_CENTERING_X}+{self.WINDOW_CENTERING_Y}"
        )
        self.protocol(
            "WM_DELETE_WINDOW", self.on_closing
        )  # Call .on_closing() when app gets closed
        
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.grid_columnconfigure((0, 1, 2), weight=1)
        
        self.create_widgets()
        
    def create_widgets(self):
        """
        Fill the window with widgets.
        """
        self.label_1 = ctk.CTkLabel(self, text="Оптичне розпізнавання\nсимволів Вашого\nпаспорта", 
                                    font=self.LARGE_FONT)
        self.label_1.grid(row=0, column=0, padx=10, pady=20)
        
        self.label_2 = ctk.CTkLabel(self, text="Оберіть фотографію\nпаспорта", 
                                    font=self.LARGE_FONT)
        self.label_2.grid(row=0, column=3, padx=10, pady=20)
        
        self.button = ctk.CTkButton(self, text="", width=75, height=70, corner_radius=10, 
                                    )
        
    def on_closing(self, event=0):
        self.destroy()
        
        
if __name__ == "__main__":
    root = Window()
    root.mainloop()