#FILE FOR SERIALISATION OF THE KDTREE
import os
import tkinter as tk
from tkinter import filedialog
from color_extraction import*
from kd_tree import insert
from nearest_neighbour_search import nearest_neighbor_search
from rgb_to_hue import*
from saturation import*
from value import*

dataset_folder = "IMGS"
root=None
with open('output.txt', 'w') as file:
    # Iterate over files in the dataset folder
    for filename in os.listdir(dataset_folder):
        image_path = os.path.join(dataset_folder, filename)
        #to calculate hsv values of each tuple to store in kdtree
        rgb_tuple = img_to_rgb(image_path)
        hue = int(rgb_to_hue(rgb_tuple))
        satur = int(saturation(rgb_tuple))
        val = int(value(rgb_tuple))
        hsv_tup = (hue, satur, val)
        # Insert data and capture the returned root
        root = insert(root, filename, hsv_tup)
        if root is None:
            break
        # Write the root to the text file
    file.write(str(root) + '\n')