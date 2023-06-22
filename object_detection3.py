from PIL import Image
from roboflow import Roboflow
import numpy as np
import heapq

#devices detection
rf = Roboflow(api_key="QEwsPw9Evo9Rs7hf0PPy")
project = rf.workspace().project("arduino-and-devices-detection")
model = project.version(1).model

#pin detection
rf2 = Roboflow(api_key="QEwsPw9Evo9Rs7hf0PPy")
project2 = rf2.workspace().project("arduino-pin-detection")
model2 = project2.version(3).model



# infer on a local image
n = "n\\c8.png"
device = {}
pin = {}
pin_color = {}
device_point_color = {}
pin_plug = {}
out_put = {}


def devices_detect(image_n):
    data = model.predict("{0}".format(image_n), confidence=40, overlap=30).json()
    #print(data)

    # visualize your prediction
    model.predict("{0}".format(image_n), confidence=40, overlap=30).save("prediction.jpg")

    # infer on an image hosted elsewhere
    # print(model.predict("URL_OF_YOUR_IMAGE", hosted=True, confidence=40, overlap=30).json())

    # get the "predictions" array
    image = data["image"]
    predictions = data["predictions"]

    # create empty lists to store the predictions for each class

    arduinos = []
    leds = []
    lasers = []

    devices = {'Arduino': 0, 'LED': 0, 'Laser': 0}

    # iterate through the predictions

    for prediction in predictions:
        class_name = prediction["class"]
        if class_name == "Arduino_UNO":
            arduinos.append(prediction)
        elif class_name == "LED":
            leds.append(prediction)
        elif class_name == "Laser":
            lasers.append(prediction)

    # print the predictions for each class

    x = 0
    b = 1
    c = 0

    number_arduino = 0
    number_led = 0
    number_laser = 0

    for arduino in arduinos:
        number_arduino = number_arduino + 1

    # display LED
    for led in leds:
        number_led = number_led + 1

    for laser in lasers:
        number_laser = number_laser + 1


    devices['Arduino'] = number_arduino
    devices['LED'] = number_led
    devices['Laser'] = number_laser



    # image coordinate and save image
    for prediction in data["predictions"]:
        width = int(prediction["width"])
        height = int(prediction["height"])
        x_coordinate = int(prediction["x"])
        y_coordinate = int(prediction["y"])

        x1 = int(x_coordinate - width / 2)
        x2 = int(x_coordinate + width / 2)
        y1 = int(y_coordinate - height / 2)
        y2 = int(y_coordinate + height / 2)

        img = Image.open("{0}".format(image_n))

        imgCropped = img.crop(box=(x1, y1, x2, y2))

        if prediction["class"] == "Arduino_UNO":
            class_devices = prediction["class"]
            image_name = class_devices + str(x)
            imgCropped.save("detect_image/{0}.png".format(image_name))
            x = x + 1
        elif prediction["class"] == "LED":
            class_devices = prediction["class"]
            image_name = class_devices + str(b)
            imgCropped.save("detect_image/{0}.png".format(image_name))
            b = b + 1
        elif prediction["class"] == "Laser":
            class_devices = prediction["class"]
            image_name = class_devices + str(c)
            imgCropped.save("detect_image/{0}.png".format(image_name))
            c = c + 1



    return devices


