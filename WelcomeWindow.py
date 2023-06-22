import subprocess
import tkinter as tk
from tkinter import filedialog

from PIL import Image, ImageTk


class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Arduino Code Generator")
        self.master.resizable(False, False)

        p1 = tk.PhotoImage(file='Images/logo.png')
        master.iconphoto(True, p1)

        self.canvas = tk.Canvas(self.master, width=800, height=500)
        self.canvas.pack()
        self.create_background()
        self.create_widgets()

    def create_background(self):
        bg_image = tk.PhotoImage(file='Images/welcome_background.png')
        self.canvas.create_image(0, 0, anchor='nw', image=bg_image)
        self.canvas.image = bg_image

    def create_widgets(self):
        self.welcome_label = tk.Label(self.master, text="Arduino Code Generator", font=("Times New Roman", 15, "bold"), fg="black")
        self.welcome_label.place(x=285, y=25)

        image = Image.open("Images/logo.png")
        image = image.resize((150, 150))
        photo = ImageTk.PhotoImage(image)

        label = tk.Label(root, image=photo)
        label.image = photo
        label.place(x=330, y=80)

        self.create_new_button = tk.Button(self.master, text="Create New Project", font=("Times New Roman", 12, "bold"), fg="black", padx=10, pady=5, command=open_create_window)
        self.create_new_button.place(x=180, y=310)

        self.create_new_button = tk.Button(self.master, text="Open Project", font=("Times New Roman", 12, "bold"), fg="black", padx=29, pady=5, command=open_existing_project)
        self.create_new_button.place(x=480, y=310)

        self.create_new_button = tk.Button(self.master, text="Upload an Image", font=("Times New Roman", 12, "bold"), fg="black", padx=18, pady=5, command=open_image_upload, compound="left")
        self.create_new_button.place(x=330, y=390)

        self.welcome_label = tk.Label(self.master, text="Copyright © 2023. All rights reserved. Design by team 'InSys Xperts', Rajarata University of Sri Lanka", font=("Trebuchet Ms", 6, "bold italic"), fg="white", bg="grey")
        self.welcome_label.place(x=200, y=480)


def open_create_window():
    subprocess.Popen(["python", "workingarea.py"])
    # root.destroy()
    root.withdraw()


def open_existing_project():
    filename = filedialog.askopenfilename()
    print(filename)  # Do something with the selected file here


def open_image_upload():
    subprocess.Popen(["python", "window15.py"])


if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

