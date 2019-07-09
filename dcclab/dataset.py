from dcclab import ImageCollection
from typing import Union, List
import numpy as np


class Dataset(ImageCollection):
    def __init__(self, images: List['Image']=None, imagesArray: np.ndarray=None, pathPattern: str=None):

        """ todo: has to load an image folder possibly containing sub folders for different classes
            and sub folders for labels or image tagged as label... and possibly load a specified label folder ?
        """

        super().__init__(images, imagesArray, pathPattern)


# todo: check images have same shape
