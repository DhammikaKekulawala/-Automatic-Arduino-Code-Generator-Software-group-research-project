# Python is used to import all the public names (functions, classes, variables, etc.) defined in the Tkinter module
# into the current namespace. Tkinter is a standard Python GUI (Graphical User Interface) toolkit used for creating
# GUI applications.
from tkinter import *

# ttk is a module that is used to style the tkinter widgets. Just like CSS is used to style an HTML element,
# we use tkinter. ttk to style tkinter widgets.
from tkinter import ttk  # If I remove this I cannot add styles to the progressbar

# it lets the user interact with the native OS Python is currently running on. In simple terms, it provides an easy
# way for the user to interact with several os functions that come in handy in day to day programming.
import os  # if I remove this I cannot close this window nd open welcome screen window


class ArduinoCodeGenerator:
    def __init__(self, master):
        self.master = master
        self.master.title("Arduino Code Generator")
        self.master.geometry("350x300")
        self.master.resizable(False, False)

        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width // 2) - (350 // 2)
        y = (screen_height // 2) - (300 // 2)
        self.master.geometry("+{}+{}".format(x, y))

        # Hide the window decorations
        self.master.overrideredirect(True)

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        # Create the "Arduino Code Generator" label
        self.welcome_label = Label(self.master, text="Arduino Code Generator", font=("Times New Roman", 15, "bold"),
                                   fg="#000000", bg="silver")
        self.welcome_label.place(x=130, y=35)

        # Create the image label
        self.image = PhotoImage(file="Images//logo.png")
        self.bg_label = Label(self.master, image=self.image, bg="silver")
        self.bg_label.place(x=190, y=65)

        # Create the progressbar label
        self.progress_label = Label(self.master, text="", font=("Times New Roman", 10, "bold"), fg="black",
                                    bg="silver")
        self.progress_label.place(x=220, y=173)

        # Create the progressbar
        self.progress = ttk.Progressbar(self.master, orient=HORIZONTAL, length=90, mode='determinate',
                                        style="red.Horizontal.TProgressbar")
        self.progress.place(x=190, y=155)

        # Configure the progressbar style
        self.progress_style = ttk.Style()
        self.progress_style.theme_use('clam')
        self.progress_style.configure("red.Horizontal.TProgressbar", background="blue", troughcolor="silver")

    def start(self):
        # Start the progressbar
        self.progress.start(10)

    def stop(self):
        # Stop the progressbar
        self.progress.stop()

    def update_progress(self, value):
        # Update the progressbar value
        self.progress['value'] = value
        self.progress_label.config(text='{}%'.format(value))

    def close(self):
        # Close the window and open the WelcomeWindow
        self.master.withdraw()
        os.system("python WelcomeWindow.py")
        self.master.destroy()


if __name__ == '__main__':
    root = Tk()
    app = ArduinoCodeGenerator(root)
    app.start()

    i = 0
    while i <= 100:
        app.update_progress(i)
        i += 1
        app.master.update_idletasks()
        app.master.after(100)

    app.stop()
    app.close()
