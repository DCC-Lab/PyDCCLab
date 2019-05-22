import unittest

from torch._C import dtype

import ImageAnalysis.DCCImages as DCCImages
import ImageAnalysis.DCCImagesExceptions as dccExcep
import numpy as np


class TestDCCImageConstructor(unittest.TestCase):

    def testValidConstructor(self):
        image = DCCImages.DCCImage(np.ones((1250, 1500, 3), dtype=np.float32))
        self.assertIsInstance(image, DCCImages.DCCImage)

    def testInvalidDimensionsConstructor(self):
        with self.assertRaises(dccExcep.ImageDimensionsException):
            DCCImages.DCCImage(np.zeros(12, dtype=np.float32))

    def testInvalidTypeConstructor(self):
        with self.assertRaises(dccExcep.PixelTypeException):
            DCCImages.DCCImage(np.ones((1250, 1500, 3), dtype=np.complex))


class TestDCCImageMethods(unittest.TestCase):

    def setUp(self) -> None:
        self.array = np.ones((1250, 1251), dtype=np.float32) * 25.56
        self.array[100][100] = 100.0
        self.array[0][0] = 0.0
        self.image = DCCImages.DCCImage(self.array)

    def testEquals(self):
        testArray = np.copy(self.array)
        testImage = DCCImages.DCCImage(testArray)
        self.assertTrue(testImage == self.image)

    def testNotEquals(self):
        testArray = np.copy(self.array)
        testArray[0][0] = 0.0001
        testImage = DCCImages.DCCImage(testArray)
        self.assertFalse(testImage == self.image)

    def testInvalidEquality(self):
        testArray = np.copy(self.array)
        with self.assertRaises(dccExcep.InvalidEqualityTest):
            self.image == testArray

    def testGetDCCImageAsNumpyArray(self):
        testArray = np.copy(self.array)
        getArray = self.image.getDCCImageAsArray()
        equality = np.array_equal(testArray, getArray)
        self.assertTrue(equality)

    def testGetDCCImageWidth(self):
        width = 1250
        self.assertEqual(self.image.getDCCImageWidth(), width)

    def testGetDCCImageLength(self):
        length = 1251
        self.assertEqual(self.image.getDCCImageLength(), length)

    def testGetDCCImageChannels(self):
        nbChannel = 1
        self.assertEqual(self.image.getDCCImageNumberOfChannels(), nbChannel)

    def testGetDCCImageChannels3Channels(self):
        nbChannels = 3
        tempArray = np.zeros((1250, 1800, 3), dtype=np.float32)
        tempImage = DCCImages.DCCImage(tempArray)
        self.assertEqual(tempImage.getDCCImageNumberOfChannels(), nbChannels)

    def testGetNumberOFPixels(self):
        nbPixels = 1563750
        self.assertEqual(self.image.getNumberOfPixels(), nbPixels)

    def testToPILImage(self):
        import PIL.Image
        pilImage = PIL.Image.fromarray(np.copy(self.array))
        getPilImage = self.image.toPILImage()
        self.assertTrue(pilImage == getPilImage)

    def testCopyDCCImage(self):
        imageCopy = self.image.copyDCCImage()
        self.assertIsInstance(imageCopy, DCCImages.DCCImage)

    def testCopyDCCImageEquality(self):
        imageCopy = self.image.copyDCCImage()
        self.assertTrue(self.image == imageCopy)

    def testModifiedCopy(self):
        imageCopy = self.image.copyDCCImage()
        arrayCopy = imageCopy.getDCCImageAsArray()
        arrayCopy[100][79] = 1.2
        imageNotCopy = DCCImages.DCCImage(arrayCopy)
        self.assertFalse(self.image == imageNotCopy)


class TestDCCImageStackConstructor(unittest.TestCase):

    def testValidConstructorEmpty(self):

        valid = True
        try:
            DCCImages.DCCImageStack([])
        except AttributeError:
            valid = False

        self.assertTrue(valid)

    def testValidConstructorOneElement(self):
        array = np.ones((130, 145), dtype=np.float32)
        image = DCCImages.DCCImage(array)
        stack = DCCImages.DCCImageStack([image])
        self.assertIsInstance(stack, DCCImages.DCCImageStack)

    def testValidConstructor100Elements(self):
        imageList = []
        for i in range(100):
            array = np.ones((1250, 1251), dtype=np.float32)
            array[i][i] = i
            image = DCCImages.DCCImage(array)
            imageList.append(image)
        stack = DCCImages.DCCImageStack(imageList)
        self.assertIsInstance(stack, DCCImages.DCCImageStack)

    def testInvalidConstructor1Element(self):
        image = np.ones((10, 10))
        with self.assertRaises(dccExcep.NotDCCImageException):
            DCCImages.DCCImageStack([image])

    def testInvalidConstructor11Elements(self):
        imageList = []
        for i in range(10):
            array = np.ones((1250, 1251), dtype=np.float32)
            array[i][i] = i
            image = DCCImages.DCCImage(array)
            imageList.append(image)
        imageList.append(np.ones((10, 10)))
        with self.assertRaises(dccExcep.NotDCCImageException):
            DCCImages.DCCImageStack(imageList)


