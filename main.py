from PIL import Image, ExifTags, ImageTk, UnidentifiedImageError
from tkinter import CENTER, RIGHT, filedialog
import customtkinter, screeninfo
from win10toast import ToastNotifier
import os

image_extensions = r"*.jpg *.jpeg *.png *.webp *.jfif *.pjpeg * .pjp"
root_ctk = customtkinter.CTk
customtkinter.set_default_color_theme("Red-Theme.json")

def get_monitor_from_coord(x, y):
    monitors = screeninfo.get_monitors()

    for m in reversed(monitors):
        if m.x <= x <= m.width + m.x and m.y <= y <= m.height + m.y:
            return m
    return monitors[0]

class GUI(root_ctk):
    def __init__(self):
        super().__init__()
        WIDTH = 650
        HEIGHT = 480
        self.title("Exif Scrapper")
        self.wm_iconbitmap("icon-512.ico")
        self.attributes('-topmost',True)
        self.minsize(WIDTH, HEIGHT)
        self.maxsize(WIDTH, HEIGHT)
        self.bind('<Escape>',lambda e: self.exit())
        current_screen = get_monitor_from_coord(self.winfo_x(), self.winfo_y())
        screen_width = current_screen.width
        screen_height = current_screen.height
        x_cord = int((screen_width / 2) - (WIDTH / 2))
        y_cord = int((screen_height / 2) - (HEIGHT / 2))
        self.geometry("{}x{}+{}+{}".format(WIDTH, HEIGHT, x_cord, y_cord))
        self.toast = ToastNotifier()

        self.iconimg = Image.open("icon.png").resize((100, 100))
        Frame1 = customtkinter.CTkFrame(self)
        Frame1.pack

        self.Frame2 = customtkinter.CTkFrame(self, 
                                                width=250, 
                                                height=725)
        self.Frame2.pack()
        self.Frame2.place(anchor="w", 
                            relx=0.0, 
                            rely=0.5, 
                            relwidth=0.28, 
                            relheight=1.1)
        
        self.Frame4 = customtkinter.CTkFrame(self.Frame2, 
                                            width=200, 
                                            height=155)                    
        self.Frame4.pack(expand= True)
        self.Frame4.place(anchor="n", 
                            relx=0.5, 
                            rely=0, 
                            relwidth=1, 
                            relheight=0.261)
        self.attributes('-topmost',False)

        self.icon_img = ImageTk.PhotoImage(self.iconimg)
        self.panel_icon = customtkinter.CTkLabel(self.Frame4, image=self.icon_img)
        self.panel_icon.place(relx=0.5, rely=0.58, anchor=CENTER)

        self.textbox = customtkinter.CTkTextbox(self, width=355, height=420, text_font=("Didot", 10, "bold"))
        self.textbox.grid(row=0, column=0)
        self.textbox.place(relx=0.63, rely=0.5, anchor=CENTER)

        self.button_get_Face = customtkinter.CTkButton(self.Frame2, 
                                                            width=150, 
                                                            height=50, 
                                                            border_width=0, 
                                                            corner_radius=8, 
                                                            hover=True, 
                                                            text="Start", 
                                                            command=self.get_EXIF, 
                                                            compound=RIGHT)
        self.button_get_Face.place(relx=0.5, rely=0.4, anchor=CENTER)
    
    def get_EXIF(self):
        try:
            image = filedialog.askopenfilename(title="Select image",
                                                filetypes=[("Supported: ", 
                                                image_extensions)])
            name = os.path.basename(image)
            img = Image.open(image)
        except UnidentifiedImageError:
            self.toast.show_toast(
                "EXS",
                f'File Not supported',
                duration = 4,
                icon_path = "icon-512.ico",
                threaded = True,)
            pass
        else:
            img_exif = img.getexif()
            self.textbox.insert("end", f"##### {name} #####\n\n")
            if len(img_exif) == 0:
                self.textbox.insert("end", f"{name} has no EXIF data\n")
            for key, val in img_exif.items():
                if key in ExifTags.TAGS:
                    if f'{ExifTags.TAGS[key]}:{val}'.startswith("DateTime"):
                        self.textbox.insert(f"end", f'* {ExifTags.TAGS[key]}:{val}\n'.replace("eT" and ":", "e T" and ": ", 1))
                    else:
                        self.textbox.insert("end", f'* {ExifTags.TAGS[key]}:{val}\n'.replace(":", ": "))
            self.textbox.insert(f"end", "\n##### Done! #####\n\n")



if __name__ == "__main__":
    app = GUI()
    app.mainloop()