def arduino_pin_series(Ar):

    # infer on a local image
    data_array = model2.predict("detect_image/{0}.png".format(Ar), confidence=40, overlap=30).json()


    # visualize your prediction
    data = model2.predict("detect_image/{0}.png".format(Ar), confidence=40, overlap=30).save("prediction1.jpg")

    # infer on an image hosted elsewhere
    # print(model.predict("URL_OF_YOUR_IMAGE", hosted=True, confidence=40, overlap=30).json())
    arduino_pin = {'SCL': 'unplug', 'SDA': 'unplug', 'AREF': 'unplug', 'GND': 'red', '13': 'yellow', '12': 'unplug', '11': 'unplug', '10': 'unplug', '9': 'unplug', '8': 'unplug', '7': 'unplug', '6': 'unplug', '5': 'unplug', '4': 'unplug', '3': 'unplug', '2': 'unplug', '1': 'unplug', '0': 'unplug', 'A0': 'unplug', 'A1': 'unplug', 'A2': 'unplug', 'A3': 'unplug', 'A4': 'unplug', 'A5': 'unplug', 'up_pin': 'unplug', 'IOREF': 'unplug', 'RESET': 'unplug', '3.3V': 'unplug', '5V': 'unplug', 'GND1': 'unplug', 'GND2': 'unplug', 'VIN': 'unplug'}

    data = data_array

    for prediction in data["predictions"]:
        width = int(prediction["width"])
        height = int(prediction["height"])
        x_coordinate = int(prediction["x"])
        y_coordinate = int(prediction["y"])

        x1 = int(x_coordinate - width / 2)
        x2 = int(x_coordinate + width / 2)
        y1 = int(y_coordinate - height / 2)
        y2 = int(y_coordinate + height / 2)

        img = Image.open("detect_image/{0}.png".format(Ar))

        imgCropped = img.crop(box=(x1, y1, x2, y2))


        class_devices = prediction["class"]
        image_name = class_devices
        imgCropped.save("pin/{0}.png".format(image_name))


        if prediction["class"] == "Right_up":

            width = prediction["width"]
            height = prediction["height"]

            one_pin_width = width / 10

            w1 = 0
            h1 = 0
            h2 = height
            w2 = one_pin_width

            img = Image.open("pin/{0}.png".format(image_name))
            imgCropped = img.crop(box=(w1, h1, w2, h2))
            imgCropped.save("pin/Right_up/SCL.png")
            pin_path = "pin/Right_up/SCL.png"
            pin_pattern = pin_colors(pin_path)
            arduino_pin['SCL'] = pin_pattern

            w1 = w2
            w2 = w2 + one_pin_width
            img = Image.open("pin/{0}.png".format(image_name))
            imgCropped = img.crop(box=(w1, h1, w2, h2))
            imgCropped.save("pin/Right_up/SDA.png")
            pin_path = "pin/Right_up/SDA.png"
            pin_pattern = pin_colors(pin_path)
            arduino_pin['SDA'] = pin_pattern

            w1 = w2
            w2 = w2 + one_pin_width
            img = Image.open("pin/{0}.png".format(image_name))
            imgCropped = img.crop(box=(w1, h1, w2, h2))
            imgCropped.save("pin/Right_up/AREF.png")
            pin_path = "pin/Right_up/AREF.png"
            pin_pattern = pin_colors(pin_path)
            arduino_pin['AREF'] = pin_pattern

            w1 = w2
            w2 = w2 + one_pin_width
            img = Image.open("pin/{0}.png".format(image_name))
            imgCropped = img.crop(box=(w1, h1, w2, h2))
            imgCropped.save("pin/Right_up/GND.png")
            pin_path = "pin/Right_up/GND.png"
            pin_pattern = pin_colors(pin_path)
            arduino_pin['GND'] = pin_pattern

            w1 = w2
            w2 = w2 + one_pin_width
            img = Image.open("pin/{0}.png".format(image_name))
            imgCropped = img.crop(box=(w1, h1, w2, h2))
            imgCropped.save("pin/Right_up/13.png")
            pin_path = "pin/Right_up/13.png"
            pin_pattern = pin_colors(pin_path)
            arduino_pin['13'] = pin_pattern

            w1 = w2
            w2 = w2 + one_pin_width
            img = Image.open("pin/{0}.png".format(image_name))
            imgCropped = img.crop(box=(w1, h1, w2, h2))
            imgCropped.save("pin/Right_up/12.png")
            pin_path = "pin/Right_up/12.png"
            pin_pattern = pin_colors(pin_path)
            arduino_pin['12'] = pin_pattern

            w1 = w2
            w2 = w2 + one_pin_width
            img = Image.open("pin/{0}.png".format(image_name))
            imgCropped = img.crop(box=(w1, h1, w2, h2))
            imgCropped.save("pin/Right_up/11.png")
            pin_path = "pin/Right_up/11.png"
            pin_pattern = pin_colors(pin_path)
            arduino_pin['11'] = pin_pattern

            w1 = w2
            w2 = w2 + one_pin_width
            img = Image.open("pin/{0}.png".format(image_name))
            imgCropped = img.crop(box=(w1, h1, w2, h2))
            imgCropped.save("pin/Right_up/10.png")
            pin_path = "pin/Right_up/10.png"
            pin_pattern = pin_colors(pin_path)
            arduino_pin['10'] = pin_pattern

            w1 = w2
            w2 = w2 + one_pin_width
            img = Image.open("pin/{0}.png".format(image_name))
            imgCropped = img.crop(box=(w1, h1, w2, h2))
            imgCropped.save("pin/Right_up/9.png")
            pin_path = "pin/Right_up/9.png"
            pin_pattern = pin_colors(pin_path)
            arduino_pin['9'] = pin_pattern

            w1 = w2
            w2 = w2 + one_pin_width
            img = Image.open("pin/{0}.png".format(image_name))
            imgCropped = img.crop(box=(w1, h1, w2, h2))
            imgCropped.save("pin/Right_up/8.png")
            pin_path = "pin/Right_up/8.png"
            pin_pattern = pin_colors(pin_path)
            arduino_pin['8'] = pin_pattern

        elif prediction["class"] == "Right_down":
            width = prediction["width"]
            height = prediction["height"]

            one_pin_width = width / 8

            w1 = 0
            h1 = 0
            h2 = height
            w2 = one_pin_width

            img = Image.open("pin/{0}.png".format(image_name))
            imgCropped = img.crop(box=(w1, h1, w2, h2))
            imgCropped.save("pin/Right_down/7.png")
            pin_path = "pin/Right_down/7.png"
            pin_pattern = pin_colors(pin_path)
            arduino_pin['7'] = pin_pattern

            w1 = w2
            w2 = w2 + one_pin_width
            img = Image.open("pin/{0}.png".format(image_name))
            imgCropped = img.crop(box=(w1, h1, w2, h2))
            imgCropped.save("pin/Right_down/6.png")
            pin_path = "pin/Right_down/6.png"
            pin_pattern = pin_colors(pin_path)
            arduino_pin['6'] = pin_pattern

            w1 = w2
            w2 = w2 + one_pin_width
            img = Image.open("pin/{0}.png".format(image_name))
            imgCropped = img.crop(box=(w1, h1, w2, h2))
            imgCropped.save("pin/Right_down/5.png")
            pin_path = "pin/Right_down/5.png"
            pin_pattern = pin_colors(pin_path)
            arduino_pin['5'] = pin_pattern

            w1 = w2
            w2 = w2 + one_pin_width
            img = Image.open("pin/{0}.png".format(image_name))
            imgCropped = img.crop(box=(w1, h1, w2, h2))
            imgCropped.save("pin/Right_down/4.png")
            pin_path = "pin/Right_down/4.png"
            pin_pattern = pin_colors(pin_path)
            arduino_pin['4'] = pin_pattern

            w1 = w2
            w2 = w2 + one_pin_width
            img = Image.open("pin/{0}.png".format(image_name))
            imgCropped = img.crop(box=(w1, h1, w2, h2))
            imgCropped.save("pin/Right_down/3.png")
            pin_path = "pin/Right_down/3.png"
            pin_pattern = pin_colors(pin_path)
            arduino_pin['3'] = pin_pattern

            w1 = w2
            w2 = w2 + one_pin_width
            img = Image.open("pin/{0}.png".format(image_name))
            imgCropped = img.crop(box=(w1, h1, w2, h2))
            imgCropped.save("pin/Right_down/2.png")
            pin_path = "pin/Right_down/2.png"
            pin_pattern = pin_colors(pin_path)
            arduino_pin['2'] = pin_pattern

            w1 = w2
            w2 = w2 + one_pin_width
            img = Image.open("pin/{0}.png".format(image_name))
            imgCropped = img.crop(box=(w1, h1, w2, h2))
            imgCropped.save("pin/Right_down/1.png")
            pin_path = "pin/Right_down/1.png"
            pin_pattern = pin_colors(pin_path)
            arduino_pin['1'] = pin_pattern

            w1 = w2
            w2 = w2 + one_pin_width
            img = Image.open("pin/{0}.png".format(image_name))
            imgCropped = img.crop(box=(w1, h1, w2, h2))
            imgCropped.save("pin/Right_down/0.png")
            pin_path = "pin/Right_down/0.png"
            pin_pattern = pin_colors(pin_path)
            arduino_pin['0'] = pin_pattern


        elif prediction["class"] == "Left_up":
            width = prediction["width"]
            height = prediction["height"]

            one_pin_width = width / 8

            w1 = 0
            h1 = 0
            h2 = height
            w2 = one_pin_width

            img = Image.open("pin/{0}.png".format(image_name))
            imgCropped = img.crop(box=(w1, h1, w2, h2))
            imgCropped.save("pin/Left_up/up_pin.png")
            pin_path = "pin/Left_up/up_pin.png"
            pin_pattern = pin_colors(pin_path)
            arduino_pin['up_pin'] = pin_pattern

            w1 = w2
            w2 = w2 + one_pin_width
            img = Image.open("pin/{0}.png".format(image_name))
            imgCropped = img.crop(box=(w1, h1, w2, h2))
            imgCropped.save("pin/Left_up/IOREF.png")
            pin_path = "pin/Left_up/IOREF.png"
            pin_pattern = pin_colors(pin_path)
            arduino_pin['IOREF'] = pin_pattern

            w1 = w2
            w2 = w2 + one_pin_width
            img = Image.open("pin/{0}.png".format(image_name))
            imgCropped = img.crop(box=(w1, h1, w2, h2))
            imgCropped.save("pin/Left_up/RESET.png")
            pin_path = "pin/Left_up/RESET.png"
            pin_pattern = pin_colors(pin_path)
            arduino_pin['RESET'] = pin_pattern

            w1 = w2
            w2 = w2 + one_pin_width
            img = Image.open("pin/{0}.png".format(image_name))
            imgCropped = img.crop(box=(w1, h1, w2, h2))
            imgCropped.save("pin/Left_up/3_3V.png")
            pin_path = "pin/Left_up/3_3V.png"
            pin_pattern = pin_colors(pin_path)
            arduino_pin['3_3V'] = pin_pattern

            w1 = w2
            w2 = w2 + one_pin_width
            img = Image.open("pin/{0}.png".format(image_name))
            imgCropped = img.crop(box=(w1, h1, w2, h2))
            imgCropped.save("pin/Left_up/5V.png")
            pin_path = "pin/Left_up/5V.png"
            pin_pattern = pin_colors(pin_path)
            arduino_pin['5V'] = pin_pattern

            w1 = w2
            w2 = w2 + one_pin_width
            img = Image.open("pin/{0}.png".format(image_name))
            imgCropped = img.crop(box=(w1, h1, w2, h2))
            imgCropped.save("pin/Left_up/GND1.png")
            pin_path = "pin/Left_up/GND1.png"
            pin_pattern = pin_colors(pin_path)
            arduino_pin['GND1'] = pin_pattern

            w1 = w2
            w2 = w2 + one_pin_width
            img = Image.open("pin/{0}.png".format(image_name))
            imgCropped = img.crop(box=(w1, h1, w2, h2))
            imgCropped.save("pin/Left_up/GND2.png")
            pin_path = "pin/Left_up/GND2.png"
            pin_pattern = pin_colors(pin_path)
            arduino_pin['GND2'] = pin_pattern

            w1 = w2
            w2 = w2 + one_pin_width
            img = Image.open("pin/{0}.png".format(image_name))
            imgCropped = img.crop(box=(w1, h1, w2, h2))
            imgCropped.save("pin/Left_up/VIN.png")
            pin_path = "pin/Left_up/VIN.png"
            pin_pattern = pin_colors(pin_path)
            arduino_pin['VIN'] = pin_pattern

        elif prediction["class"] == "Left_down":
            width = prediction["width"]
            height = prediction["height"]

            one_pin_width = width / 6

            w1 = 0
            h1 = 0
            h2 = height
            w2 = one_pin_width

            img = Image.open("pin/{0}.png".format(image_name))
            imgCropped = img.crop(box=(w1, h1, w2, h2))
            imgCropped.save("pin/Left_down/A0.png")
            pin_path = "pin/Left_down/A0.png"
            pin_pattern = pin_colors(pin_path)
            arduino_pin['A0'] = pin_pattern

            w1 = w2
            w2 = w2 + one_pin_width
            img = Image.open("pin/{0}.png".format(image_name))
            imgCropped = img.crop(box=(w1, h1, w2, h2))
            imgCropped.save("pin/Left_down/A1.png")
            pin_path = "pin/Left_down/A1.png"
            pin_pattern = pin_colors(pin_path)
            arduino_pin['A1'] = pin_pattern

            w1 = w2
            w2 = w2 + one_pin_width
            img = Image.open("pin/{0}.png".format(image_name))
            imgCropped = img.crop(box=(w1, h1, w2, h2))
            imgCropped.save("pin/Left_down/A2.png")
            pin_path = "pin/Left_down/A2.png"
            pin_pattern = pin_colors(pin_path)
            arduino_pin['A2'] = pin_pattern

            w1 = w2
            w2 = w2 + one_pin_width
            img = Image.open("pin/{0}.png".format(image_name))
            imgCropped = img.crop(box=(w1, h1, w2, h2))
            imgCropped.save("pin/Left_down/A3.png")
            pin_path = "pin/Left_down/A3.png"
            pin_pattern = pin_colors(pin_path)
            arduino_pin['A3'] = pin_pattern

            w1 = w2
            w2 = w2 + one_pin_width
            img = Image.open("pin/{0}.png".format(image_name))
            imgCropped = img.crop(box=(w1, h1, w2, h2))
            imgCropped.save("pin/Left_down/A4.png")
            pin_path = "pin/Left_down/A4.png"
            pin_pattern = pin_colors(pin_path)
            arduino_pin['A4'] = pin_pattern

            w1 = w2
            w2 = w2 + one_pin_width
            img = Image.open("pin/{0}.png".format(image_name))
            imgCropped = img.crop(box=(w1, h1, w2, h2))
            imgCropped.save("pin/Left_down/A5.png")
            pin_path = "pin/Left_down/A5.png"
            pin_pattern = pin_colors(pin_path)
            arduino_pin['A5'] = pin_pattern

    return arduino_pin

