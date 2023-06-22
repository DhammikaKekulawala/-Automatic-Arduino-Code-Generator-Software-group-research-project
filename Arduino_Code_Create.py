import tkinter as tk

# led_pins = {'LED 1': '5', 'LED 2': '6', 'LED 3': '7', 'Laser 1': '8', 'Laser 2': '9'}
led_pins = {}


def receive_dictionary(led_pins):
    devices_led(led_pins)


def submit_values_led(led_pins):
    output = {}
    for led_name in led_pins.keys():
        # get the "on" and "off" time durations from the entry fields
        on_duration = led_entries_on[led_name].get()
        off_duration = led_entries_off[led_name].get()

        # add the LED pin number, "on" duration, and "off" duration to the output dictionary
        output[led_name] = [led_pins[led_name], on_duration, off_duration]

    # print the output dictionary
    print(output)
    code_generate(output)


def devices_led(led_pins):
    global led_entries_on, led_entries_off

    # create a Tkinter window
    window = tk.Tk()
    window.geometry("680x450")  # set window size

    # set window color
    window.configure(bg='white')

    window.title("Arduino Code Generator")

    # create a table with column headings
    led_label = tk.Label(window, text="Device Name", font=('Times New Roman', 12, 'bold'), bg="#7F7FFF", padx=10, pady=10)
    led_label.grid(column=0, row=0)
    led_entry_on = tk.Label(window, text="Device on time duration in milliseconds", font=('Times New Roman', 12, 'bold'), bg="#7F7FFF", padx=10, pady=10)
    led_entry_on.grid(column=1, row=0)
    led_entry_off = tk.Label(window, text="Device off time duration in milliseconds", font=('Times New Roman', 12, 'bold'), bg="#7F7FFF", padx=10, pady=10)
    led_entry_off.grid(column=2, row=0)

    # create an entry field for each LED and its corresponding entry fields
    led_entries_on = {}
    led_entries_off = {}
    for i, (led_name, led_pin) in enumerate(led_pins.items(), start=1):
        # create a label for the LED
        led_label = tk.Label(window, text=led_name, font=('Times New Roman', 12, 'bold'), bg="white", padx=10, pady=10)
        led_label.grid(column=0, row=i)

        # create an entry field for the "on" time duration
        led_entry_on = tk.Entry(window, width=20)
        led_entry_on.grid(column=1, row=i)
        led_entries_on[led_name] = led_entry_on

        # create an entry field for the "off" time duration
        led_entry_off = tk.Entry(window, width=20)
        led_entry_off.grid(column=2, row=i)
        led_entries_off[led_name] = led_entry_off

    # create a button to submit the values
    submit_button = tk.Button(window, text="Submit", command=lambda: submit_values_led(led_pins), font=('Times New Roman', 15, 'bold'), fg="#96D9D9", bg="#00979C", padx=15, pady=10)
    submit_button.grid(column=0, row=len(led_pins) + 1, columnspan=3)

    # start the Tkinter event loop
    window.mainloop()

def code_generate(codeg):

    devices = codeg

    # Create the main window
    root = tk.Tk()

    def display_code():
        # Create a new window
        window = tk.Toplevel()

        # Create a Text widget to display the devices
        text_widget = tk.Text(window, height=30, width=50)
        text_widget.pack()

        # Display the devices
        text_widget.insert('end', 'void setup()\n{\n')
        for device, pins in devices.items():
            text_widget.insert('end', f'  pinMode({pins[0]}, OUTPUT);\n')
            # text_widget.insert('end', f'  digitalWrite({pins[0]}, LOW);\n')
        text_widget.insert('end', '}\n\nvoid loop()\n{\n')
        for device, pins in devices.items():
            text_widget.insert('end', f'  digitalWrite({pins[0]}, HIGH);\n')
            text_widget.insert('end', f'  delay({pins[1]});\n')
            text_widget.insert('end', f'  digitalWrite({pins[0]}, LOW);\n')
            text_widget.insert('end', f'  delay({pins[2]});\n')
        text_widget.insert('end', '}')

    # Create a button to display the devices
    button = tk.Button(root, text='Confirm', command=display_code, font=('Times New Roman', 15, 'bold'), fg="#96D9D9", bg="#00979C", padx=10, pady=5)
    button.pack()

    # Start the main loop
    root.mainloop()


# devices_led(led_pins)
