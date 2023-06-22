import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import object_detection3 as object_de
import code_generate4 as code_g


class ImageUploader:
    def __init__(self, master):
        self.master = master
        master.title("Image Uploader")

        # set the window size
        master.geometry("1400x800")

        # create a frame to hold the buttons
        button_frame = tk.Frame(master)
        button_frame.pack(side=tk.BOTTOM, pady=10)

        # create the widgets
        self.upload_button = tk.Button(button_frame, text="Select Image", command=self.upload_image)
        self.upload_button.pack(side=tk.LEFT, padx=10)

        self.save_button = tk.Button(button_frame, text="Save Image", command=self.save_image)
        self.save_button.pack(side=tk.LEFT, padx=10)

        self.remove_button = tk.Button(button_frame, text="Remove Image", command=self.remove_image)
        self.remove_button.pack(side=tk.LEFT, padx=10)

        self.cancel_button = tk.Button(button_frame, text="Cancel", command=self.master.destroy)
        self.cancel_button.pack(side=tk.RIGHT, padx=10)

        self.cancel_button = tk.Button(button_frame, text="Code_generater", command=self.code_generator)
        self.cancel_button.pack(side=tk.RIGHT, padx=10)

        self.image_label = tk.Label(master)
        self.values_label = tk.Label(master)

        self.values = {}

    def upload_image(self):
        # ask user to select an image
        file_path = filedialog.askopenfilename(title="Select Image")

        if file_path:
            # open the selected image
            image = Image.open(file_path)

            # resize the image to fit the label
            max_size = (1200, 600)
            image.thumbnail(max_size)

            # convert image to Tkinter-compatible format
            photo = ImageTk.PhotoImage(image)

            # display the image
            self.image_label.config(image=photo)
            self.image_label.image = photo
            self.selected_image = image

        # pack the image label into the window
        self.image_label.pack()

    def remove_image(self):
        self.image_label.config(image='')
        self.values_label.config(text='')
        del self.selected_image
        self.values = {}

    def save_image(self, quality=95):
        # check if an image has been selected
        if hasattr(self, 'selected_image'):
            # get the directory of the script
            script_dir = os.path.dirname(__file__)

            # create the full save path with the filename
            full_path = f"{script_dir}/pin/save.png"

            # save the image with the specified quality level
            self.selected_image.save(full_path, quality=quality)
            print(f"Image saved to {full_path}")
            self.values = self.object()
            print(self.values)
            self.show_predicted_image()


        else:
            print("No image selected")

    def object(self):
        self.value = {}
        n = "pin/save.png"
        self.value = object_de.object_detect(n)
        print(self.value)
        return self.value

    def show_predicted_image(self):
        # remove the old label from the window
        self.image_label.pack_forget()

        # create a new label to display the predicted image
        predicted_image = Image.open("prediction.jpg")
        max_size = (600, 600)
        predicted_image.thumbnail(max_size)
        predicted_photo = ImageTk.PhotoImage(predicted_image)
        predicted_label = tk.Label(self.master, image=predicted_photo)
        predicted_label.image = predicted_photo
        predicted_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # create the table to display the values
        table_frame = tk.Frame(self.master)
        table_frame.pack(side=tk.BOTTOM, pady=10)

        # create the table header
        tk.Label(table_frame, text="Object").grid(row=0, column=0)
        tk.Label(table_frame, text="pin_name").grid(row=0, column=1)

        # display the values in the table
        row_index = 1
        for object_name, confidence in self.values.items():
            tk.Label(table_frame, text=object_name).grid(row=row_index, column=0)
            tk.Label(table_frame, text=confidence).grid(row=row_index, column=1)
            row_index += 1

    def remove_image(self):
        self.image_label.config(image='')
        self.values_label.config(text='')
        self.selected_image = None
        self.values = {}

    def code_generator(self):
        devices = {}
        self.ss = {}
        devices = self.values
        self.ss = code_g.upload_values(devices)
        #print(self.devices)




    #def devices_value(self):
        #self.devices = {'Arduino': 0, 'LED': 0, 'Laser': 0}
        #self.devicess = {}
        #self.devicess = object_de.devices_values(self.devices)
        #print(self.devicess)
        #return self.devicess


def main():
    root = tk.Tk()
    app = ImageUploader(root)
    root.mainloop()


if __name__ == '__main__':
    main()
