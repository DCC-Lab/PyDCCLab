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
        dataframe = csv.dataframe
        array = np.array([[1, 10.2, 12.3, 89], [2, 3652.3, 74.25, 568], [3, 452.2, 4125, 1], [4, 89.25, 687.1254, 0.23],
                          [5, 784.2, 71.2, 12], [6, 12.25, 123.456789, 89], [7, 412.2, 321, 56], [8, 36, 36, 36],
                          [9, 78, 78, 7414]])
        self.assertTrue(np.allclose(array, dataframe))

    def testDataframeAsArrayDropFirstColumn(self):
        comaSep = Path(self.dataDir / "testCSVReader.csv")
        csv = CSVReader(comaSep)
        dataframe = csv.dataframe
        array = np.array([[1, 10.2, 12.3, 89], [2, 3652.3, 74.25, 568], [3, 452.2, 4125, 1], [4, 89.25, 687.1254, 0.23],
                          [5, 784.2, 71.2, 12], [6, 12.25, 123.456789, 89], [7, 412.2, 321, 56], [8, 36, 36, 36],
                          [9, 78, 78, 7414]])
        self.assertTrue(np.allclose(dataframe, array))

    def testDataframeAsArraySameDataframe(self):
        comaSep = Path(self.dataDir / "testCSVReader.csv")
        otherSep = Path(self.dataDir / "testCSVReaderOtherSep.csv")
        csvReader1 = CSVReader(comaSep)
        csvReader2 = CSVReader(otherSep, ";")
        dataframe1 = csvReader1.dataframe
        dataframe2 = csvReader2.dataframe
        self.assertTrue(np.array_equal(dataframe1, dataframe2))

    def testDataFrameAsArrayInt(self):
        comaSep = Path(self.dataDir / "testCSVReader.csv")
        csvReader1 = CSVReader(comaSep)
        arrayInt = np.array(csvReader1.dataframe, dtype=int)
        array = np.array([[1, 10.2, 12.3, 89], [2, 3652.3, 74.25, 568], [3, 452.2, 4125, 1], [4, 89.25, 687.1254, 0.23],
                          [5, 784.2, 71.2, 12], [6, 12.25, 123.456789, 89], [7, 412.2, 321, 56], [8, 36, 36, 36],
                          [9, 78, 78, 7414]], dtype=int)
        self.assertTrue(np.array_equal(arrayInt, array))


