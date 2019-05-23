import numpy as np
from skimage import color


class DCCImage:
    def __init__(self, image):
        if type(image) == np.ndarray:
            self.pixelArray = image
