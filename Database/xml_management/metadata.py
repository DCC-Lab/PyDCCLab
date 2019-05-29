import xml.etree.ElementTree as ET
import ImageAnalysis.source.cziUtil as czi
from Database.xml_management.filter import Filter
from Database.xml_management.channel import Channel
import os
import fnmatch


def findAllCziFiles(path):
    print('Walking the directory...')
    allCZIs = []
    for root, directories, files in os.walk(os.path.normpath(path)):
        for file in files:
            if fnmatch.fnmatch(file, '*.czi'):
                allCZIs.append([file, os.path.join(root, file)])
    print('...Done! ' + str(len(allCZIs)) + ' files found!')
    return allCZIs


class Metadata:
    def __init__(self, path):
        self.path = path
        self.root = self.createRoot()

        self.filters = self.setFilters()
        self.channels = self.setChannels()

        self.microscope = self.setMicroscope()
        self.objective = self.setObjective()
        self.xScale, self.yScale = self.setXYScale()
        self.xSize, self.ySize = self.setXYSize()
        self.xScaled, self.yScaled = self.setXYScaled()

    def showData(self):  # TODO This might need to be modified. Currently only for testing purpose.
        print(self.filters)
        print(self.channels)

    def createRoot(self):
        cziImageObject = czi.readCziImage(self.path)
        stringXML = czi.extractMetadataFromCziFileObject(cziImageObject)
        return ET.fromstring(stringXML)

    def setMicroscope(self):
        for microscope in self.root.find('./Metadata/Information/Instrument/Microscopes'):
            return microscope.attrib['Name']

    def setObjective(self):
        for objective in self.root.find('./Metadata/Information/Instrument/Objectives'):
            return objective.attrib['Name']

    def setXYScale(self):
        lstScale = []
        for distance in self.root.find('./Metadata/Scaling/Items'):
            for entry in distance:
                if entry.tag == 'Value':
                    lstScale.append(entry.text)
        return lstScale[0], lstScale[1]

    def setXYSize(self):
        tags = ['SizeX', 'SizeY']
        lstSize = []
        for imageData in self.root.find('./Metadata/Information/Image'):
            if imageData.tag in tags:
                lstSize.append(imageData.text)
        return lstSize[0], lstSize[1]

    def setXYScaled(self):
        xScaled = float(self.xSize) * float(self.xScale)
        yScaled = float(self.ySize) * float(self.yScale)
        return xScaled, yScaled

    def setFilters(self):
        lstFilters = []
        for filter in self.root.find('./Metadata/Information/Instrument/Filters'):
            data = [filter.attrib['Id']]
            for cut in filter.find('./TransmittanceRange'):
                data.append(cut.text)
            lstFilters.append(Filter(data[0], data[1], data[2]))

        for filter in lstFilters:
            filter.setFilterData(self.root)
        return lstFilters

    def setChannels(self):
        lstChannels = []
        for channel in self.root.find('./Metadata/Information/Image/Dimensions/Channels'):
            newChannel = Channel(channel.attrib['Id'], channel.attrib['Name'], self.root)
            newChannel.getDataFromFilters(self.filters)
            lstChannels.append(newChannel)

        return lstChannels


# For testing purpose. To be removed.
if __name__ == '__main__':
    directory = os.path.dirname(os.path.dirname(__file__))
    filepath = os.path.join(directory, 'testCziFile.czi')

    mdata = Metadata(filepath)
    mdata.showData()

