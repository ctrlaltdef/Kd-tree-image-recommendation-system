import os
import sys
from PIL import Image, ImageTk
from tkinter import filedialog
from color_extraction import*
from kd_tree import*
from nearest_neighbour_search import*
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from rgb_to_hue import*
from saturation import*
from value import*
import shutil
from tkinter import filedialog, messagebox
import ast
import copy

def load_images(folder_path, desired_size):
    images = []
    #load all the images from the IMGS folder. this function has been called theoughout the code where 
    #loading and displaying images was needed
    try:
        for filename in os.listdir(folder_path):
            image_path = os.path.join(folder_path, filename)
            image = Image.open(image_path)
            image = image.resize(desired_size)
            image_tk = ImageTk.PhotoImage(image)
            images.append((image, image_tk, filename, image_path))  # Include image path
    except FileNotFoundError:
        print(f"Folder '{folder_path}' not found.")
    return images

def display_images(canvas, images, num_cols, spacing):
    #function for displaying all the images on the screen 
    for i, (image, image_tk, filename, _) in enumerate(images):  # Extract image path from tuple
        row = i // num_cols
        col = i % num_cols
        x = col * (desired_size[0] + spacing)  # Adjust x coordinate with spacing
        y = row * (desired_size[1] + spacing*2) # Adjust y coordinate with spacing
        canvas.create_image(x, y, anchor=tk.NW, image=image_tk)
        canvas.create_text(x + desired_size[0] // 2, y + desired_size[1] + 10, text=filename, anchor=tk.CENTER)

def kdtreee():
    with open('output.txt', 'r') as file:
        # Initialize an empty dictionary to store the merged data
        kd_tree = {}
        # file.seek(0)
        for line in file:
        # last_line = file.readlines()[-1]
            try:
                # Parse each line into a dictionary
                kd_tree = ast.literal_eval(line)
            except ValueError as e:
                print("Error parsing data:", e)
    # print(kd_tree)
    return kd_tree


def delete_image(image_path):
    #to delete the selected image from the dataset
    try:
        os.remove(image_path)
        messagebox.showinfo("Success", "Image deleted successfully!")
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found!")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def delete_and_display_remaining_images(canvas, images, deleted_filename):
    #just delete the existing canvas/window and display another window with pictures in updated dataset
    updated_images = [image for image in images if image[2] != deleted_filename]
    canvas.delete("all")
    display_images(canvas, updated_images, num_cols, spacing)


def display_similar_images(similar_images):
    # Create a new Tkinter window for displaying similar images
    similar_window = tk.Toplevel()
    similar_window.title("Similar Images")
    
    # Create a frame to contain the canvas and scrollbar
    frame = tk.Frame(similar_window)
    frame.pack(fill=tk.BOTH, expand=True)

    # Create a canvas that fills the frame
    canvas = tk.Canvas(frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Create a scrollbar
    scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Create a canvas that fills the frame and is shifted down
    canvas = tk.Canvas(frame)
    canvas.place(x=0, y=30, relwidth=1, relheight=1)  # Shifted down by 10 pixels

    # Configure the canvas to work with the scrollbar
    canvas.config(yscrollcommand=scrollbar.set)

    # Bind the scrollbar to the canvas
    canvas.bind('<Configure>', lambda event: canvas.configure(scrollregion=canvas.bbox("all")))

    # Load and display similar images
    num_cols = 5 # Number of columns to display the images
    spacing = 10  # Adjust spacing as desired
    image_tk_list = []  # List to store references to PhotoImage objects
    for i, (filename, color) in enumerate(similar_images):
        image_path = os.path.join(folder_path, filename)
        image = Image.open(image_path)
        image = image.resize(desired_size)
        image_tk = ImageTk.PhotoImage(image)
        image_tk_list.append(image_tk)  # Store reference to PhotoImage object
        row = i // num_cols
        col = i % num_cols
        x = col * (desired_size[0] + spacing)  # Adjust x coordinate with spacing
        y = row * (desired_size[1] + spacing*2) # Adjust y coordinate with spacing
        canvas.create_image(x, y, anchor=tk.NW, image=image_tk)
        canvas.create_text(x + desired_size[0] // 2, y + desired_size[1] + 10, text=filename, anchor=tk.CENTER)
    
    # Keep a reference to the PhotoImage objects to prevent them from being garbage collected
    similar_window.image_tk_list = image_tk_list

    # Run the Tkinter event loop to keep the pop-up window open
    similar_window.mainloop()

def handle_dropdown_selection(filename):
    #hadnle the dropdown selestion bar to display all the image names as options
    print("Dropdown selection event triggered.")
    print("Selected filename:", filename)
    image_path = [img[3] for img in images if img[2] == filename][0]  # Extract full path
    rgb_tuple = img_to_rgb(image_path)
    hue= int(rgb_to_hue(rgb_tuple))
    satur= int(saturation(rgb_tuple))
    val= int(value(rgb_tuple))
    query=(hue,satur,val)
    kd_tree=kdtreee()
    similar_images = nearest_neighbor_search(kd_tree, query, k=10)
    print(similar_images)
    display_similar_images(similar_images)

lst=[]
def handle_dropdown_deletion(filename):
    #handle the dropdown selestion bar to display all the image names as options
    print("Dropdown deletion event triggered.")
    print("Selected filename:", filename)
    
    # Find the image path corresponding to the selected filename
    image_path = [img[3] for img in images if img[2] == filename][0]  # Extract full path
    
    # Retrieve RGB values from the image
    rgb_tuple = img_to_rgb(image_path)
    hue = int(rgb_to_hue(rgb_tuple))
    satur = int(saturation(rgb_tuple))
    val = int(value(rgb_tuple))
    query = (hue, satur, val)
    
    # Confirm deletion with user
    if messagebox.askyesno("Delete Image", "Do you want to delete this image?"):
        try:
            # Make a copy of the current KD-tree
            kd_tree = kdtreee()
            # print("OLD")
            # print(kd_tree_copy)
            # Delete the specified node from the KD-tree
            kd_tree = deleteNode(kd_tree, query)
            with open('output.txt', 'w') as file:
            # write_kd_tree_to_file(kd_tree_copy, file)
                file.write(str(kd_tree) + '\n')
            
            
            # Delete the image file from disk
            delete_image(image_path)
            lst.append(filename)
            
            # Update the list of images to exclude the deleted image
            remaining_images = [img for img in images if img[2] not in lst]
            
            # Clear the canvas before re-drawing
            canvas.delete("all")
            
            # Display the remaining images on the canvas
            display_images(canvas, remaining_images, num_cols, spacing)
            
            # Update the dropdown menu values
            dropdown_values = [img[2] for img in remaining_images]
            dropdown_delete['values'] = dropdown_values
            dropdown_delete.set('Delete image')  # Reset dropdown selection (optional)
            
            print('Deletion successful!')
        except Exception as e:
            print("An error occurred during deletion:", e)
    else:
        print("Deletion canceled.")

def insert_image():
    #function to insert images into the dataset adn kdtree simultaneously
    canvas.delete('all')
    
    window.withdraw()
    file_path = filedialog.askopenfilename(title="Select Image", filetypes=(("Image files", ".jpg;.jpeg;.png"), ("All files", ".*")))
    
    if file_path:
        # Get the filename from the file path
        filename = os.path.basename(file_path)
        
        # Define the destination folder where the image will be copied
        destination_folder = "IMGS"
        
        try:
            # Copy the image to the destination folder
            shutil.copy(file_path, os.path.join(destination_folder, filename))
            copied_image_path = os.path.join(destination_folder, filename)
            
            # Display the selected image in a new window
            new_window = tk.Toplevel()
            new_window.title("Selected Image")
            
            # Load the selected image
            selected_image = Image.open(file_path)
            # Convert the image to Tkinter format
            tk_image = ImageTk.PhotoImage(selected_image)
            
            # Create a label to display the image
            label = tk.Label(new_window, image=tk_image)
            label.image = tk_image  # Keep a reference to the image to prevent it from being garbage collected
            label.pack()
            # Function to handle window close event
            def on_close():
                rgb_tuple = img_to_rgb(copied_image_path)
                hue= int(rgb_to_hue(rgb_tuple))
                satur= int(saturation(rgb_tuple))
                val= int(value(rgb_tuple))
                query=(hue,satur,val)
                kd_tree=kdtreee()
                kd_tree=insert(kd_tree, filename, query)
                # print(kd_tree)
                with open('output.txt', 'w') as file:
                    file.write(str(kd_tree) + '\n')
                new_window.destroy()
                sys.exit()  # Terminate the program
            
            # Bind the window close event to the on_close function
            new_window.protocol("WM_DELETE_WINDOW", on_close)
            # Ask for confirmation before inserting the image
            confirm_insertion = messagebox.askyesno("Confirm", "Are you sure you want to insert this image?")
            
            if confirm_insertion:
                # Display a message box indicating successful insertion
                messagebox.showinfo("Success", "Image successfully inserted!")
                on_close() # Terminate the program
                sys.exit()
                
            else:
                # If the user selects no, close the window and do nothing
                on_close()
        except Exception as e:
            print("An error occurred:", e)
    else:
        print("No image selected.")



#-----------------------------------------------------------------------------------------------------------        
# Create a Tkinter window
window = tk.Tk()
window.title("Image Viewer")
window.geometry("1250x700")

# Relative path to the folder containing images
cwd = os.getcwd()
folder_path = "IMGS"

# Define the desired size for all images
desired_size = (137, 137)

# Load and resize images
images = load_images(folder_path, desired_size)

# Create a frame to contain the canvas and scrollbar
frame = tk.Frame(window)
frame.pack(fill=tk.BOTH, expand=True)

# Create a canvas that fills the frame and is shifted down
canvas = tk.Canvas(frame)
canvas.place(x=0, y=30, relwidth=1, relheight=1)  # Shifted down by 10 pixels

# Create a scrollbar
scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configure the canvas to work with the scrollbar
canvas.config(yscrollcommand=scrollbar.set)

# Bind the scrollbar to the canvas
canvas.bind('<Configure>', lambda event: canvas.configure(scrollregion=canvas.bbox("all")))

# Display images with spacing
num_cols = 9  # Number of columns to display the images
spacing = 13.5  # Adjust spacing as desired
display_images(canvas, images, num_cols, spacing)

# Create a list of image names for the dropdown menus
image_names = [image[2] for image in images]

# Dropdown menu for "Find Similar Image" option
selected_image_similar = tk.StringVar(window)
selected_image_similar.set(image_names[0])  # Set the default value
dropdown_values_similar = image_names  # Extract filenames from images
dropdown_similar = ttk.Combobox(window, values=dropdown_values_similar, state="readonly")
dropdown_similar.set('Find similar images')
dropdown_similar.place(x=0, y=0)

# Dropdown menu for "Delete Image" option
selected_image_delete = tk.StringVar(window)
selected_image_delete.set(image_names[0])  # Set the default value
dropdown_values_delete = image_names  # Extract filenames from images
dropdown_delete = ttk.Combobox(window, values=dropdown_values_delete, state="readonly")
dropdown_delete.set('Delete image')
dropdown_delete.place(x=200, y=0)

# Bind the handle_dropdown_selection function to the <<ComboboxSelected>> event for finding similar images
dropdown_similar.bind("<<ComboboxSelected>>", lambda event: handle_dropdown_selection(dropdown_similar.get()))

# Bind the handle_dropdown_deletion function to the <<ComboboxSelected>> event for deleting images
dropdown_delete.bind("<<ComboboxSelected>>", lambda event: handle_dropdown_deletion(dropdown_delete.get()))

# Insert button
insert_button = tk.Button(window, text="Insert Image", command=insert_image)
insert_button.place(x=400, y=0)

# Run the Tkinter event loop
try:
    window.mainloop()
except KeyboardInterrupt:
    # Code to handle the keyboard interrupt
    print("Program stopped manually by the user.")
    
