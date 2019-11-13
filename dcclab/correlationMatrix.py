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
        if dataframe is None and array is None:
            raise ValueError("A dataframe or an array is required to compute a correlation matrix.")
        if dataframe is not None and array is not None:
            raise ValueError(
                "A dataframe and an array were given. Please choose one of the two objects to compute the correlation matrix")
        if dataframe is not None and not isinstance(dataframe, pd.DataFrame):
            raise TypeError("Dataframe parameter must be a pandas.Dataframe instance.")
        if array is not None:
            self.dataframe = pd.DataFrame(array, columns=headers)
        else:
            self.dataframe = dataframe

    def computeCorrelationMatrix(self, castTo: type = float, columnsToDrop: list = None):
        if columnsToDrop is not None:
            if all(isinstance(x, int) for x in columnsToDrop):
                self.dataframe.drop(self.dataframe.columns[columnsToDrop], axis=1, inplace=True)
            elif all(isinstance(x, str) for x in columnsToDrop):
                self.dataframe.drop(columnsToDrop, axis=1, inplace=True)
            else:
                raise ValueError("The list of columns to drop must consist of integers only or strings only.")
        corr = self.dataframe.astype(castTo).corr()
        return corr

    def showCorrelationMatrix(self, castTo: type = float, annotation: bool = True, fontScale: float = 0.5,
                              title: str = None, titleFontSize: int = 16):
        corr = self.computeCorrelationMatrix(castTo)
        sns.set(font_scale=fontScale)
        ax = sns.heatmap(
            corr,
            vmin=-1, vmax=1, center=0,
            cmap=sns.diverging_palette(20, 220, n=200),
            square=True,
            annot=annotation
        )
        ax.set_xticklabels(
            ax.get_xticklabels(),
            rotation=45,
            horizontalalignment='right'
        )
        plt.title(title, fontsize=titleFontSize)
        plt.show()


class DataframeUtils:

    @staticmethod
    def ageOfMouse(dataframe: pd.DataFrame, format: str = "%Y-%m-%d"):
        age = np.nan
        dateOfBirth = dataframe["DDN"]
        dateOfDeath = dataframe["date_mort"]
        if dateOfBirth != " " and dateOfDeath != " ":
            dateOfBirth = datetime.strptime(dateOfBirth, format)
            dateOfDeath = datetime.strptime(dateOfDeath, format)
            age = dateOfDeath - dateOfBirth
            age = age.days
            if age < 0:
                age = np.nan
        return age

    @staticmethod
    def nbDaysBetweenDeathAndUse(dataframe: pd.DataFrame, format: str = "%Y-%m-%d"):
        days = np.nan
        dateUse = dataframe["date_utilisation"]
        dateOfDeath = dataframe["date_mort"]
        if dateOfDeath != " " and dateUse != " ":
            dateUse = datetime.strptime(dateUse, format)
            dateOfDeath = datetime.strptime(dateOfDeath, format)
            days = dateUse - dateOfDeath
            days = days.days
        if days < 0:
            days = np.nan
        return days

    @staticmethod
    def injectionVolume(dataframe: pd.DataFrame):
        volumeInjection = dataframe["volume_injection"]
        if volumeInjection == "2 x 200 nl (G+D)":
            injVol = 400
        else:
            try:
                injVol = float(volumeInjection)
            except ValueError:
                injVol = np.nan
        return injVol

    @staticmethod
    def usedValuesStatsPerColumn(dataframe: pd.DataFrame):
        d = dict()
        for column in dataframe.columns:
            array = np.array(dataframe[column])
            total = array.size
            nonNan = np.count_nonzero(~np.isnan(array))
            d[column] = (nonNan / total, nonNan, total)
        return d

    @staticmethod
    def dropRowsWithCertainValues(dataframe: pd.DataFrame, value, columnName: str) -> pd.DataFrame:
        newDataframe = dataframe[dataframe[columnName] != value]
        return newDataframe
