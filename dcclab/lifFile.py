from typing import Union
from .__lifReader import LifReader


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

    def getZStacks(self, seriesIndices=None, channels=None):
        if type(seriesIndices) is int:
            seriesIndices = [seriesIndices]

        series = self[seriesIndices]

        stacks = []
        for serie in series:
            # TODO: create ZStackCollection Object with array
            stacks.append(serie.getStack(channels))  # numpy array

        return stacks
