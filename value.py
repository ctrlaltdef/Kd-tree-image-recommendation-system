def value(rgb):
    r, g, b = rgb
    r /= 255.0
    g /= 255.0
    b /= 255.0
    
    cmax = max(r, g, b)
    cmin = min(r, g, b)
    delta = cmax - cmin

    # Calculate Value
    value = cmax
    value =value *100
    value =value //1
    return value