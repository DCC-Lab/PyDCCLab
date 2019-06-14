from dcclab.imageCollection import ZStack, ImageCollection
from unittest.mock import Mock, patch
import numpy as np
import unittest

# Fixme: only tested Zstacks with 3D Arrays : test zStack/ImageCollection from image files
# Todo: I can prepare a small stack sample folder.


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

    def testSetMaskCreatesCopy(self):
        self.zStack.setMask()

        self.assertIsInstance(self.zStack.maskedZStack, np.ndarray)

    def testSetMaskDontSetOriginal(self):
        self.zStack.setMask()

        self.assertIsNone(self.zStack.originalZStack)
        self.assertIsInstance(self.zStack.maskedZStack, np.ndarray)

    def testSetMask(self):  # fixme ?: not testing scipy methods individually
        self.zStack.setMask(maskClosing=1)
        trueRegion = np.ones((6, 6, self.depth-2)) == 1

        self.assertEqual(self.zStack.maskedZStack.dtype, np.dtype('bool'))
        self.assertTrue(np.array_equal(self.zStack.maskedZStack[2:8, 2:8, 1:self.depth-1], trueRegion))

    def testApplyMaskKeepOriginal(self):
        zStackBackup = self.zStack.array.copy()
        self.zStack.applyMask(maskClosing=1)

        self.assertTrue(np.array_equal(self.zStack.originalZStack, zStackBackup))

    def testSetLabel(self):
        self.zStack.setMask(maskClosing=1)
        self.zStack.setLabel()
        onesRegion = np.ones((6, 6, self.depth-2))

        self.assertEqual(self.zStack.labeledZStack.dtype, np.dtype('int'))
        self.assertTrue(np.array_equal(self.zStack.labeledZStack[2:8, 2:8, 1:self.depth-1], onesRegion))

    def testSetLabelWithoutMask(self):
        with self.assertRaises(Exception):
            self.zStack.setLabel()

    def testSetLabelDontSetOriginal(self):
        self.zStack.setMask()
        self.zStack.setLabel()

        self.assertIsNone(self.zStack.originalZStack)
        self.assertIsInstance(self.zStack.labeledZStack, np.ndarray)

    def testSetLabelWithAppliedMask(self):
        self.zStack.applyMask()
        self.zStack.setLabel()

        self.assertIsInstance(self.zStack.originalZStack, np.ndarray)
        self.assertIsInstance(self.zStack.labeledZStack, np.ndarray)

    def testApplyLabel(self):
        self.zStack.setMask()
        self.zStack.applyLabel()

        self.assertIsInstance(self.zStack.originalZStack, np.ndarray)
        self.assertIsNone(self.zStack.labeledZStack)

    def testNotReadyForParameterization(self):
        self.zStack.setMask()

        self.assertFalse(self.zStack._readyForParameterization())

    def testReadyForParameterization(self):
        self.zStack.setMask()
        self.zStack.setLabel()

        self.assertTrue(self.zStack._readyForParameterization())

    def testStacksInMemory(self):
        self.zStack.setMask()
        self.zStack.setLabel()

        self.assertTrue(len(self.zStack._stacksInMemory()) == 3)


    @unittest.skip
    def testParameterize(self):
        self.zStack.setMask(maskClosing=1)
        self.zStack.setLabel()
        self.zStack.parameterize()
        print(self.zStack.params)

    def testParamObjectsSize(self):
        pass

    def testParamTotalSize(self):
        pass

    def testParamObjectsMass(self):
        pass

    def testParamTotalMass(self):
        pass

    def testParamObjectsCenterOfMass(self):
        pass

    def testParamTotalCenterOfMass(self):
        pass

    def testSaveParamsToFile(self):
        pass

    def testStacksInMemory(self):
        pass

    @patch("matplotlib.pyplot.show", new=Mock)
    def testShow(self):
        pass

    @patch("matplotlib.pyplot.show", new=Mock)
    def testShowAllStacks(self):
        pass


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