class TestCorrelationMatrix(env.DCCLabTestCase):

    def testConstructorInvalid(self):
        with self.assertRaises(TypeError):
            CorrelationMatrix("1234556776543wdfghytf")

    def testConstructorInvalidAllNone(self):
        with self.assertRaises(ValueError):
            CorrelationMatrix()

    def testConstructorInvalidBothGiven(self):
        array = np.random.randint(0, 1253, (4, 10))
        dataframe = pd.DataFrame(array)
        with self.assertRaises(ValueError):
            CorrelationMatrix(dataframe, array)

    def testConstructorValidArray(self):
        array = np.array([[1, 2, 3, 4, 5, 6], [6, 5, 4, 3, 2, 1]])
        try:
            CorrelationMatrix(array=array)
        except:
            self.fail("No exception should be thrown.")

    def testConstructorValidDataframe(self):
        comaSep = Path(self.dataDir / "testCSVReader.csv")
        dataframe = CSVReader(comaSep).dataframe
        try:
            CorrelationMatrix(dataframe)
        except:
            self.fail("No exception should be thrown.")

    def testConstructorReturnsDataframeWithArrayGivenNoHeader(self):
        array = np.array([[1, 2, 3, 4, 5, 6], [6, 5, 4, 3, 2, 1]])
        cm = CorrelationMatrix(array=array)
        dataframe = cm.dataframe
        self.assertEqual("   0  1  2  3  4  5\n0  1  2  3  4  5  6\n1  6  5  4  3  2  1", str(dataframe))

    def testConstructorReturnsDataframeWithArrayGiven(self):
        array = np.array([[1, 2, 3, 4, 5, 6], [6, 5, 4, 3, 2, 1]])
        headers = ["A", "B", "C", "D", "E", "F"]
        cm = CorrelationMatrix(array=array, headers=headers)
        dataframe = cm.dataframe
        self.assertEqual("   A  B  C  D  E  F\n0  1  2  3  4  5  6\n1  6  5  4  3  2  1", str(dataframe))

    def testCorrelationCompute(self):
        comaSep = Path(self.dataDir / "testCSVReader.csv")
        csvReader1 = CSVReader(comaSep)
        dataframe = csvReader1.dataframe
        corr = CorrelationMatrix(dataframe)
        correlationMatrix = corr.computeCorrelationMatrix(columnsToDrop=[0])
        self.assertIsInstance(correlationMatrix, pd.DataFrame)

    def testCorrelationComputeWithDrop(self):
        array = np.array([[1, 2, 3, 4, 5, 6], [6, 5, 4, 3, 2, 1]])
        headers = ["A", "B", "C", "D", "E", "F"]
        cm = CorrelationMatrix(array=array, headers=headers)
        corrMatrixNoDrop = cm.computeCorrelationMatrix()
        corrMatrix = cm.computeCorrelationMatrix(columnsToDrop=["A", "B"])
        self.assertNotEqual(corrMatrix.shape, corrMatrixNoDrop.shape)

    def testCorrelationComputeWithDropIndices(self):
        array = np.array([[1, 2, 3, 4, 5, 6], [6, 5, 4, 3, 2, 1]])
        headers = ["A", "B", "C", "D", "E", "F"]
        cm = CorrelationMatrix(array=array, headers=headers)
        corrMatrixNoDrop = cm.computeCorrelationMatrix()
        corrMatrix = cm.computeCorrelationMatrix(columnsToDrop=[0, 1])
        self.assertNotEqual(corrMatrix.shape, corrMatrixNoDrop.shape)

    def testCorrelationComputeDropBothWays(self):
        array = np.array([[1, 2, 3, 4, 5, 6], [6, 5, 4, 3, 2, 1]])
        headers = ["A", "B", "C", "D", "E", "F"]
        cm = CorrelationMatrix(array=array, headers=headers)
        cm2 = CorrelationMatrix(array=array, headers=headers)
        correlationMatrixDropIndices = cm.computeCorrelationMatrix(columnsToDrop=[1, 2, 5])
        correlationMatrixDropNames = cm2.computeCorrelationMatrix(columnsToDrop=["B", "C", "F"])
        self.assertTrue(np.array_equal(correlationMatrixDropIndices, correlationMatrixDropNames))

    def testCorrelationComputeDropNotIntNorStrings(self):
        array = np.array([[1, 2, 3, 4, 5, 6], [6, 5, 4, 3, 2, 1]])
        headers = ["A", "B", "C", "D", "E", "F"]
        cm = CorrelationMatrix(array=array, headers=headers)
        cm2 = CorrelationMatrix(array=array, headers=headers)
        with self.assertRaises(ValueError):
            cm.computeCorrelationMatrix(columnsToDrop=[4j + 3, 23, "hello world"])
        with self.assertRaises(ValueError):
            cm2.computeCorrelationMatrix(columnsToDrop=["A", "B", 2])

    @patch("matplotlib.pyplot.show", new=Mock())
    def testCorrelationMatrixShow(self):
        array = np.array([[1, 2, 3, 4, 5, 6], [6, 5, 4, 3, 2, 1]])
        headers = ["A", "B", "C", "D", "E", "F"]
        cm = CorrelationMatrix(array=array, headers=headers)
        try:
            cm.showCorrelationMatrix()
        except:
            self.fail("Exception raised.")


