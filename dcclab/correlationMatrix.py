import numpy as np
import pandas as pd
from .DCCExceptions import *
import seaborn as sns


class CSVReader:

    def __init__(self, filename: str, separator: str = ","):
        self.dataframe: pd.DataFrame = None
        self.filename = filename
        try:
            self.dataframe = pd.read_csv(filename, sep=separator)
        except Exception as e:
            raise InvalidFileFormatException(
                "Problem occurred when reading '{}'. Please make sure it is a valid csv file. Exception message:\n{}".format(
                    filename, e))

    def dataframeAsArray(self, dataframeDropFirstColumn: bool = True, castValuesTo=float):
        df: pd.DataFrame = self.dataframe.copy()
        firstColumn = None
        if dataframeDropFirstColumn:
            firstColumn = np.array(df[df.columns[0]])
            df.drop(df.columns[0], axis=1, inplace=True)
        df = df.astype(castValuesTo)
        return (np.array(df), firstColumn) if dataframeDropFirstColumn else np.array(df)


class CorrelationMatrix:

    def __init__(self, array: np.ndarray):
        if not isinstance(array, np.ndarray):
            raise TypeError("Array parameter must be a numpy.ndarray instance.")
        self.array = array

    def computeCorrelationMatrix(self, rowsAreParameters: bool = False):
        return np.corrcoef(self.array, rowvar=rowsAreParameters)

    def displayCorrelationMatrix(self, cmap: str = None, annotations: bool = True, colorbar: bool = True):
        correlationMatrix = self.computeCorrelationMatrix()
        ax = sns.heatmap(correlationMatrix, vmin=-1, vmax=1, cmap=cmap, annot=annotations, cbar=colorbar)
        ax.plot()
