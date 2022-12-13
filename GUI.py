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
    
    LARGE_FONT = ("Calibri", 34)
    MEDIUM_FONT = ("Calibri", 28)
    SMALL_FONT = ("Calibri", 20)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Upload images that will be used in the program.
        self.ARROW_DARK = Image.open(os.path.join(sys.path[0]+"\Icons", "Arrow_Dark.png"))
        self.ARROW_LIGHT = Image.open(os.path.join(sys.path[0]+"\Icons", "Arrow_Light.png"))
        self.arrow = ctk.CTkImage(self.ARROW_DARK, self.ARROW_LIGHT, (100, 100))
        
        self.CHECK_MRZ_DARK = Image.open(os.path.join(sys.path[0]+"\Icons", "Check_MRZ_Dark.png"))
        self.CHECK_MRZ_LIGHT = Image.open(os.path.join(sys.path[0]+"\Icons", "Check_MRZ_Light.png"))
        self.check_mrz = ctk.CTkImage(self.CHECK_MRZ_DARK, self.CHECK_MRZ_LIGHT, (100, 100))
        
        self.LOADING_DARK = Image.open(os.path.join(sys.path[0]+"\Icons", "Loading_Dark.png"))
        self.LOADING_LIGHT = Image.open(os.path.join(sys.path[0]+"\Icons", "Loading_Light.png"))
        self.loading_image = ctk.CTkImage(self.LOADING_DARK, self.LOADING_LIGHT, (100, 100))
        # --------------------------------------------------
        
        self.iconbitmap(os.path.join(sys.path[0]+"\Icons", "Check_MRZ_Light.ico"))
        
        self.WINDOW_CENTERING_X = int(self.winfo_screenwidth()/2 - self.WIDTH/2)
        self.WINDOW_CENTERING_Y = int(self.winfo_screenheight()/2 - self.HEIGHT/2)
        
        self.title("OCR Your Passport")
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
        self.label_2.grid(row=0, column=2, padx=10, pady=20)
        
        self.button = ctk.CTkButton(self, text="", width=85, height=75, corner_radius=10, 
                                    image=self.check_mrz)
        self.button.grid(row=1, column=2, padx=10, pady=20)
        
        self.loading = ctk.CTkLabel(self, text="Результати\nзавантажуються...", compound="left", 
                                    font=self.SMALL_FONT, image=self.loading_image)
        self.loading.grid(row=1, column=0, padx=10, pady=20)
        
    def on_closing(self, event=0):
        self.destroy()
        
        
if __name__ == "__main__":
    root = Window()
    root.mainloop()