from PIL import Image

def img_to_rgb(filename):
    # Open the image file
    image = Image.open(filename)

    # Convert the image to RGB mode
    image = image.convert("RGB")

    # Get the width and height of the image
    width, height = image.size

    # Get the pixel RGB values
    pixels = list(image.getdata())

    # Reshape the pixel data into a 2D tuple of tuples (height x width)
    pixels_2d = tuple(tuple(pixels[i * width:(i + 1) * width]) for i in range(height))


    # Example: Print the RGB value of the pixel at position (x, y)
    totalr=0
    totalg=0
    totalb=0
    count=0
    #for loop to calculate the total sum of the rgb tuples
    for x in range(0,width,5):
            for y in range (0,height,5):
                rgbtuple=pixels_2d[y][x]
                totalr+=rgbtuple[0]
                totalg+=rgbtuple[1]
                totalb+=rgbtuple[2]
                count+=1
    #calculating the average color on the image by dividing total rgb values of  image by count(the no of pixels)            
    avgr=totalr//count
    avgg=totalg//count
    avgb=totalb//count
    totalimagetuple=(avgr,avgg,avgb)
    #return the final tuple 
    return(totalimagetuple)





