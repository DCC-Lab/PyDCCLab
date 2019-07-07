import env
from dcclab import *
from unittest.mock import Mock, patch
import numpy as np
import unittest


class TestZStackFrom4DArray(env.DCCLabTestCase):

    def setUp(self):
        self.depth = 5
        self.grayStack = np.zeros((10, 10, 1, self.depth))
        self.grayStack[1:9, 1:9, 0, :] = 0.5
        self.grayStack[3:7, 3:7, 0,  1:self.depth-1] = 1
        self.zStack = ZStack(imagesArray=self.grayStack)

    def testImageCollectionFrom4DArray(self):
        collection = ImageCollection(imagesArray=self.grayStack)

        self.assertTrue(len(collection) == self.depth)
        self.assertTrue(collection[0].shape == (10, 10, 1))

    def testZStackFrom4DArray(self):
        self.assertTrue(len(self.zStack) == self.depth)
        self.assertTrue(self.zStack[0].shape == (10, 10, 1))

    def testImagesAreSimilar(self):
        pass

    def testNumberOfChannels(self):
        pass

    def testShape(self):
        self.assertTrue(self.zStack.shape == (10, 10, 1, 5))

    def testLength(self):
        self.assertTrue(len(self.zStack) == 5)

    def testAsArray(self):
        stackArray = self.zStack.asArray()

        self.assertIsInstance(stackArray, np.ndarray)
        self.assertTrue(stackArray.shape == (10, 10, 1, 5))

    def testAsChannelArray(self):
        stackArray = self.zStack.asChannelArray(channel=0)

        self.assertIsInstance(stackArray, np.ndarray)
        self.assertTrue(stackArray.shape == (10, 10, 5))

    def testAsOriginalArrayNotModified(self):
        originalStack = self.zStack.asOriginalArray()

        self.assertTrue(np.array_equal(originalStack, self.grayStack))

    def testApply3DFilter(self):
        self.zStack.apply3DFilter(ndimage.grey_opening, size=4)

        self.assertFalse(np.array_equal(self.zStack.asArray(), self.grayStack))

    def testApply3DFilterProcessIn2D(self):
        # assert it calls super method
        pass

    def testAsOriginalArray(self):
        self.zStack.apply3DFilter(ndimage.grey_opening, size=4)
        originalArray = self.zStack.asOriginalArray()

        self.assertIsInstance(originalArray, np.ndarray)
        self.assertTrue(np.array_equal(originalArray, self.grayStack))
        self.assertTrue(originalArray.shape == (10, 10, 1, 5))

    def testAsOriginalChannelArray(self):
        self.zStack.apply3DFilter(ndimage.grey_opening, size=4)
        originalArray = self.zStack.asOriginalChannelArray(channel=0)

        self.assertIsInstance(originalArray, np.ndarray)
        self.assertTrue(np.array_equal(originalArray, self.grayStack[:, :, 0, :]))
        self.assertTrue(originalArray.shape == (10, 10, 5))

    def testApplyOpening(self):
        self.zStack.applyOpening(size=4)

        self.assertFalse(np.array_equal(self.zStack.asArray(), self.grayStack))

    def testApplyClosing(self):
        self.zStack.applyClosing(size=4)

        self.assertFalse(np.array_equal(self.zStack.asArray(), self.grayStack))

    def testApplyErosion(self):
        self.zStack.applyErosion(size=4)

        self.assertFalse(np.array_equal(self.zStack.asArray(), self.grayStack))

    def testApplyDilation(self):
        self.zStack.applyDilation(size=4)

        self.assertFalse(np.array_equal(self.zStack.asArray(), self.grayStack))

    def testApplyNoiseFilter(self):
        pass

    def testApplyNoiseFilterWithErosionDilation(self):
        pass

    def testSetMaskFromThreshold(self):
        self.zStack.setMaskFromThreshold(self.grayStack.mean())

    def testGetChannelMaskArrayNotDefined(self):
        pass

    def testGetChannelMaskArray(self):
        pass

    def testApplyOpeningToMask(self):
        pass

    def testApplyClosingToMask(self):
        pass

    def testLabelMaskComponentsWithoutMask(self):
        pass

    def testLabelMaskComponents(self):
        # self.zStack.setMask(maskClosing=1)
        # self.zStack.setLabel()
        # onesRegion = np.ones((6, 6, self.depth-2))
        #
        # self.assertEqual(self.zStack.labeledZStack.dtype, np.dtype('int'))
        # self.assertTrue(np.array_equal(self.zStack.labeledZStack[2:8, 2:8, 1:self.depth-1], onesRegion))
        pass

    def testComponentsPropertiesNotDefined(self):
        pass

    def testLabellingSetComponentsProperties(self):
        # self.zStack.setMask(maskClosing=1)
        # self.zStack.setLabel()
        #
        # self.assertTrue(self.zStack.params["nbOfObjects"] == 1)
        pass

    def testGetChannelLabelArrayNotDefined(self):
        pass

    def testGetChannelLabelArray(self):
        pass

    def testSetChannelLabelsFromArray(self):
        pass

    def testAnalyzeComponents(self):
        # self.assertTrue(len(params) == 7)
        # self.assertTrue(params["totalSize"] == 180)
        pass

    def testGetObjectsSize(self):
        pass

    def testGetObjectsMass(self):
        pass

    def testGetObjectsCenterOfMass(self):
        pass

    def testSaveComponentsProperties(self):
        # self.zStack.setMask(maskClosing=1)
        # self.zStack.setLabel()
        # self.zStack.parameterize()
        #
        # filepath = Path(self.tmpDir / "testParams.json")
        # self.zStack.saveParamsToFile(filepath)
        # self.assertTrue(os.path.exists(filepath))
        pass

    def testSaveComponentsPropertiesToBadFileExtension(self):
        # self.zStack.setMask(maskClosing=1)
        # self.zStack.setLabel()
        # self.zStack.parameterize()
        #
        # filepath = Path(self.tmpDir / "testParams.txt")
        # self.zStack.saveParamsToFile(filepath)
        # self.assertTrue(os.path.exists(filepath + ".json"))
        pass

    def testCrop(self):
        pass

    def testCrop4DArray(self):
        # fixme: careful with crop logic: maybe move to image
        pass

    def testAsk2DCropIndices(self):
        pass

    @patch("matplotlib.pyplot.show", new=Mock())
    def testShow(self):
        pass

    def testChannelStacksInMemory(self):
        # self.zStack.setMask()
        # self.zStack.setLabel()
        #
        # self.assertTrue(len(self.zStack._stacksInMemory()) == 3)
        pass

    def testChannelStacksInMemoryOrdered(self):
        # self.zStack.removeNoise()
        # self.zStack.setMask()
        # self.zStack.setLabel()
        #
        # orderedKeys = ["Original ", "", "Mask ", "Label "]
        #
        # for key, orderedKey in zip(self.zStack._stacksInMemory().keys(), orderedKeys):
        #     self.assertEqual(key, orderedKey)
        pass

    @patch("matplotlib.pyplot.show", new=Mock())
    def testShowAllChannelStacks(self):
        pass

    @patch("matplotlib.pyplot.show", new=Mock())
    def testShowAllStacks(self):
        # assert NotImplementedError...
        pass


# Fixme: only tested Zstacks from Arrays : test zStack/ImageCollection from image files
# Todo: I can prepare a small stack sample folder.

@unittest.skip
class TestZStackFromImages(env.DCCLabTestCase):

    def testImagesAreSimilar(self):
        pass

    def testZStackFromImages(self):
        pass
