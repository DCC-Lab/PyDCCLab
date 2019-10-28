import numpy as np
import pandas as pd
from .DCCExceptions import *
import seaborn as sns
import matplotlib.pyplot as plt
import typing as tp
from datetime import datetime


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


class CorrelationMatrix:

    def __init__(self, dataframe: pd.DataFrame = None, array: np.ndarray = None,
                 headers: tp.Union[list, np.ndarray] = None):
        if dataframe is None and array in None:
            raise ValueError("A dataframe or an array is required to compute a correlation matrix.")
        if dataframe is not None and array is not None:
            raise ValueError(
                "A dataframe and an array were given. Please choose one of the two objects to compute the correlation matrix")
        if array is not None:
            self.dataframe = pd.DataFrame(array, columns=headers)
        else:
            self.dataframe = dataframe

    def computeCorrelationMatrix(self, castTo: type = float):
        corr = self.dataframe.astype(castTo).corr()
        return corr

    def showCorrelationMatrix(self, castTo: type = float):
        corr = self.computeCorrelationMatrix(castTo)
        ax = sns.heatmap(
            corr,
            vmin=-1, vmax=1, center=0,
            cmap=sns.diverging_palette(20, 220, n=200),
            square=True
        )
        ax.set_xticklabels(
            ax.get_xticklabels(),
            rotation=45,
            horizontalalignment='right'
        )
        plt.show()


class DataframeUtils:

    @staticmethod
    def ageOfMouse(dataframeRow, format: str = "%Y-%m-%d"):
        age = np.nan
        dateOfBirth = dataframeRow["DDN"]
        dateOfDeath = dataframeRow["date_mort"]
        print(dateOfBirth)
        if dateOfBirth is not None and dateOfDeath is not None:
            dateOfBirth = datetime.strptime(dateOfBirth, format)
            dateOfDeath = datetime.strptime(dateOfDeath, format)
            age = dateOfBirth - dateOfDeath
            age = age.days
        return age
