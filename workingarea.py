
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import Arduino_Code_Create as acc


class ImageCanvas:
    def __init__(self, master):
        self.master = master
        self.master.state("zoomed")
        self.master.minsize(1520, 820)
        self.master.title("Arduino Code Generator")
        # Setting icon of master window
        p1 = tk.PhotoImage(file='Images/logo.png')
        master.iconphoto(False, p1)

        # set window color
        self.master.configure(bg='white')

        self.canvas = tk.Canvas(master, width=1222, height=815, bg='white')
        self.canvas.place(x=309, y=0)

        self.images = []
        self.image_ids = []
        self.anchor_point_ids = []
        self.image_index = -1
        self.image_id = None
        self.points = []
        self.object_names = []
        self.dragging = False
        self.drag_start_x = None
        self.drag_start_y = None
        self.selected_image_id = None  # initialize selected_image_id to None
        self.laser_counter = 0
        self.led_counter = 0
        self.uno_counter = 0
        self.line_start = None
        self.line_end = None
        self.lines = []
        self.prev_anchor_point_id = None
        self.current_object_name = None
        self.line_anchor_points = {}
        self.line_ids = {}
        self.final = {}
        self.send_dic = {}
        self.device_data = {}  # new instance variable to hold all device data
        self.uno_pin_data = {}  # new instance variable to hold all uno pin data
        self.swapped_send_dic = {}
        self.code_dictionary = {}
        self.final_led_count = 0
        self.final_laser_count = 0
        self.line_counter = 0

        # Add a tag to each line that is drawn
        self.line_tag_prefix = 'line'
        self.line_tag_counter = 0
        # self.canvas.bind('<Button-3>', self.delete_line)

        self.icons = {}

        # create File menu and its submenus
        menu = tk.Menu(master)
        file_menu = tk.Menu(menu, tearoff=0)
        file_menu.add_command(label="New Project", command=self.new_project, image=self._get_icon("Icons/New.png"), compound="left")
        file_menu.add_command(label="Open Project", command=self.open_project, image=self._get_icon("Icons/Open.png"), compound="left")
        file_menu.add_command(label="Save Project", command=self.save_project, image=self._get_icon("Icons/Save.png"), compound="left")
        file_menu.add_separator()
        file_menu.add_command(label="Settings", command=self.settings, image=self._get_icon("Icons/Settings.png"), compound="left")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit, image=self._get_icon("Icons/Cancel.png"), compound="left")
        menu.add_cascade(label="File", menu=file_menu)

        # create Help menu and its submenus
        help_menu = tk.Menu(menu, tearoff=0)
        help_menu.add_command(label="Devices", command=self.devices, image=self._get_icon("Icons/Electronic Devices.png"), compound="left")
        help_menu.add_command(label="How to Use", command=self.how_to_use, image=self._get_icon("Icons/How to Use.png"), compound="left")
        help_menu.add_separator()
        help_menu.add_command(label="About", command=self.about, image=self._get_icon("Icons/About.png"), compound="left")
        menu.add_cascade(label="Help", menu=help_menu)

        master.config(menu=menu)

        self.wrapper1 = ttk.LabelFrame(self.master, style='Red.TLabelframe')
        self.wrapper1.place(x=0, y=80)

        self.mycanvas = tk.Canvas(self.wrapper1, bg='light gray', width=284, height=650)
        self.mycanvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.yscrollbar = ttk.Scrollbar(self.wrapper1, orient="vertical", command=self.mycanvas.yview)
        self.yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.mycanvas.config(yscrollcommand=self.yscrollbar.set)
        self.myframe = tk.Frame(self.mycanvas, bg='#F2F2F2')
        self.mycanvas.create_window((0, 0), window=self.myframe, anchor='nw')

        widgetbox = tk.Label(self.master, text="Widget Box", font=('Times New Roman', 28, 'bold'), bg="#7F7FFF", padx=60, pady=20)
        widgetbox.place(x=0, y=0)

        create_codebutton = tk.Button(self.master, text="Create Code", command=self.send_dictionary,font=('Times New Roman', 25, 'bold'), bg="#7F7FFF", padx=51, pady=2)
        create_codebutton.place(x=0, y=753)

        # Create images
        self.image1 = Image.open("Devices/Uno_original.png")
        self.image1 = ImageTk.PhotoImage(self.image1)

        self.image2 = Image.open("Devices/Red.png")
        self.image2 = ImageTk.PhotoImage(self.image2)

        self.image3 = Image.open("Devices/laser.png")
        self.image3 = ImageTk.PhotoImage(self.image3)

        # Add two labels with images to the scroll area
        label1 = tk.Label(self.myframe, image=self.image1)
        label1.image = self.image1  # keep a reference to prevent garbage collection
        label1.pack(pady=15)

        button1 = tk.Button(self.myframe, text="Add Arduino Uno R3", command=lambda: canvas.add_uno('Devices/Uno_original.png'), font=('Times New Roman', 15, 'bold'), fg="#96D9D9", bg="#00979C", padx=10, pady=5)
        button1.pack()

        label2 = tk.Label(self.myframe, image=self.image2)
        label2.image = self.image2  # keep a reference to prevent garbage collection
        label2.pack(pady=15)

        button2 = tk.Button(self.myframe, text="Add LED", command=lambda: canvas.add_LED('Devices/Red.png'), font=('Times New Roman', 15, 'bold'), fg="#96D9D9", bg="#00979C", padx=58, pady=5)
        button2.pack()

        label3 = tk.Label(self.myframe, image=self.image3)
        label3.image = self.image3  # keep a reference to prevent garbage collection
        label3.pack(pady=15)

        button3 = tk.Button(self.myframe, text="Add Laser", command=lambda: canvas.add_laser('Devices/laser.png'), font=('Times New Roman', 15, 'bold'), fg="#96D9D9", bg="#00979C", padx=52, pady=5)
        button3.pack()

        # Bind the <Configure> event of the frame to a method that updates the scroll region of the canvas
        self.myframe.bind("<Configure>", self.on_frame_configure)

        # Bind the <MouseWheel> event of the canvas to a method that updates the scrollbar
        self.mycanvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def quit(self):
        self.master.destroy()

    def _get_icon(self, filename):
        if filename not in self.icons:
            self.icons[filename] = tk.PhotoImage(file=filename)
        return self.icons[filename]

    def new_project(self):
        print("New project created")

    def open_project(self):
        print("Project opened")

    def save_project(self):
        print("Project saved")

    def settings(self):
        print("Settings opened")

    def devices(self):
        print("Devices information")

    def how_to_use(self):
        print("How to use information")

    def about(self):
        print("About information")

    def on_frame_configure(self, event):
        # Update the scroll region of the canvas to include the whole frame
        self.mycanvas.configure(scrollregion=self.mycanvas.bbox("all"))

    def on_mousewheel(self, event):
        # Scroll the canvas in response to the mouse wheel event
        self.mycanvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def add_laser(self, filename):
        self.laser_counter += 1
        laser_object_name = f"Laser {self.laser_counter}"
        self.object_names.append(laser_object_name)
        self.images.append(tk.PhotoImage(file=filename))
        self.image_index += 1
        image_id = self.canvas.create_image(100, 100, image=self.images[self.image_index], anchor='nw')
        laser_anchor_point_id1 = self.canvas.create_rectangle(105, 145, 115, 155, fill='black')
        laser_anchor_point_id2 = self.canvas.create_rectangle(105, 165, 115, 175, fill='black')
        laser_anchor_point_id3 = self.canvas.create_rectangle(105, 185, 115, 195, fill='black')

        self.canvas.itemconfig(laser_anchor_point_id1, tags=(laser_object_name, 'anchor_point'))
        self.canvas.itemconfig(laser_anchor_point_id2, tags=(laser_object_name, 'anchor_point'))
        self.canvas.itemconfig(laser_anchor_point_id3, tags=(laser_object_name, 'anchor_point'))
        self.image_ids.append(image_id)
        self.anchor_point_ids.append([laser_anchor_point_id1, laser_anchor_point_id2, laser_anchor_point_id3])
        self.canvas.tag_bind(image_id, '<Button-1>', self.start_drag)
        self.canvas.tag_bind(image_id, '<B1-Motion>', self.drag)

        self.line_anchor_points[laser_object_name] = {}
        self.line_anchor_points[laser_object_name] = {}
        self.line_ids[laser_object_name] = []

        self.canvas.tag_bind(laser_anchor_point_id1, '<Button-1>', lambda event: self.handle_anchor_point_click(event, laser_anchor_point_id1, laser_object_name))
        self.canvas.tag_bind(laser_anchor_point_id2, '<Button-1>', lambda event: self.handle_anchor_point_click(event, laser_anchor_point_id2, laser_object_name))
        self.canvas.tag_bind(laser_anchor_point_id3, '<Button-1>', lambda event: self.handle_anchor_point_click(event, laser_anchor_point_id3, laser_object_name))

        # print(f"{laser_object_name}")

        # add Laser data to instance variable dictionary
        self.device_data[laser_object_name] = [laser_anchor_point_id1, laser_anchor_point_id2, laser_anchor_point_id3]

        # print(self.device_data)

        self.run()

    def add_LED(self, filename):
        self.led_counter += 1
        led_object_name = f"LED {self.led_counter}"
        self.object_names.append(led_object_name)
        self.images.append(tk.PhotoImage(file=filename))
        self.image_index += 1
        image_id = self.canvas.create_image(100, 100, image=self.images[self.image_index], anchor='nw')

        led_anchor_point_id1 = self.canvas.create_rectangle(110, 280, 120, 290, fill='black')
        led_anchor_point_id2 = self.canvas.create_rectangle(122, 310, 132, 320, fill='black')

        self.canvas.itemconfig(led_anchor_point_id1, tags=(led_object_name, 'anchor_point'))
        self.canvas.itemconfig(led_anchor_point_id2, tags=(led_object_name, 'anchor_point'))

        self.image_ids.append(image_id)
        self.anchor_point_ids.append([led_anchor_point_id1, led_anchor_point_id2])
        self.canvas.tag_bind(image_id, '<Button-1>', self.start_drag)
        self.canvas.tag_bind(image_id, '<B1-Motion>', self.drag)

        self.line_anchor_points[led_object_name] = {}
        self.line_ids[led_object_name] = []

        self.canvas.tag_bind(led_anchor_point_id1, '<Button-1>', lambda event: self.handle_anchor_point_click(event, led_anchor_point_id1, led_object_name))
        self.canvas.tag_bind(led_anchor_point_id2, '<Button-1>', lambda event: self.handle_anchor_point_click(event, led_anchor_point_id2, led_object_name))

        # add LED data to instance variable dictionary
        self.device_data[led_object_name] = [led_anchor_point_id1, led_anchor_point_id2]

        # print(self.device_data)

        self.run()

    def add_uno(self, filename):
        # self.uno_counter += 1
        uno_object_name = "Uno"
        # uno_object_name = f"Uno {self.uno_counter}"
        self.object_names.append(uno_object_name)
        self.images.append(tk.PhotoImage(file=filename))
        self.image_index += 1
        image_id = self.canvas.create_image(100, 100, image=self.images[self.image_index], anchor='nw')
        uno_anchor_point_id1 = self.canvas.create_rectangle(115, 275, 122, 282, fill='black')
        uno_anchor_point_id2 = self.canvas.create_rectangle(115, 289, 122, 296, fill='black')
        uno_anchor_point_id3 = self.canvas.create_rectangle(115, 303, 122, 310, fill='black')
        uno_anchor_point_id4 = self.canvas.create_rectangle(115, 316, 122, 323, fill='black')
        uno_anchor_point_id5 = self.canvas.create_rectangle(115, 329, 122, 336, fill='black')
        uno_anchor_point_id6 = self.canvas.create_rectangle(115, 342, 122, 349, fill='black')
        uno_anchor_point_id7 = self.canvas.create_rectangle(115, 356, 122, 363, fill='black')
        uno_anchor_point_id8 = self.canvas.create_rectangle(115, 369, 122, 376, fill='black')
        uno_anchor_point_id9 = self.canvas.create_rectangle(115, 389, 122, 396, fill='black')
        uno_anchor_point_id10 = self.canvas.create_rectangle(115, 402, 122, 409, fill='black')
        uno_anchor_point_id11 = self.canvas.create_rectangle(115, 416, 122, 423, fill='black')
        uno_anchor_point_id12 = self.canvas.create_rectangle(115, 429, 122, 436, fill='black')
        uno_anchor_point_id13 = self.canvas.create_rectangle(115, 443, 122, 450, fill='black')
        uno_anchor_point_id14 = self.canvas.create_rectangle(115, 456, 122, 463, fill='black')

        # right side pins start

        uno_anchor_point_id15 = self.canvas.create_rectangle(361, 228, 368, 235, fill='black')
        uno_anchor_point_id16 = self.canvas.create_rectangle(361, 241, 368, 248, fill='black')
        uno_anchor_point_id17 = self.canvas.create_rectangle(361, 254, 368, 261, fill='black')
        uno_anchor_point_id18 = self.canvas.create_rectangle(361, 267, 368, 274, fill='black')
        uno_anchor_point_id19 = self.canvas.create_rectangle(361, 282, 368, 289, fill='black')
        uno_anchor_point_id20 = self.canvas.create_rectangle(361, 295, 368, 302, fill='black')
        uno_anchor_point_id21 = self.canvas.create_rectangle(361, 308, 368, 315, fill='black')
        uno_anchor_point_id22 = self.canvas.create_rectangle(361, 321, 368, 328, fill='black')
        uno_anchor_point_id23 = self.canvas.create_rectangle(361, 334, 368, 341, fill='black')
        uno_anchor_point_id24 = self.canvas.create_rectangle(361, 347, 368, 354, fill='black')
        uno_anchor_point_id25 = self.canvas.create_rectangle(361, 368, 368, 375, fill='black')
        uno_anchor_point_id26 = self.canvas.create_rectangle(361, 381, 368, 388, fill='black')
        uno_anchor_point_id27 = self.canvas.create_rectangle(361, 395, 368, 402, fill='black')
        uno_anchor_point_id28 = self.canvas.create_rectangle(361, 408, 368, 415, fill='black')
        uno_anchor_point_id29 = self.canvas.create_rectangle(361, 422, 368, 429, fill='black')
        uno_anchor_point_id30 = self.canvas.create_rectangle(361, 435, 368, 442, fill='black')
        uno_anchor_point_id31 = self.canvas.create_rectangle(361, 449, 368, 456, fill='black')
        uno_anchor_point_id32 = self.canvas.create_rectangle(361, 462, 368, 469, fill='black')

        # right side pins end

        self.canvas.itemconfig(uno_anchor_point_id1, tags=(uno_object_name, 'anchor_point'))
        self.canvas.itemconfig(uno_anchor_point_id2, tags=(uno_object_name, 'anchor_point'))
        self.canvas.itemconfig(uno_anchor_point_id3, tags=(uno_object_name, 'anchor_point'))
        self.canvas.itemconfig(uno_anchor_point_id4, tags=(uno_object_name, 'anchor_point'))
        self.canvas.itemconfig(uno_anchor_point_id5, tags=(uno_object_name, 'anchor_point'))
        self.canvas.itemconfig(uno_anchor_point_id6, tags=(uno_object_name, 'anchor_point'))
        self.canvas.itemconfig(uno_anchor_point_id7, tags=(uno_object_name, 'anchor_point'))
        self.canvas.itemconfig(uno_anchor_point_id8, tags=(uno_object_name, 'anchor_point'))
        self.canvas.itemconfig(uno_anchor_point_id9, tags=(uno_object_name, 'anchor_point'))
        self.canvas.itemconfig(uno_anchor_point_id10, tags=(uno_object_name, 'anchor_point'))
        self.canvas.itemconfig(uno_anchor_point_id11, tags=(uno_object_name, 'anchor_point'))
        self.canvas.itemconfig(uno_anchor_point_id12, tags=(uno_object_name, 'anchor_point'))
        self.canvas.itemconfig(uno_anchor_point_id13, tags=(uno_object_name, 'anchor_point'))
        self.canvas.itemconfig(uno_anchor_point_id14, tags=(uno_object_name, 'anchor_point'))

        #right side

        self.canvas.itemconfig(uno_anchor_point_id15, tags=(uno_object_name, 'anchor_point'))
        self.canvas.itemconfig(uno_anchor_point_id16, tags=(uno_object_name, 'anchor_point'))
        self.canvas.itemconfig(uno_anchor_point_id17, tags=(uno_object_name, 'anchor_point'))
        self.canvas.itemconfig(uno_anchor_point_id18, tags=(uno_object_name, 'anchor_point'))
        self.canvas.itemconfig(uno_anchor_point_id19, tags=(uno_object_name, 'anchor_point'))
        self.canvas.itemconfig(uno_anchor_point_id20, tags=(uno_object_name, 'anchor_point'))
        self.canvas.itemconfig(uno_anchor_point_id21, tags=(uno_object_name, 'anchor_point'))
        self.canvas.itemconfig(uno_anchor_point_id22, tags=(uno_object_name, 'anchor_point'))
        self.canvas.itemconfig(uno_anchor_point_id23, tags=(uno_object_name, 'anchor_point'))
        self.canvas.itemconfig(uno_anchor_point_id24, tags=(uno_object_name, 'anchor_point'))
        self.canvas.itemconfig(uno_anchor_point_id25, tags=(uno_object_name, 'anchor_point'))
        self.canvas.itemconfig(uno_anchor_point_id26, tags=(uno_object_name, 'anchor_point'))
        self.canvas.itemconfig(uno_anchor_point_id27, tags=(uno_object_name, 'anchor_point'))
        self.canvas.itemconfig(uno_anchor_point_id28, tags=(uno_object_name, 'anchor_point'))
        self.canvas.itemconfig(uno_anchor_point_id29, tags=(uno_object_name, 'anchor_point'))
        self.canvas.itemconfig(uno_anchor_point_id30, tags=(uno_object_name, 'anchor_point'))
        self.canvas.itemconfig(uno_anchor_point_id31, tags=(uno_object_name, 'anchor_point'))
        self.canvas.itemconfig(uno_anchor_point_id32, tags=(uno_object_name, 'anchor_point'))

        self.image_ids.append(image_id)
        self.anchor_point_ids.append([uno_anchor_point_id1, uno_anchor_point_id2, uno_anchor_point_id3, uno_anchor_point_id4, uno_anchor_point_id5, uno_anchor_point_id6, uno_anchor_point_id7, uno_anchor_point_id8, uno_anchor_point_id9, uno_anchor_point_id10, uno_anchor_point_id11, uno_anchor_point_id12, uno_anchor_point_id13, uno_anchor_point_id14, uno_anchor_point_id15, uno_anchor_point_id16, uno_anchor_point_id17, uno_anchor_point_id18, uno_anchor_point_id19, uno_anchor_point_id20, uno_anchor_point_id21, uno_anchor_point_id22, uno_anchor_point_id23, uno_anchor_point_id24, uno_anchor_point_id25, uno_anchor_point_id26, uno_anchor_point_id27, uno_anchor_point_id28, uno_anchor_point_id29, uno_anchor_point_id30, uno_anchor_point_id31, uno_anchor_point_id32])
        self.canvas.tag_bind(image_id, '<Button-1>', self.start_drag)
        self.canvas.tag_bind(image_id, '<B1-Motion>', self.drag)

        self.line_anchor_points[uno_object_name] = {}
        self.line_ids[uno_object_name] = []

        self.canvas.tag_bind(uno_anchor_point_id1, '<Button-1>', lambda event: self.handle_anchor_point_click(event, uno_anchor_point_id1, uno_object_name))
        self.canvas.tag_bind(uno_anchor_point_id2, '<Button-1>', lambda event: self.handle_anchor_point_click(event, uno_anchor_point_id2, uno_object_name))
        self.canvas.tag_bind(uno_anchor_point_id3, '<Button-1>', lambda event: self.handle_anchor_point_click(event, uno_anchor_point_id3, uno_object_name))
        self.canvas.tag_bind(uno_anchor_point_id4, '<Button-1>', lambda event: self.handle_anchor_point_click(event, uno_anchor_point_id4, uno_object_name))
        self.canvas.tag_bind(uno_anchor_point_id5, '<Button-1>', lambda event: self.handle_anchor_point_click(event, uno_anchor_point_id5, uno_object_name))
        self.canvas.tag_bind(uno_anchor_point_id6, '<Button-1>', lambda event: self.handle_anchor_point_click(event, uno_anchor_point_id6, uno_object_name))
        self.canvas.tag_bind(uno_anchor_point_id7, '<Button-1>', lambda event: self.handle_anchor_point_click(event, uno_anchor_point_id7, uno_object_name))
        self.canvas.tag_bind(uno_anchor_point_id8, '<Button-1>', lambda event: self.handle_anchor_point_click(event, uno_anchor_point_id8, uno_object_name))
        self.canvas.tag_bind(uno_anchor_point_id9, '<Button-1>', lambda event: self.handle_anchor_point_click(event, uno_anchor_point_id9, uno_object_name))
        self.canvas.tag_bind(uno_anchor_point_id10, '<Button-1>', lambda event: self.handle_anchor_point_click(event, uno_anchor_point_id10, uno_object_name))
        self.canvas.tag_bind(uno_anchor_point_id11, '<Button-1>', lambda event: self.handle_anchor_point_click(event, uno_anchor_point_id11, uno_object_name))
        self.canvas.tag_bind(uno_anchor_point_id12, '<Button-1>', lambda event: self.handle_anchor_point_click(event, uno_anchor_point_id12, uno_object_name))
        self.canvas.tag_bind(uno_anchor_point_id13, '<Button-1>', lambda event: self.handle_anchor_point_click(event, uno_anchor_point_id13, uno_object_name))
        self.canvas.tag_bind(uno_anchor_point_id14, '<Button-1>', lambda event: self.handle_anchor_point_click(event, uno_anchor_point_id14, uno_object_name))
        self.canvas.tag_bind(uno_anchor_point_id15, '<Button-1>', lambda event: self.handle_anchor_point_click(event, uno_anchor_point_id15, uno_object_name))
        self.canvas.tag_bind(uno_anchor_point_id16, '<Button-1>', lambda event: self.handle_anchor_point_click(event, uno_anchor_point_id16, uno_object_name))
        self.canvas.tag_bind(uno_anchor_point_id17, '<Button-1>', lambda event: self.handle_anchor_point_click(event, uno_anchor_point_id17, uno_object_name))
        self.canvas.tag_bind(uno_anchor_point_id18, '<Button-1>', lambda event: self.handle_anchor_point_click(event, uno_anchor_point_id18, uno_object_name))
        self.canvas.tag_bind(uno_anchor_point_id19, '<Button-1>', lambda event: self.handle_anchor_point_click(event, uno_anchor_point_id19, uno_object_name))
        self.canvas.tag_bind(uno_anchor_point_id20, '<Button-1>', lambda event: self.handle_anchor_point_click(event, uno_anchor_point_id20, uno_object_name))
        self.canvas.tag_bind(uno_anchor_point_id21, '<Button-1>', lambda event: self.handle_anchor_point_click(event, uno_anchor_point_id21, uno_object_name))
        self.canvas.tag_bind(uno_anchor_point_id22, '<Button-1>', lambda event: self.handle_anchor_point_click(event, uno_anchor_point_id22, uno_object_name))
        self.canvas.tag_bind(uno_anchor_point_id23, '<Button-1>', lambda event: self.handle_anchor_point_click(event, uno_anchor_point_id23, uno_object_name))
        self.canvas.tag_bind(uno_anchor_point_id24, '<Button-1>', lambda event: self.handle_anchor_point_click(event, uno_anchor_point_id24, uno_object_name))
        self.canvas.tag_bind(uno_anchor_point_id25, '<Button-1>', lambda event: self.handle_anchor_point_click(event, uno_anchor_point_id25, uno_object_name))
        self.canvas.tag_bind(uno_anchor_point_id26, '<Button-1>', lambda event: self.handle_anchor_point_click(event, uno_anchor_point_id26, uno_object_name))
        self.canvas.tag_bind(uno_anchor_point_id27, '<Button-1>', lambda event: self.handle_anchor_point_click(event, uno_anchor_point_id27, uno_object_name))
        self.canvas.tag_bind(uno_anchor_point_id28, '<Button-1>', lambda event: self.handle_anchor_point_click(event, uno_anchor_point_id28, uno_object_name))
        self.canvas.tag_bind(uno_anchor_point_id29, '<Button-1>', lambda event: self.handle_anchor_point_click(event, uno_anchor_point_id29, uno_object_name))
        self.canvas.tag_bind(uno_anchor_point_id30, '<Button-1>', lambda event: self.handle_anchor_point_click(event, uno_anchor_point_id30, uno_object_name))
        self.canvas.tag_bind(uno_anchor_point_id31, '<Button-1>', lambda event: self.handle_anchor_point_click(event, uno_anchor_point_id31, uno_object_name))
        self.canvas.tag_bind(uno_anchor_point_id32, '<Button-1>', lambda event: self.handle_anchor_point_click(event, uno_anchor_point_id32, uno_object_name))
        # print(f"{uno_object_name}")

        # add LED data to instance variable dictionary
        self.device_data[uno_object_name] = [uno_anchor_point_id1, uno_anchor_point_id2, uno_anchor_point_id3, uno_anchor_point_id4, uno_anchor_point_id5, uno_anchor_point_id6, uno_anchor_point_id7, uno_anchor_point_id8, uno_anchor_point_id9, uno_anchor_point_id10, uno_anchor_point_id11, uno_anchor_point_id12, uno_anchor_point_id13, uno_anchor_point_id14, uno_anchor_point_id15, uno_anchor_point_id16, uno_anchor_point_id17, uno_anchor_point_id18, uno_anchor_point_id19, uno_anchor_point_id20, uno_anchor_point_id21, uno_anchor_point_id22, uno_anchor_point_id23, uno_anchor_point_id24, uno_anchor_point_id25, uno_anchor_point_id26, uno_anchor_point_id27, uno_anchor_point_id28, uno_anchor_point_id29, uno_anchor_point_id30, uno_anchor_point_id31, uno_anchor_point_id32]
        self.uno_pin_data[uno_object_name] = [uno_anchor_point_id1, uno_anchor_point_id2, uno_anchor_point_id3, uno_anchor_point_id4, uno_anchor_point_id5, uno_anchor_point_id6, uno_anchor_point_id7, uno_anchor_point_id8, uno_anchor_point_id9, uno_anchor_point_id10, uno_anchor_point_id11, uno_anchor_point_id12, uno_anchor_point_id13, uno_anchor_point_id14, uno_anchor_point_id15, uno_anchor_point_id16, uno_anchor_point_id17, uno_anchor_point_id18, uno_anchor_point_id19, uno_anchor_point_id20, uno_anchor_point_id21, uno_anchor_point_id22, uno_anchor_point_id23, uno_anchor_point_id24, uno_anchor_point_id25, uno_anchor_point_id26, uno_anchor_point_id27, uno_anchor_point_id28, uno_anchor_point_id29, uno_anchor_point_id30, uno_anchor_point_id31, uno_anchor_point_id32]

        # print("device data")
        # print(self.device_data)
        # print("uno pin data")
        # print(self.uno_pin_data)

        self.run()

    def handle_anchor_point_click(self, event, anchor_point_id, object_name):
        global first_pin_clicked
        global second_pin_clicked

        if self.prev_anchor_point_id is None:
            # If there is no previously clicked anchor point, store the current one as the previous one
            self.prev_anchor_point_id = anchor_point_id
            self.current_object_name = object_name
        elif self.current_object_name != object_name and self.prev_anchor_point_id != anchor_point_id:
            # If the current object is different from the previously clicked object and
            # the clicked anchor point is not the same as the previous one, draw a line between the two anchor points
            # Increment the line counter
            self.line_counter += 1

            # Draw the line
            line_id = self.canvas.create_line(
                self.canvas.coords(self.prev_anchor_point_id)[0],
                self.canvas.coords(self.prev_anchor_point_id)[1],
                self.canvas.coords(anchor_point_id)[0],
                self.canvas.coords(anchor_point_id)[1],
                width=6, fill="blue", tags=f"{self.line_tag_prefix}{self.line_tag_counter}"
            )
            self.canvas.itemconfig(line_id, tags=(self.current_object_name, 'line'))
            self.line_ids[object_name].append(line_id)

            ######## Search start

            search_device_value_1_previous_point = self.prev_anchor_point_id
            search_device_value_2_ending_point = anchor_point_id

