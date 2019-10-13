import env
from dcclab import *
import unittest
from unittest.mock import Mock, patch
import numpy as np
from pathlib import Path


class TestCSVReader(env.DCCLabTestCase):

    def testConstructorWrongFileType(self):
        filename = Path(self.dataDir / "testCziFileTwoChannels.czi")
        with self.assertRaises(InvalidFileFormatException):
            CSVReader(filename)

    def testConstructorValid(self):
        filname = Path(self.dataDir / "testCSVReader.csv")
        try:
            CSVReader(filname)
        except:
            self.fail("No exception should be thrown.")

    def testTwoFilesWithDifferentSeparators(self):
        comaSep = Path(self.dataDir / "testCSVReader.csv")
        otherSep = Path(self.dataDir / "testCSVReaderOtherSep.csv")
        csvReader1 = CSVReader(comaSep)
        csvReader2 = CSVReader(otherSep, ";")
        self.assertTrue(csvReader1.dataframe.equals(csvReader2.dataframe))

    def testDataframeAsArrayNoDrop(self):
        comaSep = Path(self.dataDir / "testCSVReader.csv")
        csv = CSVReader(comaSep)
        arrayFromMethod = csv.dataframeAsArray(False)
        array = np.array([[1, 10.2, 12.3, 89], [2, 3652.3, 74.25, 568], [3, 452.2, 4125, 1], [4, 89.25, 687.1254, 0.23],
                          [5, 784.2, 71.2, 12], [6, 12.25, 123.456789, 89], [7, 412.2, 321, 56], [8, 36, 36, 36],
                          [9, 78, 78, 7414]])
        # Problem with float and ==
        self.assertTrue(np.allclose(array, arrayFromMethod))

    def testDataframeAsArrayDropFirstColumn(self):
        comaSep = Path(self.dataDir / "testCSVReader.csv")
        csv = CSVReader(comaSep)
        arrayFromMethod = csv.dataframeAsArray(True)
        array = np.array([[10.2, 12.3, 89], [3652.3, 74.25, 568], [452.2, 4125, 1], [89.25, 687.1254, 0.23],
                          [784.2, 71.2, 12], [12.25, 123.456789, 89], [412.2, 321, 56], [36, 36, 36],
                          [78, 78, 7414]])
        self.assertTrue(np.allclose(array, arrayFromMethod[0]))
        self.assertTrue(np.array_equal(arrayFromMethod[1], [1, 2, 3, 4, 5, 6, 7, 8, 9]))

    def testDataframeAsArraySameDataframe(self):
        comaSep = Path(self.dataDir / "testCSVReader.csv")
        otherSep = Path(self.dataDir / "testCSVReaderOtherSep.csv")
        csvReader1 = CSVReader(comaSep)
        csvReader2 = CSVReader(otherSep, ";")
        array1Drop = csvReader1.dataframeAsArray()
        array1NoDrop = csvReader1.dataframeAsArray(False)
        array2Drop = csvReader2.dataframeAsArray()
        array2NoDrop = csvReader2.dataframeAsArray(False)
        self.assertTrue(np.array_equal(array1Drop[1], array2Drop[1]))
        self.assertTrue(np.array_equal(array1Drop[0], array2Drop[0]))
        self.assertTrue(np.array_equal(array1NoDrop, array2NoDrop))

    def testDataFrameAsArrayInt(self):
        comaSep = Path(self.dataDir / "testCSVReader.csv")
        csvReader1 = CSVReader(comaSep)
        arrayInt = csvReader1.dataframeAsArray(False, int)
        array = np.array([[1, 10.2, 12.3, 89], [2, 3652.3, 74.25, 568], [3, 452.2, 4125, 1], [4, 89.25, 687.1254, 0.23],
                          [5, 784.2, 71.2, 12], [6, 12.25, 123.456789, 89], [7, 412.2, 321, 56], [8, 36, 36, 36],
                          [9, 78, 78, 7414]], dtype=int)
        self.assertTrue(np.array_equal(arrayInt, array))

    def testDataframeAsArrayTwoDifferentCastType(self):
        comaSep = Path(self.dataDir / "testCSVReader.csv")
        csvReader1 = CSVReader(comaSep)
        arrayInt = csvReader1.dataframeAsArray(False, int)
        arrayFloat = csvReader1.dataframeAsArray(False)
        self.assertFalse(np.array_equal(arrayInt, arrayFloat))

    def testDropColumns(self):
        comaSep = Path(self.dataDir / "testCSVReader.csv")
        comaSep2 = Path(self.dataDir / "testCSVReader.csv")
        csvReader1 = CSVReader(comaSep)
        dataframeNoTouch = CSVReader(comaSep2)
        csvReader1.dropColumns((1, 2))
        originalArray = dataframeNoTouch.dataframeAsArray(False)
        removedColumns = csvReader1.dataframeAsArray(False)
        self.assertFalse(np.array_equal(originalArray, removedColumns))


class TestCorrelationMatrix(env.DCCLabTestCase):

    def testConstructorInvalid(self):
        with self.assertRaises(TypeError):
            CorrelationMatrix("1234556776543wdfghytf")

    def testConstructorValid(self):
        array = np.array([[1, 2, 3, 4, 5, 6], [6, 5, 4, 3, 2, 1]])
        try:
            CorrelationMatrix(array)
        except:
            self.fail("No exception should be thrown.")

    def testCorrelationCompute(self):
        comaSep = Path(self.dataDir / "testCSVReader.csv")
        csvReader1 = CSVReader(comaSep)
        array, firstColumn = csvReader1.dataframeAsArray()
        corr = CorrelationMatrix(array)
        correlationMatrix = corr.computeCorrelationMatrix()
        self.assertIsInstance(correlationMatrix, np.ndarray)

    def testCorrelationComputeRowsAreParameters(self):
        array = np.array([[235, 236, 245.25], [23.25, 19.58, 47.36], [-12.25, -12, -13.0005]])
        corr = CorrelationMatrix(array)
        correlationMatrix = corr.computeCorrelationMatrix(True)
        print(correlationMatrix)
        self.assertIsInstance(correlationMatrix, np.ndarray)

    def testCorrelationMatrixValues(self):
        array = np.array([[10, 13, 1], [11, 14, 1], [10, 15, 0]])
        corr = CorrelationMatrix(array)
        correlationMatrix = corr.computeCorrelationMatrix()
        print(correlationMatrix)


if __name__ == '__main__':
    unittest.main()
