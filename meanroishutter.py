__version__ = '0.1.0'

import os
import numpy as np
import time
import tifffile
from scipy.ndimage import gaussian_filter

import xml.etree.ElementTree as xml


# Threshold to define ROI
threshold = 0

# file prefix to import/filter images located in image_dir
img_prefix = ""

# Directories containing the images to be parsed
image_dir = ""

start = time.time()

def main():

    load_config()

    images = load_images()

    means = get_from_ROI(images, threshold, np.mean)
    std_dev = get_from_ROI(images, threshold, np.std)

    # TODO: where to save the data? Apply filter?



############
# Methods
############
def load_images():
    
    all_files = os.listdir(image_dir)

    img_files = list(filter(lambda x: x.startswith(img_prefix), all_files))

    images = []

    # copy DC images
    for file in img_files :
        source = os.path.join(image_dir, file)

        # load image
        images.append(np.array(tifffile.imread(source)))

    return images


def get_from_ROI(images, threshold, func) -> np.array:

    means = []
    
    for img in images:

        # b = apply_threshold(img, threshold)
        # max_cols = get_max_col(b)        
        # max_indices = np.count_nonzero(max_cols)
        # roi = img[:,:max_indices]

        #TODO: affects all, what about outliers in the right part
        means.append(func(img[img<threshold]))

    return means



def apply_threshold(img: np.array, threshold: int) -> np.array:
    bin_img = img < threshold
    return bin_img


def get_shutter_pos(bin_img: np.array):

    shutter_pos = np.max(bin_img, 0)

    return shutter_pos


def get_max_col(img: np.array) -> np.array:

    return np.max(img,axis=0)


def check_config():
    
    if (is_invalid_path(image_dir)):
        print(f"Image directory '{image_dir}' does not exists")
        quit()

def load_config(config_path = ""):
    
    if(config_path == ""):
        config_path = os.path.join(os.getcwd(), "config.xml")

    tree = xml.parse(config_path)
    try:        
        print()
    except:
        print(f"Cannot load configuration file, ensure a the file '{config_path}' exists!")
        quit()
        
    root = tree.getroot()

    global image_dir
    image_dir = load_property(root, "imageDir")

    global img_prefix
    img_prefix = load_property(root, "imagePrefix")

    try:        
        global threshold
        threshold = load_property(root, "threshold")
    except:
        print(f"Cannot convert threshold '{threshold}' to a number! Ensure it is a 16 bit unsigned integer!")
        quit()
    
    check_config()

def load_property(xmlRoot, key):
    try:        
        prop = xmlRoot.findall(f'.//{key}')
        return prop[0].text
    except:
        print(f"Cannot deserialize '{key}' from config! Ensure the property exists!")
        quit()

def is_invalid_path(path):
    return (path == None or path == "" or os.path.isdir(path) == False)

if __name__ == "__main__":
    main()