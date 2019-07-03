import env
from dcclab import *
import unittest

header = "path,channelNumber,average,stdDev,entropy,median,min,max,averageN,stdDevN,entropyN,medianN,minN,maxN"
computeMedian = False


class DataExtractionMCherry(env.dcclabTestCase):
    def setUp(self):
        with open(Path(self.dataDir / r"query_mcher.csv"), "r",
                  encoding="utf-8") as readQuery:
            self.lines = readQuery.readlines()

        self.writeResults = open(Path(self.dataDir / r"query_mcher_results.csv"),
                                 "w", encoding="utf-8")
        self.writeResults.writelines(header)

    def tearDown(self):
        self.writeResults.close()

    def testMCherryExtraction(self):
        numberOfFiles = len(self.lines)
        for i in range(numberOfFiles):
            path, channelNumber = self.lines[i].split(";")
            channelNumber = channelNumber.split(":")[1]
            pathChanged = os.path.join("../", path)
            try:
                image = Image(path=pathChanged)
                channel = image.channels[int(channelNumber)]
                average = channel.getAverageValueOfPixels()
                stdDev = channel.getStandardDeviation()
                entropy = channel.getShannonEntropy()
                median = channel.getMedian() if computeMedian else np.nan
                minimum, maximum = channel.getExtrema()
                normalizedChannel = channel.convertToNormalizedFloat()
                averageN = normalizedChannel.getAverageValueOfPixels()
                stdDevN = normalizedChannel.getStandardDeviation()
                entropyN = normalizedChannel.getShannonEntropy()
                medianN = normalizedChannel.getMedian() if computeMedian else np.nan
                minimumN, maximumN = normalizedChannel.getExtrema()
            except Exception as e:

                if isinstance(e, NotImplementedError):
                    average = "NotYetImplemented"
                elif isinstance(e, IndexError):
                    average = "IndexError"
                else:
                    average = "OtherError"
                print(average)
                stdDev = average
                entropy = average
                median = average
                minimum = average
                maximum = average
                averageN = average
                stdDevN = average
                entropyN = average
                medianN = average
                minimumN = average
                maximumN = average

            self.writeResults.writelines(
                "\n{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(path, channelNumber.strip(), average,
                                                                     stdDev, entropy, median, minimum, maximum,
                                                                     averageN,
                                                                     stdDevN, entropyN, medianN, minimumN, maximumN))
            print("{} / {} files read (mCherry)".format(i + 1, numberOfFiles))


class DataExtractionEGFP(env.dcclabTestCase):
    def setUp(self):
        with open(Path(self.dataDir / r"query_egfp.csv"), "r",
                  encoding="utf-8") as readQuery:
            self.lines = readQuery.readlines()

        self.writeResults = open(Path(self.dataDir / r"query_egfp_results.csv"),
                                 "w", encoding="utf-8")
        self.writeResults.writelines(header)

    def tearDown(self):
        self.writeResults.close()

    def testEGFPExtraction(self):
        numberOfFiles = len(self.lines)
        for i in range(numberOfFiles):
            path, channelNumber = self.lines[i].split(";")
            channelNumber = channelNumber.split(":")[1]
            pathChanged = os.path.join("../", path)
            try:
                image = Image(path=pathChanged)
                channel = image.channels[int(channelNumber)]
                average = channel.getAverageValueOfPixels()
                stdDev = channel.getStandardDeviation()
                entropy = channel.getShannonEntropy()
                median = channel.getMedian() if computeMedian else np.nan
                minimum, maximum = channel.getExtrema()
                normalizedChannel = channel.convertToNormalizedFloat()
                averageN = normalizedChannel.getAverageValueOfPixels()
                stdDevN = normalizedChannel.getStandardDeviation()
                entropyN = normalizedChannel.getShannonEntropy()
                medianN = normalizedChannel.getMedian() if computeMedian else np.nan
                minimumN, maximumN = normalizedChannel.getExtrema()
            except Exception as e:

                if isinstance(e, NotImplementedError):
                    average = "NotYetImplemented"
                elif isinstance(e, IndexError):
                    average = "IndexError"
                else:
                    average = "OtherError"
                print(average)
                stdDev = average
                entropy = average
                median = average
                minimum = average
                maximum = average
                averageN = average
                stdDevN = average
                entropyN = average
                medianN = average
                minimumN = average
                maximumN = average

            self.writeResults.writelines(
                "\n{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(path, channelNumber.strip(), average,
                                                                     stdDev, entropy, median, minimum, maximum,
                                                                     averageN,
                                                                     stdDevN, entropyN, medianN, minimumN, maximumN))
            print("{} / {} files read (EGFP)".format(i + 1, numberOfFiles))


class DataExtractionDAPI(env.dcclabTestCase):
    def setUp(self):
        with open(Path(self.dataDir / r"query_DAPI.csv"), "r",
                  encoding="utf-8") as readQuery:
            self.lines = readQuery.readlines()

        self.writeResults = open(Path(self.dataDir / r"query_DAPI_results.csv"),
                                 "w", encoding="utf-8")
        self.writeResults.writelines(header)

    def tearDown(self):
        self.writeResults.close()

    def testDAPIExtraction(self):
        numberOfFiles = len(self.lines)
        for i in range(numberOfFiles):
            path, channelNumber = self.lines[i].split(";")
            channelNumber = channelNumber.split(":")[1]
            pathChanged = os.path.join("../", path)
            try:
                image = Image(path=pathChanged)
                channel = image.channels[int(channelNumber)]
                average = channel.getAverageValueOfPixels()
                stdDev = channel.getStandardDeviation()
                entropy = channel.getShannonEntropy()
                median = channel.getMedian() if computeMedian else np.nan
                minimum, maximum = channel.getExtrema()
                normalizedChannel = channel.convertToNormalizedFloat()
                averageN = normalizedChannel.getAverageValueOfPixels()
                stdDevN = normalizedChannel.getStandardDeviation()
                entropyN = normalizedChannel.getShannonEntropy()
                medianN = normalizedChannel.getMedian() if computeMedian else np.nan
                minimumN, maximumN = normalizedChannel.getExtrema()

            except Exception as e:

                if isinstance(e, NotImplementedError):
                    average = "NotYetImplemented"
                elif isinstance(e, IndexError):
                    average = "IndexError"
                else:
                    average = "OtherError"
                print(average)
                stdDev = average
                entropy = average
                median = average
                minimum = average
                maximum = average
                averageN = average
                stdDevN = average
                entropyN = average
                medianN = average
                minimumN = average
                maximumN = average

            self.writeResults.writelines(
                "\n{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(path, channelNumber.strip(), average,
                                                                     stdDev, entropy, median, minimum, maximum,
                                                                     averageN,
                                                                     stdDevN, entropyN, medianN, minimumN, maximumN))
            print("{} / {} files read (DAPI)".format(i + 1, numberOfFiles))


if __name__ == '__main__':
    unittest.main()