def pin_colors(pin_path):
    # Define color ranges for red, green, blue, yellow, orange, purple, pink, brown, and grey
    color_ranges = {
        "red": ((170, 0, 0), (255, 50, 50)),
        "green": ((0, 170, 0), (70, 255, 70)),
        "blue": ((0, 0, 170), (50, 180, 255)),
        "yellow": ((200, 200, 0), (255, 255, 50)),
        "orange": ((220, 120, 0), (255, 200, 50)),
        "purple": ((120, 0, 120), (170, 70, 170)),
        "pink": ((200, 20, 130), (255, 105, 180)),
        "brown": ((150, 42, 42), (200, 125, 80)),
        "grey": ((128, 128, 128), (200, 200, 200)),
        "unplug": ((0, 0, 0), (30, 30, 30))
    }

    # Load the image file
    image = Image.open("{0}".format(pin_path))

    # Get the RGB values for every pixel in the image and identify the color of each pixel
    width, height = image.size
    colors = []
    color_wire = {'red': 0, 'green': 0, 'blue': 0, 'yellow': 0, 'orange': 0, 'purple': 0, 'pink': 0, 'brown': 0, 'grey': 0, 'unplug': 0}
    red_count = 0
    green_count = 0
    blue_count = 0
    yellow_count = 0
    orange_count = 0
    purple_count = 0
    pink_count = 0
    brown_count = 0
    grey_count = 0
    count_other = 0
    count_unplug = 0

    for y in range(height):
        row = []
        for x in range(width):
            rgb = image.getpixel((x, y))
            color = "other"
            for name, (low, high) in color_ranges.items():
                if low[0] <= rgb[0] <= high[0] and low[1] <= rgb[1] <= high[1] and low[2] <= rgb[2] <= high[2]:
                    color = name
                    if color == "red":
                        # Increment the red pixel count
                        red_count += 1
                    elif color == "green":
                        green_count += 1
                    elif color == "blue":
                        blue_count += 1
                    elif color == "yellow":
                        yellow_count += 1
                    elif color == "orange":
                        orange_count += 1
                    elif color == "purple":
                        purple_count += 1
                    elif color == "pink":
                        pink_count += 1
                    elif color == "brown":
                        brown_count += 1
                    elif color == "grey":
                        grey_count += 1
                    elif color == "unplug":
                        count_unplug += 1
                    else:
                        count_other += 1

                    break

            row.append(color)
        colors.append(row)

    color_wire['red'] = red_count
    color_wire['green'] = green_count
    color_wire['blue'] = blue_count
    color_wire['yellow'] = yellow_count
    color_wire['orange'] = orange_count
    color_wire['purple'] = purple_count
    color_wire['pink'] = pink_count
    color_wire['brown'] = brown_count
    color_wire['grey'] = grey_count
    color_wire['unplug'] = count_unplug

    # Print the colors in matrix form
    #for row in colors:
       # print(row)
    #print(color_wire)
    #print(count_other)
    max_value = max(color_wire, key=color_wire.get)

   # print("Maximum value = ", max_value)
    pin_color = max_value
    #print(pin_color)

    return pin_color


