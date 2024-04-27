import os

# Folder containing the images
folder_path = "IMGS"

# Get the list of files in the folder
files = os.listdir(folder_path)

# Rename each file sequentially
for i, file in enumerate(files):
    # Split the file name and extension
    filename, file_extension = os.path.splitext(file)
    
    # Construct the new file name with a prefix and the original extension
    new_filename = f"image_{i + 1}{file_extension}"
    
    # Rename the file
    os.rename(os.path.join(folder_path, file), os.path.join(folder_path, new_filename))

print("Files renamed successfully!")