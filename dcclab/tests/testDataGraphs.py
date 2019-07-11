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
