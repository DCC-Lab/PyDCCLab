import dcclab
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

path = r"C:\Users\goubi\Desktop\results"

csvReaderMCherry = dcclab.CSVReader(path + r"\queryMCherAll.csv", separator=",")
csvReaderDAPI = dcclab.CSVReader(path + r"\queryDAPIAll.csv", separator=",")
csvReaderEGFP = dcclab.CSVReader(path + r"\queryEGFPAll.csv", separator=",")
csvs = [csvReaderMCherry, csvReaderDAPI, csvReaderEGFP]
channels = ["mCherry", "DAPI", "EGFP"]
for csv, channel in zip(csvs, channels):
    dataframe = csv.dataframe.astype(str)
    dataframe = dcclab.DataframeUtils.dropRowsWithCertainValues(dataframe, "NotYetImplemented", "medianN")
    dataframe = dcclab.DataframeUtils.dropRowsWithCertainValues(dataframe, "IndexError", "medianN")
    dataframe.replace("None", np.nan, inplace=True)
    dataframe["age"] = dataframe.apply(lambda row: dcclab.DataframeUtils.ageOfMouse(row), axis=1)
    dataframe["DeathUseDelay"] = dataframe.apply(lambda row: dcclab.DataframeUtils.nbDaysBetweenDeathAndUse(row),
                                                 axis=1)
    dataframe["injectionVolume"] = dataframe.apply(lambda row: dcclab.DataframeUtils.injectionVolume(row), axis=1)
    dataframe.drop(["path", "DDN", "date_mort", "date_utilisation", "beam_splitter", "volume_injection"], axis=1,
                   inplace=True)
    # corr = dcclab.CorrelationMatrix(dataframe=dataframe)
    # corr2 = corr.computeCorrelationMatrix()
    # corr.showCorrelationMatrix(title='Correlation Matrix ({})'.format(channel))
    # print(dcclab.DataframeUtils.usedValuesStatsPerColumn(dataframe.astype(float)))
    perm = dcclab.PermutationCorrelations(dataframe, numberOfPermutations=100000)
    perm.computeCorrelationTensor()
    pvalues = perm.computePValue()
    print(pvalues)
    valid = perm.arePValuesValid(pvalues, 1 / 100)
    print(f"Valide à a = 0.01: {valid}")
    valid = perm.arePValuesValid(pvalues, 1 / 1000)
    print(f"Valide à a = 0.001: {valid}")
    perm.displayPValues(1 / 1000,
                        title=f"p-values valides selon le seuil  = {1 / 1000} et matrice de corrélation originale ({channel})")
