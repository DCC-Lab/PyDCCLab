import xml.etree.ElementTree as ET
import ImageAnalysis.source.cziUtil as czi
from cziChannel import Channel
from cziFilter import Filter


class Metadata:
    def __init__(self, path, name=None):
        self.mouseId = None
        self.name = name
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

        self.vectors = None

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

    def exportDataAsDict(self):
        return {'name': self.name, 'mouse_id': self.mouseId, 'path': self.path, 'microscope': self.microscope,
                'objective': self.objective, 'x_size': self.xSize, 'y_size': self.ySize, 'x_scale': self.xScale,
                'y_scale': self.yScale, 'x_scaled': self.xScaled, 'y_scaled': self.yScaled, 'vectors': self.vectors}

    def getChannels(self):
        return self.channels

    def getName(self):
        return self.name

    def setMouseId(self, mouseId):
        self.mouseId = mouseId

    def setVectors(self, vectors):
        self.vectors = vectors

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

            print('Attribute "Name" not found for Microscope.')
            return 'Attribute "Name" not found for Microscope.'
        except AttributeError:
            print('Microscope field is empty.')
            return 'Microscope field is empty.'
        except Exception as err:
            print(err)
            return 'Other Exception'

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
            print('Filter attribute error')
            raise
        except KeyError:
            print('Filter Key Error')
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
            print('Channel attribute error.')
            raise
        except KeyError:
            print('Channel key error.')
            raise

    def setChannelsData(self):
        try:
            channels = self.findChannelsEntriesInXml()
            if len(channels) == 0:
                return channels
            for channel in channels:
                channel.getDataFromFilters(self.filters)
                channel.setFileId(self.name)
            return channels
        except Exception:
            raise
