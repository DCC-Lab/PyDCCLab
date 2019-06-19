from typing import Union, List
from .__lifReader import LifReader
from .imageCollection import ZStack


class LIFFile:
    def __init__(self, path: str):
        self.path = path
        lifObject = LifReader(self.path)
        self.series = lifObject.getSeries()

    @property
    def numberOfSeries(self):
        return len(self.series)

    def __len__(self):
        return self.numberOfSeries

    def __getitem__(self, indices: Union[int, tuple, list, slice]=None):
        if indices is None:
            return self.series
        if type(indices) is slice:
            return self.series[indices]
        elif type(indices) is int:
            return self.series[indices]
        elif type(indices) is tuple:
            indices = list(indices)

        if type(indices) is list:
            return [self.series[i] for i in indices]

    def keepSeries(self, indices):
        self.series = self[indices]
        if type(self.series) is not list:
            self.series = [self.series]

    def removeAt(self, index: int):
        self.series.pop(index)

    def getMetadata(self, serieIndex: int=None):
        if serieIndex is None:
            metadata = []
            for serie in self.series:
                metadata.append(serie.getMetadata())
        else:
            metadata = self.series[serieIndex].getMetadata()

        return metadata

    def getZStacks(self, seriesIndices=None, channelIndices=None, crop=False) -> List[ZStack]:
        if type(seriesIndices) is int:
            seriesIndices = [seriesIndices]

        series = self[seriesIndices]

        zStacks = []
        for i, serie in enumerate(series):
            print("... Loading serie {}/{}".format(i+1, len(series)))
            stackArray = serie.getStack(channelIndices)
            print("... Loading ZStack Collection".format(i+1, len(series)))
            zStack = ZStack(imagesArray=stackArray, cropAtInit=crop)
            zStacks.append(zStack)

        return zStacks