# previous pin

            for key, value in self.device_data.items():
                if search_device_value_1_previous_point in value:
                    # print(key)
                    first_clicked_device_type = key.split()[0]
                    # print(first_clicked_device_type)

                    if first_clicked_device_type == "LED":
                        # print("added device is a LED")

                        for key, first_value in self.device_data.items():
                            if search_device_value_1_previous_point in first_value:
                                first_led_negative_pin = min(first_value)
                                first_led_positive_pin = max(first_value)

                                if search_device_value_1_previous_point == first_led_positive_pin:
                                    # positive = search_device_value_1_previous_point
                                    first_pin_clicked = f"{key} positive"
                                    # print(pin_clicked)

                                elif search_device_value_1_previous_point == first_led_negative_pin:
                                    # negative = search_device_value_1_previous_point
                                    first_pin_clicked = f"{key} negative"
                                    # print(pin_clicked)

                    elif first_clicked_device_type == "Laser":
                        first_Digital_signal_pin = min(value)
                        first_Ground_pin = max(value)
                        first_Power_pin = sum(value) - first_Digital_signal_pin - first_Ground_pin

                        if search_device_value_1_previous_point == first_Digital_signal_pin:
                            first_pin_clicked = f"{key} ds"
                        elif search_device_value_1_previous_point == first_Ground_pin:
                            first_pin_clicked = f"{key} ground"
                        elif search_device_value_1_previous_point == first_Power_pin:
                            first_pin_clicked = f"{key} power"

                    elif first_clicked_device_type == "Uno":
                        my_list_1 = self.uno_pin_data[key]
                        first_index = my_list_1.index(search_device_value_1_previous_point)

                        my_list_2 = {'uno_pin_list': ['NC', 'IOREF', 'RESET', '3.3V', '5V', 'GND', 'GND', 'Vin', 'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'SCL', 'SDA', 'AREF', 'GND', '13', '12', '11', '10', '9', '8', '7', '6', '5', '4', '3', '2', '1', '0']}

                        first_value = my_list_2['uno_pin_list'][first_index]
                        first_pin_clicked = f"{key} {first_value}"

            # print("first click\n")
            # print(first_pin_clicked)
            # print("first click\n")

################################################# ending pin

            for key, value2 in self.device_data.items():

                if search_device_value_2_ending_point in value2:
                    # print(key)
                    second_clicked_device_type = key.split()[0]
                    # print(second_clicked_device_type)

                    if second_clicked_device_type == "LED":
                        # print("added device is a LED")

                        for key, second_value_2 in self.device_data.items():
                            if search_device_value_2_ending_point in second_value_2:
                                second_led_negative_pin = min(second_value_2)
                                second_led_positive_pin = max(second_value_2)

                                if search_device_value_2_ending_point == second_led_positive_pin:
                                    # positive = search_device_value_1_previous_point
                                    second_pin_clicked = f"{key} positive"

                                elif search_device_value_2_ending_point == second_led_negative_pin:
                                    # negative = search_device_value_1_previous_point
                                    second_pin_clicked = f"{key} negative"

                    elif second_clicked_device_type == "Laser":
                        second_Digital_signal_pin = min(value2)
                        second_Ground_pin = max(value2)
                        second_Power_pin = sum(value2) - second_Digital_signal_pin - second_Ground_pin

                        if search_device_value_2_ending_point == second_Digital_signal_pin:
                            second_pin_clicked = f"{key}"
                        elif search_device_value_2_ending_point == second_Ground_pin:
                            pass
                            # second_pin_clicked = f"{key} ground"
                        elif search_device_value_2_ending_point == second_Power_pin:
                            pass
                            # second_pin_clicked = f"{key} power"

                    elif second_clicked_device_type == "Uno":
                        my_list_3 = self.uno_pin_data[key]
                        second_index = my_list_3.index(search_device_value_2_ending_point)
                        # print(second_index)

                        my_list_4 = {'uno_pin_list': ['NC', 'IOREF', 'RESET', '3.3V', '5V', 'GND', 'GND', 'Vin', 'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'SCL', 'SDA', 'AREF', 'GND', '13', '12', '11', '10', '9', '8', '7', '6', '5', '4', '3', '2', '1', '0']}

                        # index = 0  # replace 0 with the desired index value
                        second_value = my_list_4['uno_pin_list'][second_index]
                        second_pin_clicked = f"{key} {second_value}"

            # print("second click\n")
            # print(second_pin_clicked)
            # print("second click\n")
######## Search end

            # print(f"Line drawn between {self.prev_anchor_point_id} and {anchor_point_id}")
            self.prev_anchor_point_id = None
            self.current_object_name = object_name

            # Increment the line tag counter
            self.line_tag_counter += 1
        else:
            # If the current object is the same as the previously clicked object or the clicked anchor point is the same as the previous one,
            # do not draw a line and store the current anchor point as the previous one
            self.prev_anchor_point_id = anchor_point_id

        # print(f"{anchor_point_id} clicked for {object_name}")

        self.final[first_pin_clicked] = second_pin_clicked
        # print("final")
        # print(self.final)

#########################################################################################

        to_remove_gnd = []

        for key, value in self.final.items():
            if "GND" in key:
                to_remove_gnd.append(key)
                for k, v in self.final.items():
                    if v == key:
                        to_remove_gnd.append(k)
            elif "GND" in value:
                to_remove_gnd.append(key)
                for k, v in self.final.items():
                    if k == value:
                        to_remove_gnd.append(k)

        new_dict = {k: v for k, v in self.final.items() if k not in to_remove_gnd and v not in to_remove_gnd}
        # print("without GNDs")
        # print(new_dict)

        to_remove_power = []

        for key, value in new_dict.items():
            if "power" in key:
                to_remove_power.append(key)
                for k, v in new_dict.items():
                    if v == key:
                        to_remove_power.append(k)
            elif "power" in value:
                to_remove_power.append(key)
                for k, v in new_dict.items():
                    if k == value:
                        to_remove_power.append(k)

        new_dict2 = {k: v for k, v in new_dict.items() if k not in to_remove_power and v not in to_remove_power}
        # print("without power")
        # print(new_dict2)

################################################################################################################

        to_remove_5V = []

        for key, value in new_dict2.items():
            if "5V" in key:
                to_remove_5V.append(key)
                for k, v in new_dict2.items():
                    if v == key:
                        to_remove_5V.append(k)
            elif "5V" in value:
                to_remove_5V.append(key)
                for k, v in new_dict2.items():
                    if k == value:
                        to_remove_5V.append(k)

        new_diction1 = {k: v for k, v in new_dict2.items() if k not in to_remove_gnd and v not in to_remove_5V}

        new_dict3 = {}
        swapped_send_dic = {}

        for key, value in new_diction1.items():
            if key.split()[0] == "Uno":
                new_dict3[key] = value
            elif value.split()[0] == "Uno":
                new_key = value
                new_value = key
                new_dict3[new_key] = new_value
            else:
                print(f"Skipping key-value pair: {key}: {value}")

        swapped_send_dic = {value: key for key, value in new_dict3.items()}

        self.code_dictionary = {}

        for key, value in swapped_send_dic.items():
            code_key = key.split()[0] + " " + key.split()[1]
            code_value = value.split()[1]
            self.code_dictionary[code_key] = code_value

    def start_drag(self, event):
        self.dragging = True
        self.drag_start_x = event.x
        self.drag_start_y = event.y
        # Set the selected_image_id to the ID of the image that is clicked
        self.selected_image_id = event.widget.find_closest(event.x, event.y)[0]
        self.image_index = self.image_ids.index(self.selected_image_id)
        self.canvas.unbind('<Button-1>')
        self.canvas.unbind('<B1-Motion>')

    def drag(self, event):
        if self.dragging:
            dx = event.x - self.drag_start_x
            dy = event.y - self.drag_start_y
            self.canvas.move(self.selected_image_id, dx, dy)
            anchor_points = self.anchor_point_ids[self.image_ids.index(self.selected_image_id)]
            for anchor_point_id in anchor_points:
                self.canvas.move(anchor_point_id, dx, dy)
            self.drag_start_x = event.x
            self.drag_start_y = event.y

            self.canvas.unbind('<Button-1>')
            self.canvas.unbind('<B1-Motion>')
            self.canvas.unbind('<ButtonRelease-1>')

        self.canvas.tag_bind(self.selected_image_id, '<Button-1>', self.start_drag)
        self.canvas.tag_bind(self.selected_image_id, '<B1-Motion>', self.drag)

    def stop_drag(self, event):
        self.dragging = False
        self.selected_image_id = None

    def run(self):
        self.master.bind('<ButtonRelease-1>', self.stop_drag)
        # Bind the right mouse button to the delete_line method
        # self.canvas.bind('<Button-3>', self.delete_line)
        self.master.mainloop()

    def send_dictionary(self):
        sending_code_dictionary = {}
        # print("create code")
        sending_code_dictionary = self.code_dictionary
        # print(sending_code_dictionary)
        acc.receive_dictionary(sending_code_dictionary)


if __name__ == '__main__':
    root = tk.Tk()
    canvas = ImageCanvas(root)
    root.mainloop()