class TestDataframeUtils(env.DCCLabTestCase):

    def testAgeOfMouseNotNegative(self):
        birthDate = "2018-05-09"
        deathDate = "2019-08-02"
        birthDate2 = "2018-05-10"
        deathDate2 = "2019-08-02"
        birthDate3 = "2018-05-11"
        deathDate3 = "2019-08-02"
        array = np.array([[birthDate, deathDate], [birthDate2, deathDate2], [birthDate3, deathDate3]], dtype=str)
        headers = ["DDN", "date_mort"]
        dataframe = pd.DataFrame(array, columns=headers)
        dataframe["age"] = dataframe.apply(lambda row: DataframeUtils.ageOfMouse(row), axis=1)
        newArray = [[birthDate, deathDate, 450], [birthDate2, deathDate2, 449], [birthDate3, deathDate3, 448]]
        newHeaders = ["DDN", "date_mort", "age"]
        finalDataframe = pd.DataFrame(newArray, columns=newHeaders)
        self.assertTrue(finalDataframe.equals(dataframe))

    def testAgeOfMouseNegative(self):
        deathDate = "2018-05-09"
        birthDate = "2019-08-02"
        deathDate2 = "2018-05-10"
        birthDate2 = "2019-08-02"
        deathDate3 = "2018-05-11"
        birthDate3 = "2019-08-02"
        array = np.array([[birthDate, deathDate], [birthDate2, deathDate2], [birthDate3, deathDate3]], dtype=str)
        headers = ["DDN", "date_mort"]
        dataframe = pd.DataFrame(array, columns=headers)
        dataframe["age"] = dataframe.apply(lambda row: DataframeUtils.ageOfMouse(row), axis=1)
        newArray = [[birthDate, deathDate, np.nan], [birthDate2, deathDate2, np.nan], [birthDate3, deathDate3, np.nan]]
        newHeaders = ["DDN", "date_mort", "age"]
        finalDataframe = pd.DataFrame(newArray, columns=newHeaders)
        self.assertTrue(finalDataframe.equals(dataframe))

    def testDeathUseDelayNotNegative(self):
        deathDate = "2018-05-09"
        useDate = "2019-08-02"
        deathDate2 = "2018-05-10"
        useDate2 = "2019-08-02"
        deathDate3 = "2018-05-11"
        useDate3 = "2019-08-02"
        array = np.array([[deathDate, useDate], [deathDate2, useDate2], [deathDate3, useDate3]], dtype=str)
        headers = ["date_mort", "date_utilisation"]
        dataframe = pd.DataFrame(array, columns=headers)
        dataframe["delay"] = dataframe.apply(lambda row: DataframeUtils.nbDaysBetweenDeathAndUse(row), axis=1)
        newArray = [[deathDate, useDate, 450], [deathDate2, useDate2, 449], [deathDate3, useDate3, 448]]
        newHeaders = ["date_mort", "date_utilisation", "delay"]
        finalDataframe = pd.DataFrame(newArray, columns=newHeaders)
        self.assertTrue(finalDataframe.equals(dataframe))

    def testDeathUseDelayNegative(self):
        useDate = "2018-05-09"
        deathDate = "2019-08-02"
        useDate2 = "2018-05-10"
        deathDate2 = "2019-08-02"
        useDate3 = "2018-05-11"
        deathDate3 = "2019-08-02"
        array = np.array([[deathDate, useDate], [deathDate2, useDate2], [deathDate3, useDate3]], dtype=str)
        headers = ["date_mort", "date_utilisation"]
        dataframe = pd.DataFrame(array, columns=headers)
        dataframe["delay"] = dataframe.apply(lambda row: DataframeUtils.nbDaysBetweenDeathAndUse(row), axis=1)
        newArray = [[deathDate, useDate, np.nan], [deathDate2, useDate2, np.nan], [deathDate3, useDate3, np.nan]]
        newHeaders = ["date_mort", "date_utilisation", "delay"]
        finalDataframe = pd.DataFrame(newArray, columns=newHeaders)
        self.assertTrue(finalDataframe.equals(dataframe))

    def testInjectionVolumeFloatInString(self):
        injectionVolume = "300"
        injectionVolume2 = " 300"
        injectionVolume3 = "   300.36"
        injectionVolume4 = "0.25"
        array = np.array([[injectionVolume], [injectionVolume2], [injectionVolume3], [injectionVolume4]])
        headers = ["volume_injection"]
        dataframe = pd.DataFrame(array, columns=headers)
        dataframe["injectionVolume"] = dataframe.apply(lambda row: DataframeUtils.injectionVolume(row), axis=1)
        newArray = [[injectionVolume, 300], [injectionVolume2, 300], [injectionVolume3, 300.36],
                    [injectionVolume4, 0.25]]
        headers = ["volume_injection", "injectionVolume"]
        finalDataframe = pd.DataFrame(newArray, columns=headers)
        self.assertTrue(finalDataframe.equals(dataframe))

    def testInjectionVolume2x200(self):
        injectionVolume = [["2 x 200 nl (G+D)"], ["2 x 200 nl (G+D)"]]
        headers = ["volume_injection"]
        dataframe = pd.DataFrame(injectionVolume, columns=headers)
        dataframe["injectionVolume"] = dataframe.apply(lambda row: DataframeUtils.injectionVolume(row), axis=1)
        newArray = [["2 x 200 nl (G+D)", 400], ["2 x 200 nl (G+D)", 400]]
        newHeaders = ["volume_injection", "injectionVolume"]
        finalDataframe = pd.DataFrame(newArray, columns=newHeaders)
        self.assertTrue(finalDataframe.equals(dataframe))

    def testInjectionVolumeNotValidValues(self):
        injectionVolume = [["2 x 20000 nl (G+D)"], ["2 x 20000 nl (G+D)"]]
        headers = ["volume_injection"]
        dataframe = pd.DataFrame(injectionVolume, columns=headers)
        dataframe["injectionVolume"] = dataframe.apply(lambda row: DataframeUtils.injectionVolume(row), axis=1)
        newArray = [["2 x 20000 nl (G+D)", np.nan], ["2 x 20000 nl (G+D)", np.nan]]
        newHeaders = ["volume_injection", "injectionVolume"]
        finalDataframe = pd.DataFrame(newArray, columns=newHeaders)
        self.assertTrue(finalDataframe.equals(dataframe))

    def testUtilMethodsDropRows(self):
        array = np.array([[0, 1, 2, 3], [1, 2, 3, 4], [2, 3, 4, -25]])
        headers = ["A", "B", "C", "D"]
        dataframe = pd.DataFrame(array, columns=headers)
        newDataframe = DataframeUtils.dropRowsWithCertainValues(dataframe, -25, "D")
        self.assertFalse(dataframe.equals(newDataframe))

    def testUtilUsageStats(self):
        array = np.array([[np.nan, 0, 1, 2], [1, np.nan, 1, 2]])
        headers = ["a", "b", "c", "d"]
        dataframe = pd.DataFrame(array, columns=headers)
        stats = DataframeUtils.usedValuesStatsPerColumn(dataframe)
        supposedDict = {"a": (1 / 2, 1, 2), "b": (1 / 2, 1, 2), "c": (1, 2, 2), "d": (1, 2, 2)}
        self.assertEqual(supposedDict, stats)


if __name__ == '__main__':
    unittest.main()
