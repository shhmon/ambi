import numpy as np
import math

def get_whites(color):
    h, s, l = rgba_to_hsl(color)
    color_point = [math.cos(h), math.sin(h)]
    
    # Sending 255 cold white gives approx. 180deg hue
    # Sending 255 warm white gives approx. 0deg hue
    cw_dist = math.dist([math.cos(180), math.sin(180)], color_point) / 2
    ww_dist = math.dist([math.cos(0), math.sin(0)], color_point) / 2
    cw = int((1-cw_dist)*(1-s)*255)
    ww = int((1-ww_dist)*(1-s)*255)

    return cw, ww

def rgba_to_hsl(rgba):
    rgba = np.array(rgba)
    # Normalize RGB values to the range [0, 1]
    rgb = rgba[:3] / 255.0
    r, g, b = rgb

    # Find the minimum and maximum values of RGB
    cmin, cmax = np.min(rgb[:3]), np.max(rgb[:3])
    delta = cmax - cmin

    # Calculate lightness
    l = (cmax + cmin) / 2.0

    # Calculate saturation
    if delta == 0:
        s = 0
    else:
        s = delta / (1 - abs(2 * l - 1))

    # Calculate hue
    if delta == 0:
        h = 0
    elif cmax == r:
        h = 60 * (((g - b) / delta) % 6)
    elif cmax == g:
        h = 60 * (((b - r) / delta) + 2)
    elif cmax == b:
        h = 60 * (((r - g) / delta) + 4)
    else:
        h = 0  # Initialize h when delta != 0 but none of the conditions match

    return h, max(s, 0), l

def get_average_color(rgba_array):
    avg = np.average(rgba_array, axis=(0, 1))
    r, g, b = round(avg[2]), round(avg[1]), round(avg[0])
    return r, g, b

def get_color_diff(color1, color2):
    return np.linalg.norm(np.array(color2) - np.array(color1))

def find_most_occuring_color(rgba_array):
    # TODO this is borked

    # Reshape the RGBA array to 2D
    flat_array = rgba_array.reshape(-1, 4)

    # Convert the 2D array to a structured NumPy array
    rgba_structured_array = np.core.records.fromarrays(flat_array.T, names='r, g, b, a', formats='u1, u1, u1, u1')

    # Convert the structured array to a view
    rgba_view = rgba_structured_array.view(dtype=np.uint32)

    # Count occurrences of each color using unique and bincount
    unique_colors, counts = np.unique(rgba_view, return_counts=True)

    # Find the index of the most occurring color
    most_occuring_index = np.argmax(counts)

    # Extract RGB values from the most occurring color
    most_occuring_color = np.frombuffer(unique_colors[most_occuring_index].tobytes(), dtype=np.uint8)

    return tuple(most_occuring_color[:3])

def find_most_varied_color(rgba_array):
    pass

def find_most_saturated_color(rgba_array):
    pass