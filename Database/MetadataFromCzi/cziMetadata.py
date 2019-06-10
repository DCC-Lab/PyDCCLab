import xml.etree.ElementTree as ET
import ImageAnalysis.source.cziUtil as czi
from cziChannel import Channel
from cziFilter import Filter
from cziName import Name


class Metadata:
    def __init__(self, path, name=''):
        self.name = Name(name)
        self.path = path
        self.root = self.createElementTreeRoot()

        # Filters and channels are lists of objects.
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

    def __repr__(self):
        return '{};{};{}'.format(self.path, self.filters, self.channels)

    def __eq__(self, other):
        return repr(self) == repr(other)

    def cziFileToCziImageObject(self):
        try:
            return czi.readCziImage(self.path)
        except FileNotFoundError:
            raise
        except ValueError:
            raise

    def extractXmlAsStringFromCziImageObject(self, cziImageObject):
        try:
            return czi.extractMetadataFromCziFileObject(cziImageObject)
        except AttributeError:
            raise

    def createElementTreeRoot(self):
        cziImageObject = self.cziFileToCziImageObject()
        stringXML = self.extractXmlAsStringFromCziImageObject(cziImageObject)
        return ET.fromstring(stringXML)

    def exportAsDict(self):
        dictMeta = {'path': self.path, 'microscope': self.microscope, 'objective': self.objective, 'x_size': self.xSize,
                    'y_size': self.ySize, 'x_scale': self.xScale, 'y_scale': self.yScale, 'x_scaled': self.xScaled,
                    'y_scaled': self.yScaled}
        dictName = self.name.exportAsDict()
        dictReturned = {**dictMeta, **dictName}
        return dictReturned

    def getChannels(self):
        return self.channels

    def checkIfElementHasChildren(self, element):
        if element is None:
            return False
        try:
            if not list(element):
                return False
            return True
        except Exception:
            return False

    def setMicroscope(self):
        try:
            return self.root.find('./Metadata/Information/Instrument/Microscopes/Microscope').attrib['Name']
        except KeyError as err:
            return 'Attribute "Name" not found for Microscope.'
        except AttributeError:
            return 'Microscope field is empty.'

    def setObjective(self):
        try:
            return self.root.find('./Metadata/Information/Instrument/Objectives/Objective').attrib['Name']
        except KeyError:
            return 'Attribute "Name" not found for Objective.'
        except AttributeError:
            return 'Objective field is empty.'

    def setXScale(self):
        try:
            return self.root.find('./Metadata/Scaling/Items/Distance[@Id="X"]/Value').text
        except AttributeError:
            return 'Either the id "X" could not be found or the field is empty for xScale.'

    def setYScale(self):
        try:
            return self.root.find('./Metadata/Scaling/Items/Distance[@Id="Y"]/Value').text
        except AttributeError:
            return 'Either the id "Y" could not be found or the field is empty for yScale.'

    def setXSize(self):
        try:
            return self.root.find('./Metadata/Information/Image/SizeX').text
        except AttributeError:
            return 'SizeX field is empty.'

    def setYSize(self):
        try:
            return self.root.find('./Metadata/Information/Image/SizeY').text
        except AttributeError:
            return 'SizeY field is empty.'

    def setXScaled(self):
        try:
            return float(self.xSize) * float(self.xScale)
        except ValueError:
            return 0

    def setYScaled(self):
        try:
            return float(self.ySize) * float(self.yScale)
        except ValueError:
            return 0

    def findFiltersEntriesInXml(self):
        filters = []
        try:
            root = self.root.find('./Metadata/Information/Instrument/Filters')
            if self.checkIfElementHasChildren(root):
                for filter in root:
                    filterId = filter.attrib['Id']
                    cutIn = filter.find('./TransmittanceRange/CutIn').text
                    cutOut = filter.find('./TransmittanceRange/CutOut').text

                    filters.append(Filter(filterId, cutIn, cutOut))
            return filters
        except AttributeError:
            raise
        except KeyError:
            raise

    def setFiltersData(self):
        try:
            filters = self.findFiltersEntriesInXml()
            if len(filters) == 0:
                return filters
            for filter in filters:
                filter.setFilterData(self.root)
            return filters
        except Exception:
            raise

    def findChannelsEntriesInXml(self):
        channels = []
        try:
            root = self.root.find('./Metadata/Information/Image/Dimensions/Channels')
            if self.checkIfElementHasChildren(root):
                for channel in root:
                    channels.append(Channel(channel.attrib['Id'], channel.attrib['Name'], self.root))
            return channels
        except AttributeError:
            raise
        except KeyError:
            raise

    def setChannelsData(self):
        try:
            channels = self.findChannelsEntriesInXml()
            if len(channels) == 0:
                return channels
            for channel in channels:
                channel.getDataFromFilters(self.filters)
                channel.setFileId(self.name.name)
            return channels
        except Exception:
            raise
