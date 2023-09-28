import env
from dcclab.image.imageCollection import *
from unittest.mock import Mock, patch
import unittest
import numpy as np
import re
import os


class TestImageMap(env.DCCLabTestCase):
    def setUp(self) -> None:
        self.filePathPattern = os.path.join(self.dataDir, "images", ".+X(\d+)-Y(\d+).+")
        super().setUp()

    def testInit(self):
        myMap = ImageCollection(pathPattern=self.filePathPattern)
        self.assertEqual(myMap.numberOfImages, 6)

    def testImages(self):
        myMap = ImageCollection(pathPattern=self.filePathPattern)
        img = myMap[0,0]
        self.assertTrue(isinstance(img, Image))

    def test1DCaptureGroups(self):
        self.filePathPattern = os.path.join(self.dataDir, "images", r".+X(\d+)-.+")
        myMap = ImageCollection(pathPattern=self.filePathPattern)
        self.assertEqual(myMap.numberOfImages, 3)
        self.assertEqual(myMap.dimension, 1)
        self.assertEqual(myMap.shape, (3,))

    def testInitNoCaptureGroups(self):
        self.filePathPattern = os.path.join(self.dataDir, "images", r".+X\d+-Y\d+.+")
        myMap = ImageCollection(pathPattern=self.filePathPattern)
        self.assertEqual(myMap.numberOfImages, 6)
        self.assertEqual(myMap.dimension, 1)
        self.assertEqual(myMap.shape, (6,))

    def testDimension(self):
        myMap = ImageCollection(pathPattern=self.filePathPattern)
        self.assertEqual(myMap.dimension, 2)

    def testShape(self):
        myMap = ImageCollection(pathPattern=self.filePathPattern)
        self.assertEqual(myMap.shape, (3, 2))

    def testReshape(self):
        myMap = ImageCollection(pathPattern=self.filePathPattern)
        self.assertEqual(myMap.shape, (3, 2))
        myMap.reshape((2, 3))
        self.assertEqual(myMap.shape, (2, 3))
        self.assertEqual(myMap.axes, [Axis.any, Axis.any])

    def testReshapeWithAxes(self):
        myMap = ImageCollection(pathPattern=self.filePathPattern)
        self.assertEqual(myMap.shape, (3, 2))
        myMap.reshape((2, 3), axes=[Axis.x, Axis.y])
        self.assertEqual(myMap.shape, (2, 3))
        self.assertEqual(myMap.axes, [Axis.x, Axis.y])

    def testIncorrectReshape(self):
        myMap = ImageCollection(pathPattern=self.filePathPattern)
        with self.assertRaises(ValueError):
            myMap.reshape((2, 2))

    def testSetAxes(self):
        myMap = ImageCollection(pathPattern=self.filePathPattern)
        myMap.axes = [Axis.x, Axis.y]
        self.assertEqual(myMap.axes, [Axis.x, Axis.y])

    def testAxes(self):
        myMap = ImageCollection(pathPattern=self.filePathPattern)
        self.assertEqual(myMap.axes, [Axis.x, Axis.y])

    def testGetItem(self):
        myMap = ImageCollection(pathPattern=self.filePathPattern)
        self.assertIsNotNone(myMap[(0, 0)])

    def testGetItemNoExplicitTuple(self):
        myMap = ImageCollection(pathPattern=self.filePathPattern)
        self.assertIsNotNone(myMap[0, 0])
        self.assertEqual(myMap[0, 0], myMap[(0, 0)])

    def testLoopThroughItems(self):
        myMap = ImageCollection(pathPattern=self.filePathPattern)
        maxX, maxY = myMap.shape

        for i in range(maxX):
            for j in range(maxY):
                self.assertIsNotNone(myMap[(i, j)])

    def testIterThroughItems(self):
        myMap = ImageCollection(pathPattern=self.filePathPattern)
        for image in myMap:
            self.assertIsNotNone(image)

    def testUnravel(self):
        with self.assertRaises(Exception):
            np.unravel_index(5, (2, 2))

    def testRavel(self):
        i = np.ravel_multi_index((1, 1), (2, 2))
        self.assertEqual(i, 3)

    def testShow(self):
        myMap = ImageCollection(pathPattern=self.filePathPattern)
        myMap.showAllSequentially()

    def testImageSizeInBytes(self):
        myMap = ImageCollection(pathPattern=self.filePathPattern)
        totalBytes = myMap.sizeInBytes
        sizes = np.sum(list(map(lambda img: img.sizeInBytes, myMap.images)))
        self.assertEqual(totalBytes, sizes)

    def testChannels(self):
        myMap = ImageCollection(pathPattern=self.filePathPattern)
        img = myMap[0,0]
        self.assertEqual(len(img.channels), 1)

    def testGaussianFilter(self):
        myMap = ImageCollection(pathPattern=self.filePathPattern)
        myMap.applyGaussianFilter(sigma=20)
        myMap.showAllOnGrid()

    def testCollectionAsArray(self):
        myMap = ImageCollection(pathPattern=self.filePathPattern)
        numpyArray = myMap.asArray()
        self.assertEqual(numpyArray.shape, (1024, 512,1, 6))
        numpyChannelArray = myMap[0,0].asArray()
        self.assertEqual(numpyChannelArray.shape, (1024, 512, 1))

    def testKeepOriginal(self):
        myMap = ImageCollection(pathPattern=self.filePathPattern)
        myMap.applyGaussianFilter(sigma=20)
        self.assertTrue(myMap.hasOriginal)

    def testRestoreOriginal(self):
        myMap = ImageCollection(pathPattern=self.filePathPattern)
        myMap.applyGaussianFilter(sigma=20)
        myMap.showAllSequentially()
        self.assertTrue(myMap.hasOriginal)
        myMap.restoreOriginal()
        self.assertFalse(myMap.hasOriginal)
        myMap.showAllSequentially()

    def testKeepSingleChannel(self):
        myMap = ImageCollection(pathPattern=self.filePathPattern)
        myMap.keepChannel(0)
        myMap.applyGaussianFilter(sigma=20)

if __name__ == "__main__":
    unittest.main()
