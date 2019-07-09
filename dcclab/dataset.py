from dcclab import ImageCollection
from typing import Union, List
import numpy as np


"""
Machine Learning Dataset

It needs to be able to load such data structures: 

data/
|-- type_A
    |-- 0.png
    |-- ...
|-- type_A_labels
    |-- 0.png
    |-- ...
|-- type_B
|-- type_B_labels
|-- mixed
|-- mixed_labels
|-- ...

OR 

data/
|-- images
    |-- 0.png  # [each image might contain multiple classes]
    |-- ...
|-- labels
    |-- 0.png
    |-- ...


+ some variants considering the fact that the labels might not exist yet.


In the first case it has to seperate and remember each type (or source?) by their name.
This looks to me like each type (called class in ML classification) or source, with its labels, is one image collection object. 
This means that a Dataset Class has to load multiple ImageCollections (and remember their names).

I would then define a Dataset class without heritage, that intentiate different ImageCollection objects (or maybe 
a new `MLCollection` object heriting from ImageCollection).
"""


class Dataset:
    def __init__(self, directory: str):
        self.directory = directory
        self.collections = dict()

        self.loadCollections()

        self.report()

    def loadCollections(self):
        # check inside input directory and search for possible subfolders and labels
        collections = {'nametag1': [['Images'], ['Labels']]}

        # ultimately fills the collections with a nametag, images and labels
        for nametag, images, labels in collections:
            self.collections['nametag'] = ImageCollection(images=images)
            if labels is not None:
                self.collections['nametag'].loadLabels(labels)

    def report(self):
        # - images have same shape
        # - image classes
        # - class balance
        # - ...
        pass


"""

Maybe replace ImageCollection with a possible ML Collection ? ...

"""


class MLCollection:
    supportedTypes = ["Image", "Spectra"]

    def __new__(cls, *args, **kwargs):
        pass

    def augment(self):
        pass


class MLImageCollection(ImageCollection):  # ?

    def augment(self):
        # Keras image augmentation generator
        pass


class MLSpectraCollection('SpectraCollection'):  # ?

    def augment(self):
        # Spectra augmentation technique
        pass
