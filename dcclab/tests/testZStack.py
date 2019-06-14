from dcclab.imageCollection import ZStack, ImageCollection
import numpy as np
import unittest

# Fixme: only tested Zstacks with 3D Arrays : test zStack/ImageCollection from image files


class TestZStackFrom3DArray(unittest.TestCase):

    def setUp(self):
        self.depth = 5
        self.grayStack = np.zeros((10, 10, self.depth))
        self.grayStack[1:9, 1:9, :] = 0.5
        self.grayStack[3:7, 3:7, 1:self.depth-1] = 1
        self.zStack = ZStack(self.grayStack)

    def testImageCollectionFrom3DArray(self):  # fixme: sorry for touching another class
        collection = ImageCollection(self.grayStack)

        self.assertTrue(len(collection) == self.depth)
        self.assertTrue(collection[0].shape == (10, 10))

    def testZStackFrom3DArray(self):
        self.assertTrue(len(self.zStack) == self.depth)
        self.assertTrue(self.zStack[0].shape == (10, 10))

    def testShape(self):
        self.assertTrue(self.zStack.shape == (10, 10, 5))

    def testLength(self):
        self.assertTrue(len(self.zStack) == 5)

    def testArray(self):
        stackArray = self.zStack.array
        self.assertIsInstance(stackArray, np.ndarray)
        self.assertTrue(stackArray.shape == (10, 10, 5))

    def testRemoveNoise(self):  # fixme ?: not testing scipy methods individually
        self.zStack.removeNoise()
        self.assertTrue(self.zStack.array.mean() != self.grayStack.mean())

    def testRemoveNoiseKeepOriginal(self):
        originalStack = self.zStack.array.copy()
        self.zStack.removeNoise()
        self.assertIsInstance(self.zStack.originalZStack, np.ndarray)
        self.assertTrue(np.array_equal(self.zStack.originalZStack, originalStack))

    def testRemoveNoiseDoNotKeepOriginal(self):
        zStack = ZStack(self.grayStack, keepOriginal=False)
        zStack.removeNoise()
        self.assertIsNone(zStack.originalZStack)


class TestZStackFrom4DArray(unittest.TestCase):

    @unittest.skip("Collection from 4D arrays is Not Implemented")
    def testZStackFromRGBArray(self):
        RGBStack = np.zeros((40, 40, 10, 3))


class TestZStackFromImages(unittest.TestCase):

    def testImagesAreSimilar(self):
        pass

    def testZStackFromImages(self):
        pass

    # test all attributes
