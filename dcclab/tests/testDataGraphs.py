import env
import pandas as pd
import numpy as np
import unittest
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns


class DataGraphs(env.DCCLabTestCase):

    def setUp(self) -> None:
        self.mCherry = pd.read_csv(Path(self.dataDir / "query_mcher_results.csv")).dropna(axis="columns")
        self.dapi = pd.read_csv(Path(self.dataDir / "query_DAPI_results.csv")).dropna(axis="columns")
        self.egfp = pd.read_csv(Path(self.dataDir / "query_egfp_results.csv")).dropna(axis="columns")
        self.mCherry = self.mCherry[
            (self.mCherry["average"] != "NotYetImplemented") & (self.mCherry["average"] != "IndexError")]
        self.dapi = self.dapi[
            (self.dapi["average"] != "NotYetImplemented") & (self.dapi["average"] != "IndexError")]
        self.egfp = self.egfp[
            (self.egfp["average"] != "NotYetImplemented") & (self.egfp["average"] != "IndexError")]

    def testDropNan(self):
        with self.assertRaises(Exception):
            self.dapi["median"]
        with self.assertRaises(Exception):
            self.dapi["medianN"]
        with self.assertRaises(Exception):
            self.egfp["median"]
        with self.assertRaises(Exception):
            self.egfp["medianN"]
        with self.assertRaises(Exception):
            self.mCherry["median"]
        with self.assertRaises(Exception):
            self.mCherry["medianN"]

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


if __name__ == '__main__':
    unittest.main()