def device_color(led):

    device_point_color = []



    # Define color ranges for red, green, blue, yellow, orange, purple, pink, brown, and grey
    color_ranges = {
        "red": ((170, 0, 0), (255, 50, 50)),
        "green": ((0, 170, 0), (70, 255, 70)),
        "blue": ((0, 0, 170), (50, 180, 255)),
        "yellow": ((200, 200, 0), (255, 255, 50)),
        "orange": ((220, 120, 0), (255, 200, 50)),
        "purple": ((120, 0, 120), (170, 70, 170)),
        "pink": ((200, 20, 130), (255, 105, 180)),
        "brown": ((150, 42, 42), (200, 125, 80))
        # "grey": ((128, 128, 128), (200, 200, 200))
    }

    # Load the image file and convert it to a NumPy array without alpha channel
    image = np.array(Image.open("detect_image/{0}.png".format(led)))[:, :, :3]


    # Create an empty mask with the same size as the image
    mask = np.zeros((image.shape[0], image.shape[1]), dtype=bool)

    # Apply each color range to the mask
    for name, (low, high) in color_ranges.items():
        # Convert the low and high RGB values to arrays
        low_arr = np.array(low)
        high_arr = np.array(high)
        # Create a boolean mask for pixels within the color range
        color_mask = np.all((low_arr <= image) & (image <= high_arr), axis=2)
        # Combine the color mask with the overall mask
        mask |= color_mask

    # Apply the mask to the original image to extract the colored objects
    colored_objects = Image.fromarray(np.uint8(image * mask[:, :, None]))

    # Save the colored objects to a file
    colored_objects.save("5_colored.png")

    image = Image.open("5_colored.png")

    # Get the RGB values for every pixel in the image and identify the color of each pixel
    width, height = image.size
    colors = []
    color_wire = {'red': 0, 'green': 0, 'blue': 0, 'yellow': 0, 'orange': 0, 'purple': 0, 'pink': 0, 'brown': 0,
                  'grey': 0}
    red_count = 0
    green_count = 0
    blue_count = 0
    yellow_count = 0
    orange_count = 0
    purple_count = 0
    pink_count = 0
    brown_count = 0
    grey_count = 0
    count_other = 0

    for y in range(height):
        row = []
        for x in range(width):
            rgb = image.getpixel((x, y))
            color = "other"
            for name, (low, high) in color_ranges.items():
                if low[0] <= rgb[0] <= high[0] and low[1] <= rgb[1] <= high[1] and low[2] <= rgb[2] <= high[2]:
                    color = name
                    if color == "red":
                        # Increment the red pixel count
                        red_count += 1
                    elif color == "green":
                        green_count += 1
                    elif color == "blue":
                        blue_count += 1
                    elif color == "yellow":
                        yellow_count += 1
                    elif color == "orange":
                        orange_count += 1
                    elif color == "purple":
                        purple_count += 1
                    elif color == "pink":
                        pink_count += 1
                    elif color == "brown":
                        brown_count += 1
                    elif color == "grey":
                        grey_count += 1
                    else:
                        count_other += 1

                    break

            row.append(color)
        colors.append(row)

    color_wire['red'] = red_count
    color_wire['green'] = green_count
    color_wire['blue'] = blue_count
    color_wire['yellow'] = yellow_count
    color_wire['orange'] = orange_count
    color_wire['purple'] = purple_count
    color_wire['pink'] = pink_count
    color_wire['brown'] = brown_count
    color_wire['grey'] = grey_count

    # Print the colors in matrix form
    #for row in colors:
        #print(row)
    #print(color_wire)
    #print(count_other)
    #max_value = max(color_wire, key=color_wire.get)

    top2 = heapq.nlargest(2, color_wire, key=color_wire.get)

    # Print the two maximum values

    j = 0

    device_point_color.append(top2[0])
    device_point_color.append(top2[1])
    print(device_point_color)

    return device_point_color

