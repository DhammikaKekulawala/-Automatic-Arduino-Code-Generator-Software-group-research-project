import tkinter as tk

devices = {}
led_entries_on = {}
led_entries_off = {}
pin_values = {}
codeg = {}

def upload_values(devices):
    value = {}
    value = devices
    print("a")
    print(devices)
    only_devices(devices)
    return devices


#devices = {'LED1': ['GND2', '5'], 'LED2': ['GND', '12'],'Laser1':['GND','12',1],'LED15':['11','2']}

def only_devices(devices):

    led_devices = {}
    laser_devices = {}
    led_dict = {}
    laser_dict = {}
    laser = {}

    for device, pins in devices.items():
        if 'LED' in device:
            led_devices[device] = pins
            for pin in pins:
                if pin.isdigit():
                    led_dict[device] = pin
        elif 'Laser' in device:
            laser_devices[device] = pins
            for pin in pins:
                if pin.isdigit():
                    laser_dict[device] = pin

    print("LED devices:", led_devices)
    print("Laser devices:", laser_devices)
    print(led_dict)
    print(laser_dict)
    if len(laser_dict) == 0:
        print("Laser 0")
    elif len(laser_dict) != 0:
        print("Laser not 0")
        laser = devices_laser(laser_dict)
    else:
        print("wrong2")
    if len(led_dict) == 0:
        print("LED 0")
    elif len(led_dict) != 0:
        print("LED not 0")
        pin_values = led_dict
        if len(laser_dict) != 0:
            print(pin_values)
            print("abc")
            devices_led(led_dict)
        else:
            led_dict.update(laser)
            print(led_dict)
            devices_led(led_dict)
    else:
        print("wrong")


def devices_laser(input_dict):
    exclude_values =  ['GND', 'GND1', 'GND2', '5V']

    output_dict = {k: v[0] for k, v in input_dict.items() if v[1:] != exclude_values}

    print(output_dict)
    return output_dict


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
    window.geometry("400x150")  # set window size

    # create a table with column headings
    led_label = tk.Label(window, text="LED devices  ")
    led_label.grid(column=0, row=0)
    led_entry_on = tk.Label(window, text="Bulb on time duration  ")
    led_entry_on.grid(column=1, row=0)
    led_entry_off = tk.Label(window, text="Bulb off time duration")
    led_entry_off.grid(column=2, row=0)

    # create an entry field for each LED and its corresponding entry fields
    led_entries_on = {}
    led_entries_off = {}
    for i, (led_name, led_pin) in enumerate(led_pins.items(), start=1):
        # create a label for the LED
        led_label = tk.Label(window, text=led_name)
        led_label.grid(column=0, row=i)

        # create an entry field for the "on" time duration
        led_entry_on = tk.Entry(window, width=10)
        led_entry_on.grid(column=1, row=i)
        led_entries_on[led_name] = led_entry_on

        # create an entry field for the "off" time duration
        led_entry_off = tk.Entry(window, width=10)
        led_entry_off.grid(column=2, row=i)
        led_entries_off[led_name] = led_entry_off

    # create a button to submit the values
    submit_button = tk.Button(window, text="Submit", command=lambda: submit_values_led(led_pins))
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
        text_widget = tk.Text(window, height=20, width=50)
        text_widget.pack()

        # Display the devices
        text_widget.insert('end', 'void setup()\n{\n')
        for device, pins in devices.items():
            text_widget.insert('end', f'  pinMode({pins[0]}, OUTPUT);\n')
            #text_widget.insert('end', f'  digitalWrite({pins[0]}, LOW);\n')
        text_widget.insert('end', '}\n\nvoid loop()\n{\n')
        for device, pins in devices.items():
            text_widget.insert('end', f'  digitalWrite({pins[0]}, HIGH);\n')
            text_widget.insert('end', f'  delay({pins[1]});\n')
            text_widget.insert('end', f'  digitalWrite({pins[0]}, LOW);\n')
            text_widget.insert('end', f'  delay({pins[2]});\n')
        text_widget.insert('end', '}')

    # Create a button to display the devices
    button = tk.Button(root, text='Display code', command=display_code)
    button.pack()

    # Start the main loop
    root.mainloop()






