from tkinter.filedialog import askopenfilename
import os
import sys
import threading

import customtkinter as ctk
import PIL
from PIL import Image

from ocr_passport import ocr_passport

ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue".
ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light".


class Window(ctk.CTk):

    WIDTH = 1431
    HEIGHT = 789
    
    LARGE_FONT = ("Calibri Light", 42)
    MEDIUM_FONT = ("Calibri Light", 32)
    SMALL_FONT = ("Calibri Light", 28)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Upload images that will be used in the program.
        self.ARROW_DARK = Image.open(os.path.join(sys.path[0]+"\Icons", "Arrow_Dark.png"))
        self.ARROW_LIGHT = Image.open(os.path.join(sys.path[0]+"\Icons", "Arrow_Light.png"))
        self.arrow_image = ctk.CTkImage(self.ARROW_DARK, self.ARROW_LIGHT, (100, 100))
        
        self.CHECK_MRZ_DARK = Image.open(os.path.join(sys.path[0]+"\Icons", "Check_MRZ_Dark.png"))
        self.CHECK_MRZ_LIGHT = Image.open(os.path.join(sys.path[0]+"\Icons", "Check_MRZ_Light.png"))
        self.check_mrz = ctk.CTkImage(self.CHECK_MRZ_DARK, self.CHECK_MRZ_LIGHT, (110, 110))
        
        self.LOADING_DARK = Image.open(os.path.join(sys.path[0]+"\Icons", "Loading_Dark.png"))
        self.LOADING_LIGHT = Image.open(os.path.join(sys.path[0]+"\Icons", "Loading_Light.png"))
        self.loading_image = ctk.CTkImage(self.LOADING_DARK, self.LOADING_LIGHT, (115, 115))
        # --------------------------------------------------
        
        self.iconbitmap(os.path.join(sys.path[0]+"\Icons", "Check_MRZ_Light.ico"))
        
        self.widgets = "not grided"
        
        self.WINDOW_CENTERING_X = int(self.winfo_screenwidth()/2 - self.WIDTH/2)
        self.WINDOW_CENTERING_Y = int(self.winfo_screenheight()/2 - self.HEIGHT/2)
        
        self.title("OCR Your Passport")
        self.geometry(
            f"{self.WIDTH}x{self.HEIGHT}+{self.WINDOW_CENTERING_X}+{self.WINDOW_CENTERING_Y}"
        )
        self.minsize(1365, 690)

        self.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.grid_columnconfigure((0, 1, 2), weight=1)
        
        self.create_widgets()
        
    def create_widgets(self):
        """
        Fill the window with widgets.
        """
        self.label_1 = ctk.CTkLabel(self, text="Оптичне розпізнавання\nсимволів Вашого\nпаспорта", 
                                    font=("Calibri Light", 42, "bold"), width=600)
        self.label_1.grid(row=0, column=0, padx=10, pady=(40, 30))
        
        self.label_2 = ctk.CTkLabel(self, text="Виберіть фотографію\nпаспорта", 
                                    font=self.LARGE_FONT, width=600)
        self.label_2.grid(row=0, column=2, padx=10, pady=(40, 30))
        
        self.button = ctk.CTkButton(self, text="", width=170, height=80, corner_radius=10, 
                                    image=self.check_mrz, command=self.set_mrz)
        self.button.grid(row=1, column=2, padx=10, pady=(0, 30))
        
        self.loading = ctk.CTkLabel(self, text="Результати\nзавантажуються...", compound="left", 
                                    font=self.SMALL_FONT, image=self.loading_image)
        
        self.frame = ctk.CTkFrame(self, height=330, width=600, fg_color="transparent", corner_radius=10)
        self.frame.grid(row=2, column=0, padx=10, pady=(0, 40))
        self.passport_label = ctk.CTkLabel(self.frame, text="", height=330, width=600)
        self.passport_label.pack()
        
        self.arrow = ctk.CTkLabel(self, text="", width=100)
        self.arrow.grid(row=2, column=1, padx=10, sticky="nswe")
        
        self.mrz_textbox = ctk.CTkTextbox(self, height=330, width=600, corner_radius=10, 
                                       font=("Consolas", 32, "bold"))
        
    def set_mrz(self):
        self.passport_path = askopenfilename(parent=self, title="Виберіть файл зображення")
        
        if self.passport_path:
            self.arrow.configure(image="")
            self.passport_label.configure(image=None)
            self.mrz_textbox.grid_remove()
            
            self.loading.grid(row=1, column=0, padx=10, pady=(0, 30))
            
            self.mrz_textbox.delete(0.0, "end")
            
            threading.Thread(target=self.mrz_to_text).start()
        
    def mrz_to_text(self):
        try:
            passport_photo = ctk.CTkImage(Image.open(self.passport_path), size=(600, 330))
            mrz_text = ocr_passport(self.passport_path)
            self.mrz_textbox.insert(0.0, mrz_text)
            
            if mrz_text != "":
                self.loading.grid_remove()
                self.passport_label.configure(image=passport_photo)
                self.arrow.configure(image=self.arrow_image)
                self.mrz_textbox.grid(row=2, column=2, padx=10, pady=(0, 40))
            else:
                self.loading.grid_remove()
                self.mrz_textbox.insert(0.0, "Неможливо завантажити результати\n\nMRZ не виявлено.")
                self.mrz_textbox.grid(row=2, column=2, padx=10, pady=(0, 40))
                
        except ValueError:
            self.loading.grid_remove()
            self.mrz_textbox.insert(0.0, "Неможливо завантажити результати\n\nВиберіть інше фото.")
            self.mrz_textbox.grid(row=2, column=2, padx=10, pady=(0, 40))
            
        except PIL.UnidentifiedImageError:
                self.loading.grid_remove()
                self.mrz_textbox.insert(0.0, "Неможливо завантажити результати\n\nВиберіть інший файл.")
                self.mrz_textbox.grid(row=2, column=2, padx=10, pady=(0, 40))
                
        except:
            self.loading.grid_remove()
            self.mrz_textbox.insert(0.0, "Неможливо завантажити результати\n\nСпробуйте ще раз.")
            self.mrz_textbox.grid(row=2, column=2, padx=10, pady=(0, 40))


if __name__ == "__main__":
    root = Window()
    root.mainloop()