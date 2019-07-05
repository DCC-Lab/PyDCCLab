import env
from dcclab import *
import unittest

header = "path,channelNumber,averageN,stdDevN,entropyN,medianN"
computeMedian = True


class DataExtractionMCherry(env.DCCLabTestCase):
    def setUp(self):
        mode = "a"
        self.start = 0
        if self.start == 0:
            mode = "w"
        with open(Path(self.dataDir / r"query_mcher.csv"), "r",
                  encoding="utf-8") as readQuery:
            self.lines = readQuery.readlines()

        self.writeResults = open(Path(self.dataDir / r"query_mcher_resultsN.csv"),
                                 mode, encoding="utf-8")
        self.writeResults.writelines(header)

    def tearDown(self):
        self.writeResults.close()

    def testMCherryExtraction(self):
        numberOfFiles = len(self.lines)
        for i in range(self.start, numberOfFiles):
            path, channelNumber = self.lines[i].split(";")
            channelNumber = channelNumber.split(":")[1]
            pathChanged = os.path.join("../", path)
            try:
                image = Image(path=pathChanged)
                channel = image.channels[int(channelNumber)]
                normalizedChannel = channel.convertToNormalizedFloatMinToZeroMaxToOne()
                del channel
                averageN = normalizedChannel.getAverageValueOfPixels()
                stdDevN = normalizedChannel.getStandardDeviation()
                entropyN = normalizedChannel.getShannonEntropy()
                medianN = normalizedChannel.getMedian() if computeMedian else np.nan
            except Exception as e:

                if isinstance(e, NotImplementedError):
                    average = "NotYetImplemented"
                elif isinstance(e, IndexError):
                    average = "IndexError"
                else:
                    average = "OtherError"
                print(average)
                averageN = average
                stdDevN = average
                entropyN = average
                medianN = average

            self.writeResults.writelines(
                "\n{},{},{},{},{},{}".format(path, channelNumber.strip(), averageN, stdDevN,
                                             entropyN, medianN))
            print("{} / {} files read (mCherry)".format(i + 1, numberOfFiles))


class DataExtractionEGFP(env.DCCLabTestCase):
    def setUp(self):
        mode = "a"
        self.start = 0
        if self.start == 0:
            mode = "w"
        with open(Path(self.dataDir / r"query_egfp.csv"), "r",
                  encoding="utf-8") as readQuery:
            self.lines = readQuery.readlines()

        self.writeResults = open(Path(self.dataDir / r"query_egfp_resultsN.csv"),
                                 mode, encoding="utf-8")
        self.writeResults.writelines(header)

    def tearDown(self):
        self.writeResults.close()

    def testEGFPExtraction(self):
        numberOfFiles = len(self.lines)
        for i in range(self.start, numberOfFiles):
            path, channelNumber = self.lines[i].split(";")
            channelNumber = channelNumber.split(":")[1]
            pathChanged = os.path.join("../", path)
            try:
                image = Image(path=pathChanged)
                channel = image.channels[int(channelNumber)]
                normalizedChannel = channel.convertToNormalizedFloatMinToZeroMaxToOne()
                del channel
                averageN = normalizedChannel.getAverageValueOfPixels()
                stdDevN = normalizedChannel.getStandardDeviation()
                entropyN = normalizedChannel.getShannonEntropy()
                medianN = normalizedChannel.getMedian() if computeMedian else np.nan
            except Exception as e:

                if isinstance(e, NotImplementedError):
                    average = "NotYetImplemented"
                elif isinstance(e, IndexError):
                    average = "IndexError"
                else:
                    average = "OtherError"
                print(average)
                averageN = average
                stdDevN = average
                entropyN = average
                medianN = average

            self.writeResults.writelines(
                "\n{},{},{},{},{},{}".format(path, channelNumber.strip(), averageN, stdDevN,
                                             entropyN, medianN))
            print("{} / {} files read (EGFP)".format(i + 1, numberOfFiles))


class DataExtractionDAPI(env.DCCLabTestCase):
    def setUp(self):
        mode = "a"
        self.start = 0
        if self.start == 0:
            mode = "w"
        with open(Path(self.dataDir / r"query_DAPI.csv"), "r",
                  encoding="utf-8") as readQuery:
            self.lines = readQuery.readlines()

        self.writeResults = open(Path(self.dataDir / r"query_DAPI_resultsN.csv"),
                                 mode, encoding="utf-8")
        self.writeResults.writelines(header)

    def tearDown(self):
        self.writeResults.close()

    def testDAPIExtraction(self):
        numberOfFiles = len(self.lines)
        for i in range(self.start, numberOfFiles):
            path, channelNumber = self.lines[i].split(";")
            channelNumber = channelNumber.split(":")[1]
            pathChanged = os.path.join("../", path)
            try:
                image = Image(path=pathChanged)
                channel = image.channels[int(channelNumber)]
                normalizedChannel = channel.convertToNormalizedFloatMinToZeroMaxToOne()
                del channel
                averageN = normalizedChannel.getAverageValueOfPixels()
                stdDevN = normalizedChannel.getStandardDeviation()
                entropyN = normalizedChannel.getShannonEntropy()
                medianN = normalizedChannel.getMedian() if computeMedian else np.nan

            except Exception as e:

                if isinstance(e, NotImplementedError):
                    average = "NotYetImplemented"
                elif isinstance(e, IndexError):
                    average = "IndexError"
                else:
                    average = "OtherError"
                print(average)
                averageN = average
                stdDevN = average
                entropyN = average
                medianN = average

            self.writeResults.writelines(
                "\n{},{},{},{},{},{}".format(path, channelNumber.strip(), averageN, stdDevN,
                                             entropyN, medianN))
            print("{} / {} files read (DAPI)".format(i + 1, numberOfFiles))


if __name__ == '__main__':
    unittest.main()
