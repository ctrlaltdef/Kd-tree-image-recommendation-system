def saturation(rgb):
    # Step 1: Normalize RGB values
    r, g, b = rgb
    
    # Convert RGB values to the range [0, 1]
    r /= 255.0
    g /= 255.0
    b /= 255.0

    # Step 2: Find max and min RGB values
    max_rgb = max(r, g, b)
    min_rgb = min(r, g, b)

    # Step 3: Calculate delta (difference between max and min)
    delta = max_rgb - min_rgb

    # Step 4: Calculate saturation
    if max_rgb == 0:
        saturation = 0
    else:
        saturation = delta / max_rgb

    # Convert saturation to percentage
    saturation=saturation*100
    return saturation


