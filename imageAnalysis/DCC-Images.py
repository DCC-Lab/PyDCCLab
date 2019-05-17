import numpy as np


class DCCImage:
    def __init__(self, image):
        if type(image) == np.ndarray:
            self.pixelArray = image
