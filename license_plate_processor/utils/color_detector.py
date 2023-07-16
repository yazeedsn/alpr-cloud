import cv2
import numpy as np
from colorthief import ColorThief
import os
from collections import Counter
from PIL import Image
import webcolors
import colorsys

# def get_image_color(image):
#     output_dir = 'temp'
#     os.makedirs(output_dir, exist_ok=True)

#     # Save the padded image with its name being the HSV values
#     output_filename = 'padded_image.jpg'
#     output_path = os.path.join(output_dir, output_filename)
#     cv2.imwrite(output_path, image)

#     # Use ColorThief library to get the dominant color
#     ct = ColorThief(output_path)
#     dominant_color = ct.get_color(quality=1)

#     car_color = get_color_name(dominant_color)

#     # Delete the temporary image file
#     # os.remove(output_path)

#     return car_color



def get_color_name(rgb_value):
    # color_names = {
    #     'red': [[0, 20], [65, 100], [25, 75]],
    #     'white': [[0, 360], [0, 100], [85, 100]],
    #     'black': [[0, 360], [0, 100], [0, 8]],
    #     'silver': [[0, 360], [0, 10], [65, 100]],
    #     'blue': [[180, 260], [60, 100], [25, 90]],
    #     'gray': [[0, 360], [0, 100], [15, 65]],
    #     'green': [[75, 150], [25, 100], [15, 65]],
    #     'gold/beige': [[25, 65], [30, 75], [45, 80]],
    #     'orange': [[20, 50], [70, 100], [30, 65]],
    #     'brown': [[10, 50], [70, 100], [25, 55]],
    #     'Red': [[340, 355], [25, 100], [25, 75]]
    # }

    color_names = {
        'red': [[0, 20], [40, 100], [25, 75]],
        'brown': [[10, 50], [70, 100], [25, 55]],
        'orange': [[20, 50], [70, 100], [30, 65]],
        'gold/beige': [[25, 65], [30, 75], [45, 80]],
        'green': [[75, 150], [25, 100], [15, 65]],
        'blue': [[180, 260], [25, 100], [25, 90]],
        'Red': [[340, 355], [25, 100], [25, 75]],
        'black': [[0, 360], [0, 100], [0, 8]],
        'silver/gray': [[0, 360], [0, 10], [65, 100]],
        'white': [[0, 360], [0, 100], [85, 100]]
    }

    color_names = {
        'gray': [[0, 20], [0, 40]],
        'white': [[0, 20], [0, 80]],
        'black': [[0, 180], [0, 40]],
        'silver': [[0, 180], [0, 30]],
        'blue': [[78, 126], [40, 255]],
        'red': [[0, 8], [40, 255]],
        'green': [[36, 77], [40, 255]],
        'gold/beige': [[23, 35], [80, 255]],
        'orange': [[9, 22], [40, 255]],
        'brown': [[11, 20], [40, 255]]
    }


    #rgb normal: range (0-255, 0-255, 0.255)
    red, green, blue = rgb_value[0], rgb_value[1], rgb_value[2]
    
    # hsv_value = cv2.cvtColor(np.uint8([[rgb_value]]), cv2.COLOR_RGB2HSV)
    # hue, saturation, value = hsv_value[0, 0]

    ## normalizing values to get value between 0 and 1
    red = red/255
    green = green/255
    blue = blue/255

    hue, saturation, value = colorsys.rgb_to_hsv(red, green, blue)
    hue *= 360
    saturation *= 85
    value *= 60

    for color, ranges in color_names.items():
        hue_range = ranges[0]
        saturation_range = ranges[1]
        if hue_range[0] <= hue <= hue_range[1] and \
            saturation_range[0] <= saturation <= saturation_range[1] \
            and value >= 30:

            return color

    print("r= " + str(red) + ", g=" + str(green) + ", b=" + str(blue))
    print("hue= " + str(hue) + ", sat=" + str(saturation) + ", val=" + str(value))

    return 'unknown'



    # for color, ranges in color_names.items():
    #     hue_range = ranges[0]
    #     saturation_range = ranges[1]
    #     value_range = ranges[2]
    #     if hue_range[0] <= hue <= hue_range[1] and \
    #         saturation_range[0] <= saturation <= saturation_range[1] and \
    #         value_range[0] <= value <= value_range[1]:
    #         return color

    # return 'unknown'



def get_image_color(image):
    output_dir = 'temp'
    os.makedirs(output_dir, exist_ok=True)

    output_filename = 'car.jpg'
    output_path = os.path.join(output_dir, output_filename)
    cv2.imwrite(output_path, image)

    image = Image.open(output_path)

    image.thumbnail((100, 100))

    image = image.convert('RGB')

    # Get the pixel colors
    pixels = list(image.getdata())

    # Count the occurrences of each color
    color_counter = Counter(pixels)

    # Get the most common color and its count
    most_common_color = color_counter.most_common(1)[0][0]

    print(most_common_color)

    # Find the closest color name from the predefined list
    closest_color = find_closest_color_name(most_common_color)

    return closest_color


def find_closest_color_name(rgb_color):
    # Convert RGB color to its closest named color
    closest_color = None
    min_distance = float('inf')

    for color_name, color_rgb in webcolors.CSS3_NAMES_TO_HEX.items():
        print(rgb_color) # format = (93, 92, 90)
        print(color_rgb) # format = #f0f8ff
        distance = calculate_color_distance(rgb_color, color_rgb)
        if distance < min_distance:
            min_distance = distance
            closest_color = color_name

    return closest_color


def calculate_color_distance(rgb_color1, rgb_color2):
    # Calculate the Euclidean distance between two RGB colors
    r1, g1, b1 = rgb_color1
    r2, g2, b2 = rgb_color2
    distance = ((r2 - r1) ** 2) + ((g2 - g1) ** 2) + ((b2 - b1) ** 2)
    return distance