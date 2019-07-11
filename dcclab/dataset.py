from dcclab import ImageCollection, Image, Channel
from typing import List
import numpy as np

import os

"""
Machine Learning Dataset

It needs to be able to load such data structures: 

<SEMANTIC>
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

<SEMANTIC>
data/
|-- images
    |-- 0.png  # [each image might contain multiple classes]
    |-- ...
|-- labels
    |-- 0.png
    |-- ...

OR

<NOT semantic>  # labels are foldernames  # ** this structure cannot be infered : user has to specify if its semantic or not
data/
|-- cats
    |-- 0.png
    |-- ...
|-- dogs
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
        self.labelTag = 'label'
        self.collections = dict()

        self.loadAllCollections()

        self.report()

    def loadAllCollections(self):
        folders = self.getFolders(self.directory)
        files = self.getFiles(self.directory)

        if len(folders) != 0:
            assert len(files) == 0, "Cannot infer datafile structure if a directory has folders and files."

            orderedFolders = [f for f in folders if self.labelTag not in f]
            orderedFolders.extend([f for f in folders if self.labelTag in f])
            for folder in orderedFolders:
                self.loadCollectionFiles(os.path.join(self.directory, folder))

        elif len(files) != 0:
            self.loadCollectionFiles(self.directory)

        else:
            raise FileNotFoundError

        self.loadCollectionObjects()

        # ultimately fills the collections with a nametag and an ImageCollection object
        for nametag, images, labels in collections:
            self.collections['nametag'] = ImageCollection(images=images)
            if labels is not None:
                self.collections['nametag'].setLabelledComponents(labels=labels)

    def report(self):
        # - images have same shape
        # - labels are present
        # - number of classes
        # - pixel values for the labels correspond to class indexes
        # - image format is png
        # - classes are balanced (ratio)
        # - the dataset is big enough
        # - ...

    # offer to label from folder names if its a non-semantic classification

    @staticmethod
    def getFolders(source):
        return list(os.walk(source))[0][1]

    @staticmethod
    def getFiles(source, absolute=False):
        filenames = list(os.walk(source))[0][2]
        if absolute:
            return [os.path.join(source, fn) for fn in filenames]
        else:
            return filenames

    def getImageAndLabelFiles(self, source) -> list:
        filenames = self.getFiles(source)
        imageFiles = [os.path.join(source, fn) for fn in filenames if self.labelTag not in fn]
        labelFiles = [os.path.join(source, fn) for fn in filenames if self.labelTag in fn]
        return [imageFiles, labelFiles]


"""

Maybe replace ImageCollection with a possible ML Collection ? ...

"""


class MLCollection:
    supportedTypes = ["Image", "Spectra"]

    def __new__(cls, data: List[np.ndarray]):
        datatype = None
        # check data dimensions and try to infer data type

        if datatype == "Image":
            return super(MLCollection, cls).__new__(MLImageCollection)
        elif datatype == "Spectra":
            return super(MLCollection, cls).__new__(MLSpectraCollection)

    def augment(self):
        pass


class MLImageCollection(ImageCollection):  # ?

    def augment(self):
        # Keras image augmentation generator
        pass


class MLSpectraCollection:  # ?  (SpectraCollection)

    def augment(self):
        # Spectra augmentation technique
        pass