class TesDCCImageStackMethods(unittest.TestCase):

    def setUp(self) -> None:
        self.imageList = []
        for i in range(5):
            array = np.ones((1250, 1251), dtype=np.float32)
            array[i][i] = i
            image = DCCImages.DCCImage(array)
            self.imageList.append(image)
        self.stack = DCCImages.DCCImageStack(self.imageList)

    def testImageInStackInvalidImage(self):
        invalidImage = np.ones((1250, 1251), dtype=np.float32)
        with self.assertRaises(dccExcep.NotDCCImageException):
            self.stack.isImageInStack(invalidImage)

    def testImageNotInStack(self):
        arrayNotInStack = np.ones((1250, 1251), dtype=np.float32)
        arrayNotInStack[0][0] = 0.00001
        imageNotInStack = DCCImages.DCCImage(arrayNotInStack)
        self.assertFalse(self.stack.isImageInStack(imageNotInStack))

    def testImageInStack(self):
        imageInStack = self.imageList[-1].copyDCCImage()
        self.assertTrue(self.stack.isImageInStack(imageInStack))

    def testGetIndexOfInvalidImage(self):
        invalidImage = np.ones((1250, 1251), dtype=np.float32)
        with self.assertRaises(dccExcep.NotDCCImageException):
            self.stack.getIndexOfImage(invalidImage)

    def testGetIndexOfImageNotInStack(self):
        arrayNotInStack = np.ones((1250, 1251), dtype=np.float32)
        arrayNotInStack[0][0] = 0.00001
        imageNotInStack = DCCImages.DCCImage(arrayNotInStack)
        with self.assertRaises(dccExcep.ImageNotInStackException):
            self.stack.getIndexOfImage(imageNotInStack)

    def testGetIndexImageInStack(self):
        imageInStack = self.imageList[2].copyDCCImage()
        self.assertEqual(self.stack.getIndexOfImage(imageInStack), 2)

    def testAddInvalidImage(self):
        invalidImage = np.ones((1250, 1251), dtype=np.float32)
        with self.assertRaises(dccExcep.NotDCCImageException):
            self.stack.addDCCImage(invalidImage)

    def testAddImageAlreadyIn(self):
        imageAlreadyIn = self.imageList[-1]
        with self.assertRaises(dccExcep.ImageAlreadyInStackException):
            self.stack.addDCCImage(imageAlreadyIn)

    def testAddImageNotAlreadyIn(self):
        imageNotAlreadyIn = DCCImages.DCCImage(np.zeros((1250, 1251), dtype=np.float32))
        indexOfAddedImage = self.stack.addDCCImage(imageNotAlreadyIn)
        self.assertEqual(indexOfAddedImage, 5)

    def testRemoveAtIndexOutOfBound(self):
        with self.assertRaises(IndexError):
            self.stack.removeAtIndex(5)

    def testRemoveImageAtIndex(self):
        imageToRemove = self.imageList[-1]
        removedImage = self.stack.removeAtIndex(-1)
        self.assertTrue(imageToRemove == removedImage)

    def testRemoveImageWithInvalidImage(self):
        invalidImage = np.ones((125, 12547), dtype=np.float32)
        with self.assertRaises(dccExcep.NotDCCImageException):
            self.stack.removeDCCImage(invalidImage)

    def testRemoveImageWithImageNotInStack(self):
        arrayNotInStack = np.ones((1250, 1251), dtype=np.float32)
        arrayNotInStack[0][0] = 0.00001
        imageNotInStack = DCCImages.DCCImage(arrayNotInStack)
        with self.assertRaises(dccExcep.ImageNotInStackException):
            self.stack.removeDCCImage(imageNotInStack)

    def testRemoveImageWithImage(self):
        imageInStack = self.imageList[0].copyDCCImage()
        indexOfRemovedImage = self.stack.removeDCCImage(imageInStack)
        self.assertEqual(indexOfRemovedImage, 0)

    def testDetNumberOfImages(self):
        numberOfImages = len(self.imageList)
        self.assertEqual(self.stack.getNumberOfImages(), numberOfImages)

    def testGetNumberOfImagesAddedImage(self):
        numberOfImages = len(self.imageList)
        imageNotAlreadyIn = DCCImages.DCCImage(np.zeros((1250, 1251), dtype=np.float32))
        self.stack.addDCCImage(imageNotAlreadyIn)
        self.assertEqual(self.stack.getNumberOfImages(), numberOfImages + 1)

    def testGetNumberOfImagesRemovedImage(self):
        numberOfImages = len(self.imageList)
        self.stack.removeAtIndex(0)
        self.assertEqual(self.stack.getNumberOfImages(), numberOfImages - 1)

    def testImageStackAsNumpyArray(self):
        imageArray = np.array(self.imageList)
        arrayFromStack = self.stack.asNumpyArray()
        self.assertTrue(np.array_equal(imageArray, arrayFromStack))

    def testImageStackAsList(self):
        listFromStack = self.stack.asList()
        self.assertTrue(listFromStack == self.imageList)

    def testClearStack(self):
        self.stack.clearAll()
        self.assertTrue(len(self.stack) == 0)


if __name__ == '__main__':
    unittest.main()
