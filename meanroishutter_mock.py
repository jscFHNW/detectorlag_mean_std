__version__ = '0.1.0'

import numpy as np
import time
import tifffile as tiff
import random
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt

import meanroishutter as mrs


# Threshold to define ROI
mean_threshold = 0

# file mask to import
img_prefix = ""

# Directories used
source_dir = ""
dest_dir = ""

start = time.time()

def create_test_image(size: int, value: int) -> np.array:

    # Vertical split
    test_img = np.zeros((size, size), np.uint16)

    for i in range(size):
        test_img[0 + i : 1 + i, 45 + i // 12 :] = value + random.randint(-25, 25)

    test_img = gaussian_filter(test_img,sigma=3)

    return test_img

def main():

    size = 100

    img = create_test_image(size, 100)

    tiff.imshow(img, show=True, cmap='gray')
    
    x = np.array(range(0, size))

    max_cols = mrs.get_max_col(img)

    plt.plot(x, max_cols)
    plt.show()

    ret = mrs.get_from_ROI([img], 50, np.mean)[0]

    print(f"Mean of the shutter ROI of the dummy image is '{ret}'")

    ret = mrs.get_from_ROI([img], 50, np.std)[0]

    print(f"Standard deviation of the above threshold pixels is '{ret}'")


if __name__ == "__main__":
    main()