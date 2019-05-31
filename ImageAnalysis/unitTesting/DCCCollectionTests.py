try:
    import unittest
    import DCCImage
    import DCCImagesExceptions as DCCExcep
    import numpy as np
    from DCCImageCollection import DCCImageCollection
    from unittest.mock import Mock, patch
except ImportError:
    print("Please install the required libraries.")


class TestDCCImageCollecionConstructor(unittest.TestCase):

    def testValidConstructorEmpty(self):

        valid = True
        try:
            DCCImageCollection([])
        except AttributeError:
            valid = False

        self.assertTrue(valid)

    def testValidConstructorOneElement(self):
        array = np.ones((130, 145), dtype=np.float32)
        image = DCCImage.DCCImage(array)
        collection = DCCImageCollection([image])
        self.assertIsInstance(collection, DCCImageCollection)

    def testValidConstructor100Elements(self):
        imageList = []
        for i in range(100):
            array = np.ones((1250, 1251), dtype=np.float32)
            array[i][i] = i
            image = DCCImage.DCCImage(array)
            imageList.append(image)
        collection = DCCImageCollection(imageList)
        self.assertIsInstance(collection, DCCImageCollection)

    def testInvalidConstructor1Element(self):
        image = np.ones((10, 10))
        with self.assertRaises(DCCExcep.NotDCCImageException):
            DCCImageCollection([image])

    def testInvalidConstructor11Elements(self):
        imageList = []
        for i in range(10):
            array = np.ones((1250, 1251), dtype=np.float32)
            array[i][i] = i
            image = DCCImage.DCCImage(array)
            imageList.append(image)
        imageList.append(np.ones((10, 10)))
        with self.assertRaises(DCCExcep.NotDCCImageException):
            DCCImageCollection(imageList)


