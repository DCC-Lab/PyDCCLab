import env
import pandas as pd
import numpy as np
import unittest
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns


class DataGraphs(env.DCCLabTestCase):

    def setUp(self) -> None:
        self.mCherry = pd.read_csv(Path(self.dataDir / "query_mcher_results.csv"), sep=";").dropna(axis="columns")
        self.dapi = pd.read_csv(Path(self.dataDir / "query_DAPI_results.csv"), sep=";").dropna(axis="columns")
        self.egfp = pd.read_csv(Path(self.dataDir / "query_egfp_results.csv"), sep=";").dropna(axis="columns")
        self.mCherry = self.mCherry[
            (self.mCherry["average"] != "NotYetImplemented") & (self.mCherry["average"] != "IndexError")]
        self.dapi = self.dapi[
            (self.dapi["average"] != "NotYetImplemented") & (self.dapi["average"] != "IndexError")]
        self.egfp = self.egfp[
            (self.egfp["average"] != "NotYetImplemented") & (self.egfp["average"] != "IndexError")]

    def testAllChannelsAvgVsStdDev(self):
        avgMC = np.array(self.mCherry["average"], float)
        stdDevMC = np.array(self.mCherry["stdDev"], float)
        avgDAPI = np.array(self.dapi["average"], float)
        stdDevDAPI = np.array(self.dapi["stdDev"], float)
        avgEGFP = np.array(self.egfp["average"], float)
        stdDevEGFP = np.array(self.egfp["stdDev"], float)
        allAvg = np.concatenate((avgMC, avgDAPI, avgEGFP))
        allStdDev = np.concatenate((stdDevMC, stdDevDAPI, stdDevEGFP))
        jp = sns.jointplot(allAvg, allStdDev, kind="reg", scatter=False, fit_reg=False)
        jp.ax_joint.plot(avgMC, stdDevMC, "o", color="red", alpha=0.2, label="mCherry")
        jp.ax_joint.plot(avgDAPI, stdDevDAPI, "x", color="blue", alpha=0.2, label="DAPI")
        jp.ax_joint.plot(avgEGFP, stdDevEGFP, "v", color="green", alpha=0.2, label="EGFP")
        plt.ylabel("Standard Deviation")
        plt.xlabel("Average")
        plt.title("Average and standard deviation of images from the POM platform (non normalized images)")
        plt.legend()
        plt.show()

    def testAllChannelsAvgVsEntropy(self):
        avgMC = np.array(self.mCherry["average"], float)
        entroDevMC = np.array(self.mCherry["entropy"], float)
        avgDAPI = np.array(self.dapi["average"], float)
        entroDAPI = np.array(self.dapi["entropy"], float)
        avgEGFP = np.array(self.egfp["average"], float)
        entroEGFP = np.array(self.egfp["entropy"], float)
        allAvg = np.concatenate((avgMC, avgDAPI, avgEGFP))
        allEntro = np.concatenate((entroDevMC, entroDAPI, entroEGFP))
        jp = sns.jointplot(allAvg, allEntro, kind="reg", scatter=False, fit_reg=False)
        jp.ax_joint.plot(avgMC, entroDevMC, "o", color="red", alpha=0.2, label="mCherry")
        jp.ax_joint.plot(avgDAPI, entroDAPI, "x", color="blue", alpha=0.2, label="DAPI")
        jp.ax_joint.plot(avgEGFP, entroEGFP, "v", color="green", alpha=0.2, label="EGFP")
        plt.ylabel("Entropy")
        plt.xlabel("Average")
        plt.title("Average and entropy of images from the POM platform (non normalized images)")
        plt.legend()
        plt.show()

    def testAllChannelsStdDevVsEntropy(self):
        stdDevMC = np.array(self.mCherry["stdDev"], float)
        entroDevMC = np.array(self.mCherry["entropy"], float)
        stdDevDAPI = np.array(self.dapi["stdDev"], float)
        entroDAPI = np.array(self.dapi["entropy"], float)
        stdDevEGFP = np.array(self.egfp["stdDev"], float)
        entroEGFP = np.array(self.egfp["entropy"], float)
        allStdDev = np.concatenate((stdDevMC, stdDevDAPI, stdDevEGFP))
        allEntro = np.concatenate((entroDevMC, entroDAPI, entroEGFP))
        jp = sns.jointplot(allStdDev, allEntro, kind="reg", scatter=False, fit_reg=False)
        jp.ax_joint.plot(stdDevMC, entroDevMC, "o", color="red", alpha=0.2, label="mCherry")
        jp.ax_joint.plot(stdDevDAPI, entroDAPI, "x", color="blue", alpha=0.2, label="DAPI")
        jp.ax_joint.plot(stdDevEGFP, entroEGFP, "v", color="green", alpha=0.2, label="EGFP")
        plt.ylabel("Entropy")
        plt.xlabel("Standard deviation")
        plt.title("Standard deviation and entropy of images from the POM platform (non normalized images)")
        plt.legend()
        plt.show()

    def testAllChannelsAvgVsStdDevN(self):
        avgMC = np.array(self.mCherry["averageN"], float)
        stdDevMC = np.array(self.mCherry["stdDevN"], float)
        avgDAPI = np.array(self.dapi["averageN"], float)
        stdDevDAPI = np.array(self.dapi["stdDevN"], float)
        avgEGFP = np.array(self.egfp["averageN"], float)
        stdDevEGFP = np.array(self.egfp["stdDevN"], float)
        allAvg = np.concatenate((avgMC, avgDAPI, avgEGFP))
        allStdDev = np.concatenate((stdDevMC, stdDevDAPI, stdDevEGFP))
        jp = sns.jointplot(allAvg, allStdDev, kind="reg", scatter=False, fit_reg=False)
        jp.ax_joint.plot(avgMC, stdDevMC, "o", color="red", alpha=0.2, label="mCherry")
        jp.ax_joint.plot(avgDAPI, stdDevDAPI, "x", color="blue", alpha=0.2, label="DAPI")
        jp.ax_joint.plot(avgEGFP, stdDevEGFP, "v", color="green", alpha=0.2, label="EGFP")
        plt.ylabel("Standard Deviation")
        plt.xlabel("Average")
        plt.title("Average and standard deviation of images from the POM platform (normalized images)")
        plt.legend()
        plt.show()

    def testAllChannelsAvgVsEntropyN(self):
        avgMC = np.array(self.mCherry["averageN"], float)
        entroDevMC = np.array(self.mCherry["entropyN"], float)
        avgDAPI = np.array(self.dapi["averageN"], float)
        entroDAPI = np.array(self.dapi["entropyN"], float)
        avgEGFP = np.array(self.egfp["averageN"], float)
        entroEGFP = np.array(self.egfp["entropyN"], float)
        allAvg = np.concatenate((avgMC, avgDAPI, avgEGFP))
        allEntro = np.concatenate((entroDevMC, entroDAPI, entroEGFP))
        jp = sns.jointplot(allAvg, allEntro, kind="reg", scatter=False, fit_reg=False)
        jp.ax_joint.plot(avgMC, entroDevMC, "o", color="red", alpha=0.2, label="mCherry")
        jp.ax_joint.plot(avgDAPI, entroDAPI, "x", color="blue", alpha=0.2, label="DAPI")
        jp.ax_joint.plot(avgEGFP, entroEGFP, "v", color="green", alpha=0.2, label="EGFP")
        plt.ylabel("Entropy")
        plt.xlabel("Average")
        plt.title("Average and entropy of images from the POM platform (normalized images)")
        plt.legend()
        plt.show()

    def testAllChannelsStdDevVsEntropyN(self):
        stdDevMC = np.array(self.mCherry["stdDevN"], float)
        entroDevMC = np.array(self.mCherry["entropyN"], float)
        stdDevDAPI = np.array(self.dapi["stdDevN"], float)
        entroDAPI = np.array(self.dapi["entropyN"], float)
        stdDevEGFP = np.array(self.egfp["stdDevN"], float)
        entroEGFP = np.array(self.egfp["entropyN"], float)
        allStdDev = np.concatenate((stdDevMC, stdDevDAPI, stdDevEGFP))
        allEntro = np.concatenate((entroDevMC, entroDAPI, entroEGFP))
        jp = sns.jointplot(allStdDev, allEntro, kind="reg", scatter=False, fit_reg=False)
        jp.ax_joint.plot(stdDevMC, entroDevMC, "o", color="red", alpha=0.2, label="mCherry")
        jp.ax_joint.plot(stdDevDAPI, entroDAPI, "x", color="blue", alpha=0.2, label="DAPI")
        jp.ax_joint.plot(stdDevEGFP, entroEGFP, "v", color="green", alpha=0.2, label="EGFP")
        plt.ylabel("Entropy")
        plt.xlabel("Standard deviation")
        plt.title("Standard deviation and entropy of images from the POM platform (normalized images)")
        plt.legend()
        plt.show()

    def testAllChannelsStdDevVsMedianN(self):
        stdDevMC = np.array(self.mCherry["stdDevN"], float)
        medianMC = np.array(self.mCherry["medianN"], float)
        stdDevDAPI = np.array(self.dapi["stdDevN"], float)
        medianDAPI = np.array(self.dapi["medianN"], float)
        stdDevEGFP = np.array(self.egfp["stdDevN"], float)
        medianEGFP = np.array(self.egfp["medianN"], float)
        allStdDev = np.concatenate((stdDevMC, stdDevDAPI, stdDevEGFP))
        allMedian = np.concatenate((medianMC, medianDAPI, medianEGFP))
        jp = sns.jointplot(allStdDev, allMedian, kind="reg", scatter=False, fit_reg=False)
        jp.ax_joint.plot(stdDevMC, medianMC, "o", color="red", alpha=0.2, label="mCherry")
        jp.ax_joint.plot(stdDevDAPI, medianDAPI, "x", color="blue", alpha=0.2, label="DAPI")
        jp.ax_joint.plot(stdDevEGFP, medianEGFP, "v", color="green", alpha=0.2, label="EGFP")
        plt.ylabel("Median")
        plt.xlabel("Standard deviation")
        plt.title("Standard deviation and median of images from the POM platform (normalized images)")
        plt.legend()
        plt.show()

    def testAllChannelsAverageVsMedianN(self):
        averageMC = np.array(self.mCherry["averageN"], float)
        medianMC = np.array(self.mCherry["medianN"], float)
        averageDAPI = np.array(self.dapi["averageN"], float)
        medianDAPI = np.array(self.dapi["medianN"], float)
        averageEGFP = np.array(self.egfp["averageN"], float)
        medianEGFP = np.array(self.egfp["medianN"], float)
        allAverage = np.concatenate((averageMC, averageDAPI, averageEGFP))
        allMedian = np.concatenate((medianMC, medianDAPI, medianEGFP))
        jp = sns.jointplot(allAverage, allMedian, kind="reg", scatter=False, fit_reg=False)
        jp.ax_joint.plot(averageMC, medianMC, "o", color="red", alpha=0.2, label="mCherry")
        jp.ax_joint.plot(averageDAPI, medianDAPI, "x", color="blue", alpha=0.2, label="DAPI")
        jp.ax_joint.plot(averageEGFP, medianEGFP, "v", color="green", alpha=0.2, label="EGFP")
        plt.ylabel("Median")
        plt.xlabel("Average")
        plt.title("Average and median of images from the POM platform (normalized images)")
        plt.legend()
        plt.show()

    def testAllChannelsEntropyVsMedianN(self):
        entropyMC = np.array(self.mCherry["entropyN"], float)
        medianMC = np.array(self.mCherry["medianN"], float)
        entropyDAPI = np.array(self.dapi["entropyN"], float)
        medianDAPI = np.array(self.dapi["medianN"], float)
        entropyEGFP = np.array(self.egfp["entropyN"], float)
        medianEGFP = np.array(self.egfp["medianN"], float)
        allEntropy = np.concatenate((entropyMC, entropyDAPI, entropyEGFP))
        allMedian = np.concatenate((medianMC, medianDAPI, medianEGFP))
        jp = sns.jointplot(allEntropy, allMedian, kind="reg", scatter=False, fit_reg=False)
        jp.ax_joint.plot(entropyMC, medianMC, "o", color="red", alpha=0.2, label="mCherry")
        jp.ax_joint.plot(entropyDAPI, medianDAPI, "x", color="blue", alpha=0.2, label="DAPI")
        jp.ax_joint.plot(entropyEGFP, medianEGFP, "v", color="green", alpha=0.2, label="EGFP")
        plt.ylabel("Median")
        plt.xlabel("Entropy")
        plt.title("Entropy and median of images from the POM platform (normalized images)")
        plt.legend()
        plt.show()

    def testExtractDataSingleChannel(self):
        channels = [self.egfp, self.dapi, self.mCherry]
        dataNonNormalized = ["average", "stdDev", "entropy"]
        dataNormalized = ["averageN", "stdDevN", "entropyN", "medianN"]
        for channel in channels:
            if self.egfp.equals(channel):
                channelName = "EGFP"
                color = "green"
            elif self.mCherry.equals(channel):
                channelName = "mCherry"
                color = "red"
            else:
                channelName = "DAPI"
                color = "blue"
            for i in range(len(dataNonNormalized)):
                for j in range(i, len(dataNonNormalized)):
                    xLabel = dataNonNormalized[i]
                    yLabel = dataNonNormalized[j]
                    if j != i:
                        x = np.array(channel[xLabel], float)
                        y = np.array(channel[yLabel], float)
                        jp = sns.jointplot(x, y, kind="reg", scatter=False, fit_reg=False)
                        jp.ax_joint.plot(x, y, "o", color=color, alpha=0.2)
                        plt.ylabel(yLabel)
                        plt.xlabel(xLabel)
                        plt.title("{} and {} of {} from the POM platform (non normalized images)".format(xLabel, yLabel,
                                                                                                         channelName))
                        plt.show()
            for i in range(len(dataNormalized)):
                for j in range(i, len(dataNormalized)):
                    xLabel = dataNormalized[i]
                    yLabel = dataNormalized[j]
                    if j != i:
                        x = np.array(channel[xLabel], float)
                        y = np.array(channel[yLabel], float)
                        jp = sns.jointplot(x, y, kind="reg", scatter=False, fit_reg=False)
                        jp.ax_joint.plot(x, y, "o", color=color, alpha=0.2)
                        plt.ylabel(yLabel)
                        plt.xlabel(xLabel)
                        plt.title("{} and {} of {} from the POM platform (normalized images)".format(xLabel, yLabel,
                                                                                                     channelName))
                        plt.show()


if __name__ == '__main__':
    unittest.main()
