import xml.etree.ElementTree as ET
import ImageAnalysis.source.cziUtil as czi
from channel import Channel
from filter import Filter


class Metadata:
    def __init__(self, path):
        self.path = path
        self.root = None

        # Filters and channels are lists of objects.
        self.filters = None
        self.channels = None

        self.microscope = None
        self.objective = None
        self.xScale = 0
        self.yScale = 0
        self.xSize = 0
        self.ySize = 0
        self.xScaled = 0
        self.yScaled = 0

    def __repr__(self):
        return '{};{};{}'.format(self.path, self.filters, self.channels)

    def __eq__(self, other):
        return repr(self) == repr(other)

    def cziFileToCziImageObject(self):
        try:
            return czi.readCziImage(self.path)
        except FileNotFoundError as error:
            raise error
        except ValueError as error:
            raise error

    def extractXmlAsStringFromCziImageObject(self, cziImageObject):
        try:
            return czi.extractMetadataFromCziFileObject(cziImageObject)
        except AttributeError as error:
            raise error

    def createElementTreeRoot(self):
        cziImageObject = self.cziFileToCziImageObject()
        stringXML = self.extractXmlAsStringFromCziImageObject(cziImageObject)
        return ET.fromstring(stringXML)

    def setAttributesFromXml(self):
        self.root = self.createElementTreeRoot()

        self.filters = self.setFiltersData()
        self.channels = self.setChannelsData()

        self.microscope = self.setMicroscope()
        self.objective = self.setObjective()
        self.xScale = self.setXScale()
        self.yScale = self.setYScale()
        self.xSize = self.setXSize()
        self.ySize = self.setYSize()
        self.xScaled = self.setXScaled()
        self.yScaled = self.setYScaled()

    def checkIfElementHasChildren(self, element):
        try:
            if not element.getchildren():
                raise AttributeError
            else:
                return True
        except Exception as error:
            raise error

    def setMicroscope(self):
        try:
            return self.root.find('./Metadata/Information/Instrument/Microscopes/Microscope').attrib['Name']
        except KeyError as error:
            raise error
        except AttributeError as error:
            raise error

    def setObjective(self):
        try:
            return self.root.find('./Metadata/Information/Instrument/Objectives/Objective').attrib['Name']
        except KeyError as error:
            raise error
        except AttributeError as error:
            raise error

    def setXScale(self):
        try:
            return self.root.find('./Metadata/Scaling/Items/Distance[@Id="X"]/Value').text
        except AttributeError as error:
            raise error

    def setYScale(self):
        try:
            return self.root.find('./Metadata/Scaling/Items/Distance[@Id="Y"]/Value').text
        except AttributeError as error:
            raise error

    def setXSize(self):
        try:
            return self.root.find('./Metadata/Information/Image/SizeX').text
        except AttributeError as error:
            raise error

    def setYSize(self):
        try:
            return self.root.find('./Metadata/Information/Image/SizeY').text
        except AttributeError as error:
            raise error

    def setXScaled(self):
        try:
            return float(self.xSize) * float(self.xScale)
        except ValueError as error:
            raise error

    def setYScaled(self):
        try:
            return float(self.ySize) * float(self.yScale)
        except ValueError as error:
            raise error

    def findFiltersEntriesInXml(self):
        filters = []
        try:
            root = self.root.find('./Metadata/Information/Instrument/Filters')
            self.checkIfElementHasChildren(root)

            for filter in root:
                filterId = filter.attrib['Id']
                cutIn = filter.find('./TransmittanceRange/CutIn').text
                cutOut = filter.find('./TransmittanceRange/CutOut').text

                filters.append(Filter(filterId, cutIn, cutOut))
            return filters
        except AttributeError as error:
            raise error
        except KeyError as error:
            raise error

    def setFiltersData(self):
        try:
            filters = self.findFiltersEntriesInXml()
            for filter in filters:
                filter.setFilterData(self.root)
            return filters
        except Exception as error:
            raise error

    def findChannelsEntriesInXml(self):
        channels = []
        try:
            root = self.root.find('./Metadata/Information/Image/Dimensions/Channels')
            self.checkIfElementHasChildren(root)

            for channel in root:
                channels.append(Channel(channel.attrib['Id'], channel.attrib['Name'], self.root))
            return channels
        except AttributeError as error:
            raise error
        except KeyError as error:
            raise error

    def setChannelsData(self):
        try:
            channels = self.findChannelsEntriesInXml()
            for channel in channels:
                channel.getDataFromFilters(self.filters)
            return channels
        except Exception as error:
            raise error