def devices_values(deviceses):
    pass_devices_value = {}
    pass_devices_value = deviceses
    print(pass_devices_value)
    return pass_devices_value


def object_detect(n):
    device = devices_detect(n)
    a = device['Arduino']
    L = device['LED']
    La = device['Laser']
    i = 0
    devices_values(device)
    while i < a:
        Ar = "Arduino_UNO" + str(i)
        pin = arduino_pin_series(Ar)
        i += 1
    pin_name = list(pin.keys())
    pin_colors = list(pin.values())


    # LED
    j = 0
    while j < L:
        j += 1
        LE = "LED" + str(j)
        pin_color = device_color(LE)
        device_point_color[LE] = pin_color

    # pin color
    y = 0
    while y < 32:
        if pin_colors[y] != "unplug":
            key = pin_name[y]
            value = pin_colors[y]
            pin_plug[key] = value
        y += 1

    # pin select
    led = 0
    while led < L:
        led = led + 1
        LE = "LED" + str(led)
        f = 0
        while f < 2:
            value_to_find = device_point_color[LE][f]
            # key_to_find = None
            for key, value in pin_plug.items():
                if value == value_to_find:
                    device_point_color[LE][f] = key
                    break
            f = f + 1
    print(device_point_color)
    return device_point_color

#object_detect(n)
#def device_value():