class TesDCCImageCollectionMethods(unittest.TestCase):

    def setUp(self) -> None:
        self.imageList = []
        for i in range(5):
            array = np.ones((1250, 1251), dtype=np.float32)
            array[i][i] = i
            image = DCCImage.DCCImage(array)
            self.imageList.append(image)
        self.collection = DCCImageCollection(self.imageList)

    def testImageInCollectionInvalidImage(self):
        invalidImage = np.ones((1250, 1251), dtype=np.float32)
        with self.assertRaises(DCCExcep.NotDCCImageException):
            self.collection.isImageInCollection(invalidImage)

    def testImageNotInCollection(self):
        arrayNotInCollection = np.ones((1250, 1251), dtype=np.float32)
        arrayNotInCollection[0][0] = 0.00001
        imageNotInCollection = DCCImage.DCCImage(arrayNotInCollection)
        self.assertFalse(self.collection.isImageInCollection(imageNotInCollection))

    def testImageInCollection(self):
        imageInCollection = self.imageList[-1].copyDCCImage()
        self.assertTrue(self.collection.isImageInCollection(imageInCollection))

    def testGetIndexOfInvalidImage(self):
        invalidImage = np.ones((1250, 1251), dtype=np.float32)
        with self.assertRaises(DCCExcep.NotDCCImageException):
            self.collection.getIndexOfImage(invalidImage)

    def testGetIndexOfImageNotInCollection(self):
        arrayNotInCollection = np.ones((1250, 1251), dtype=np.float32)
        arrayNotInCollection[0][0] = 0.00001
        imageNotInCollection = DCCImage.DCCImage(arrayNotInCollection)
        with self.assertRaises(DCCExcep.ImageNotInCollectionException):
            self.collection.getIndexOfImage(imageNotInCollection)

    def testGetIndexImageInCollection(self):
        imageInCollection = self.imageList[2].copyDCCImage()
        self.assertEqual(self.collection.getIndexOfImage(imageInCollection), 2)

    def testAddInvalidImage(self):
        invalidImage = np.ones((1250, 1251), dtype=np.float32)
        with self.assertRaises(DCCExcep.NotDCCImageException):
            self.collection.addDCCImage(invalidImage)

    def testAddImageAlreadyIn(self):
        imageAlreadyIn = self.imageList[-1]
        with self.assertRaises(DCCExcep.ImageAlreadyInCollectionException):
            self.collection.addDCCImage(imageAlreadyIn)

    def testAddImageNotAlreadyIn(self):
        imageNotAlreadyIn = DCCImage.DCCImage(np.zeros((1250, 1251), dtype=np.float32))
        indexOfAddedImage = self.collection.addDCCImage(imageNotAlreadyIn)
        self.assertEqual(indexOfAddedImage, 5)

    def testRemoveAtIndexOutOfBound(self):
        with self.assertRaises(IndexError):
            self.collection.removeAtIndex(5)

    def testRemoveImageAtIndex(self):
        imageToRemove = self.imageList[-1]
        removedImage = self.collection.removeAtIndex(-1)
        self.assertTrue(imageToRemove == removedImage)

    def testRemoveImageWithInvalidImage(self):
        invalidImage = np.ones((125, 12547), dtype=np.float32)
        with self.assertRaises(DCCExcep.NotDCCImageException):
            self.collection.removeDCCImage(invalidImage)

    def testRemoveImageWithImageNotInCollection(self):
        arrayNotInStack = np.ones((1250, 1251), dtype=np.float32)
        arrayNotInStack[0][0] = 0.00001
        imageNotInStack = DCCImage.DCCImage(arrayNotInStack)
        with self.assertRaises(DCCExcep.ImageNotInCollectionException):
            self.collection.removeDCCImage(imageNotInStack)

    def testRemoveImageWithImage(self):
        imageInStack = self.imageList[0].copyDCCImage()
        indexOfRemovedImage = self.collection.removeDCCImage(imageInStack)
        self.assertEqual(indexOfRemovedImage, 0)

    def testGetNumberOfImages(self):
        numberOfImages = len(self.imageList)
        self.assertEqual(self.collection.getNumberOfImages(), numberOfImages)

    def testGetNumberOfImagesAddedImage(self):
        numberOfImages = len(self.imageList)
        imageNotAlreadyIn = DCCImage.DCCImage(np.zeros((1250, 1251), dtype=np.float32))
        self.collection.addDCCImage(imageNotAlreadyIn)
        self.assertEqual(self.collection.getNumberOfImages(), numberOfImages + 1)

    def testGetNumberOfImagesRemovedImage(self):
        numberOfImages = len(self.imageList)
        self.collection.removeAtIndex(0)
        self.assertEqual(self.collection.getNumberOfImages(), numberOfImages - 1)

    def testImageCollectionAsNumpyArray(self):
        imageArray = np.array(self.imageList)
        arrayFromCollection = self.collection.asNumpyArray()
        self.assertTrue(np.array_equal(imageArray, arrayFromCollection))

    def testImageCollectionAsList(self):
        listFromCollection = self.collection.asList()
        self.assertTrue(listFromCollection == self.imageList)

    def testClearCollection(self):
        self.collection.clearAll()
        self.assertTrue(len(self.collection) == 0)

    @patch("matplotlib.pyplot.show", new=Mock)
    def testShowImages(self):
        nbOfImagesShown = self.collection.showImages()
        self.assertEqual(nbOfImagesShown, 5)

    def testIndexingOutOfBound(self):
        image = DCCImage.DCCImage(np.ones((5, 5), dtype=np.float32))
        listOfImage = DCCImageCollection([image])
        with self.assertRaises(IndexError):
            listOfImage[2]

    def testIndexing(self):
        image = DCCImage.DCCImage(np.ones((5, 5), dtype=np.float32))
        listOfImage = DCCImageCollection([image])
        self.assertTrue(listOfImage[0] == image)


if __name__ == '__main__':
    unittest.main()
