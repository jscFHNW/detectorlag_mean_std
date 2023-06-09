import meanroishutter_mock as mrs
import numpy as np
from scipy.ndimage import gaussian_filter, median_filter


def test_version():
    assert mrs.__version__ == '0.1.0'


def test_bin_img():

    img_size = 100
    img_value = 100
    img = create_test_image(img_size, img_value)

    bin_img = mrs.get_bin_img(img, img_value/2)

    #create control array
    control = np.zeros((100,100), bool)
    control[:, :50] = True

    # all booleans must be False
    assert np.bitwise_xor(bin_img, control).all((0,1), where=False)



def create_test_image(size: int, value: int) -> np.array:

    # Vertical split
    test_img = np.zeros((size, size), np.uint16)
    test_img[:,:size/2] = value

    return test_img


def create_median_image(size: int, value: int) -> np.array:

    # Vertical split
    test_img = np.zeros((size, size), np.uint16)
    test_img[:,:size/2] = value

    return test_img

def create_gauss_image(size: int, value: int) -> np.array:

    sigma = 1

    # Vertical split
    test_img = gaussian_filter(np.zeros((size, size), np.uint16), sigma)
    test_img[:,:size/2] = value

    return test_img