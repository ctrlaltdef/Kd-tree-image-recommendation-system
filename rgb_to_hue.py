def rgb_to_hue(rgb):
    r, g, b = rgb
    
    # Convert RGB values to the range [0, 1]
    r /= 255.0
    g /= 255.0
    b /= 255.0
    
    max_val = max(r, g, b)
    min_val = min(r, g, b)
    
    # Calculate the delta between max and min
    delta = max_val - min_val
    
    # Calculate hue
    if delta == 0:
        hue = 0  # Undefined (achromatic)
    elif max_val == r:
        hue = 60 * (((g - b) / delta) % 6)
    elif max_val == g:
        hue = 60 * (((b - r) / delta) + 2)
    else:
        hue = 60 * (((r - g) / delta) + 4)
    
    # Adjust hue to be in the range [0, 360]
    hue = round(hue)
    if hue < 0:
        hue += 360
    
    return hue
