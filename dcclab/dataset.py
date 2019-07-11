from dcclab import ImageCollection, Image
from typing import List
import pandas as pd
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
        self.type = None  # Classification, Semantic Classification, Regression (more for table data: Not implemented)...
        self.supervised = None
        self.model = None

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

    def loadCollectionFiles(self, source):
        # TODO: support non-semantic structure.
        """ self.collections = {'sourceName': [list(imageFiles), list(labelFiles)], ...} """

        folderName = os.path.basename(source)
        if self.labelTag not in folderName:
            self.collections[folderName] = self.getImageAndLabelFiles(source)
        else:
            folderName = [key for key in self.collections.keys() if key in folderName][0]
            self.collections[folderName][1] = self.getFiles(source, absolute=True)

    def loadCollectionObjects(self):
        """ self.collections = {'sourceName': ImageCollection(), ...} """

        for key in self.collections:
            imageFiles, labelFiles = self.collections[key]
            images = [Image(path=file) for file in imageFiles]
            self.collections[key] = ImageCollection(images=images)

            if len(labelFiles) != 0:
                labels = [Image(path=file).channels[0] for file in labelFiles]
                self.collections[key].setLabelledComponents(labels=labels)
                self.type = "Semantic classification"
                self.supervised = True

    def report(self):
        # Temporary

        collectionsInfo = []
        globalClassInfo = {}
        classNames = {}

        for source in self.collections:
            collection = self.collections[source]
            classInfo = collection.labelValues

            if collection.hasLabelledComponents:
                classValues, classCounts = list(classInfo.keys()), list(classInfo.values())

                if 0 in classValues and len(classValues) == 2:
                    classNames[0] = "background"
                    classNames[sorted(classValues)[-1]] = source

                for value, count in classInfo.items():
                    if value not in globalClassInfo:
                        globalClassInfo[value] = count
                    else:
                        globalClassInfo[value] += count

                totalCount = np.sum(list(classInfo.values()))
                for value in classInfo:
                    classInfo[value] = np.round(int(classInfo[value]) / totalCount * 100, 1)
            else:
                classValues, classCounts = None, None

            collectionsInfo.append([source, collection.numberOfImages, collection.hasLabelledComponents, classValues,
                                    classCounts, collection.imagesAreSimilar, collection.images[0].shape])

        df = pd.DataFrame(collectionsInfo, columns=["source", "nbOfImages", "hasLabels", "clsValues", "clsRatios", "sameShape", "shape"])

        print("\n", df.to_string(index=False), "\n")

        totalCount = np.sum(list(globalClassInfo.values()))
        for value in globalClassInfo:
            globalClassInfo[value] = np.round(int(globalClassInfo[value]) / totalCount * 100, 1)

        print("NbOfClasses = ", len(globalClassInfo.keys()) if len(globalClassInfo) != 0 else None)
        if len(classNames) == 0:
            print("Class values = ", list(globalClassInfo.keys()))
        else:
            print("Class values = ", ["{}: {}".format(value, classNames[value]) for value in list(globalClassInfo.keys())])
        print("Class ratios = ", list(globalClassInfo.values()))
        print("ML Type = ", self.type if self.type is not None else "unknown")
        print("Supervised = ", self.supervised if self.supervised is not None else "unknown")
        print("Model = ", self.model if self.model is not None else "unknown")

        # - pixel values for the labels correspond to class indexes
        # - image format is png
        # - classes are balanced (ratio)
        # - the dataset is big enough
        # - ...

    def applyLabelsFromSourceNames(self):
        for source in self.collections:
            collection = self.collections[source]
            assert not collection.hasLabelledComponents, "Collection already has labels"

            for image in collection.images:
                for channel in image.channels:
                    channel.setLabelledComponents(source)

        self.type = "Classification"

    def setModel(self, model=None):
        if model is None:
            # infer model...
            if self.type is "Semantic classification":
                # use resnet50... check size...
                pass

    def train(self):
        pass

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


if __name__ == '__main__':
    dataset = Dataset(directory="./tests/testData/labelledDataset")
    # dataset.applyLabelsFromSourceNames()
    # dataset.report()


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
