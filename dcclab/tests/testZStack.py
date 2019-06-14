from dcclab.imageCollection import ZStack, ImageCollection
import numpy as np
import unittest


class TestZStack(unittest.TestCase):

    def setUp(self):
        self.depth = 5
        self.grayStack = np.zeros((10, 10, self.depth))

    def testImageCollectionFrom3DArray(self):  # fixme: sorry for touching another class. Image & ImageCollection tests look deprecated
        collection = ImageCollection(self.grayStack)

        self.assertTrue(len(collection) == self.depth)
        self.assertTrue(collection[0].shape == (10, 10))

    def testZStackFrom3DArray(self):
        stack = ZStack(self.grayStack)
        self.assertTrue(len(stack) == self.depth)
        self.assertTrue(stack[0].shape == (10, 10))

    def testZStackShape(self):
        stack = ZStack(self.grayStack)
        self.assertTrue(stack.shape == (10, 10, 5))

    def testZStackAsArray(self):
        stack = ZStack(self.grayStack)
        stackArray = stack.asArray()
        self.assertIsInstance(stackArray, np.ndarray)
        self.assertTrue(stackArray.shape == (10, 10, 5))

    @unittest.skip("Collection from 4D arrays is Not Implemented")
    def testZStackFromRGBArray(self):
        RGBStack = np.zeros((40, 40, 10, 3))

    # Todo: test zStack/ImageCollection from image files
