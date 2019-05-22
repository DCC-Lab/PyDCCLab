import unittest
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
        with self.assertRaises(AttributeError):
            DCCImages.DCCImage([image])

    def testInvalidConstructor11Elements(self):
        imageList = []
        for i in range(10):
            array = np.ones((1250, 1251), dtype=np.float32)
            array[i][i] = i
            image = DCCImages.DCCImage(array)
            imageList.append(image)
        imageList.append(np.ones((10, 10)))
        with self.assertRaises(AttributeError):
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

    def testImageNotInStack(self):
        imageNotInStack = DCCImages.DCCImage(np.zeros((1250, 1251), dtype=np.float32))
        index = self.stack.isImageInStack(imageNotInStack)
        self.assertEqual(index, 5)

    def testImageInStack(self):
        imageInStack = DCCImages.DCCImage(np.ones((1250, 1251), dtype=np.float32))
        index = self.stack.isImageInStack(imageInStack)
        self.assertEqual(index, 2)

    def testAddNotDCCImage(self):
        imageNotDCC = np.ones((1454, 3025), dtype=np.float32)
        with self.assertRaises()


if __name__ == '__main__':
    unittest.main()
