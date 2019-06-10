import xml.etree.ElementTree as ET
import ImageAnalysis.source.cziUtil as czi
from cziChannel import CZIChannel
from cziFilter import CZIFilter
from cziNameAnalysis import CZINameAnalysis


class CZIMetadata:
    def __init__(self, path, fileName=''):
        self.path = path
        self.root = self.createElementTreeRoot()
        self.fileNameAnalysis = CZINameAnalysis(fileName)

        # Filters and channels are lists of objects.
        self.filters = self.findFiltersInRoot()
        self.channels = self.findChannelsInRoot()

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
        dictName = self.fileNameAnalysis.exportAsDict()
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
        except KeyError:
            return "Name not found."
        except AttributeError:
            return "Empty field."

    def setObjective(self):
        try:
            return self.root.find('./Metadata/Information/Instrument/Objectives/Objective').attrib['Name']
        except KeyError:
            return "Name not found."
        except AttributeError:
            return 'Empty field.'

    def setXScale(self):
        try:
            return self.root.find('./Metadata/Scaling/Items/Distance[@Id="X"]/Value').text
        except AttributeError:
            return 0

    def setYScale(self):
        try:
            return self.root.find('./Metadata/Scaling/Items/Distance[@Id="Y"]/Value').text
        except AttributeError:
            return 0

    def setXSize(self):
        try:
            return self.root.find('./Metadata/Information/Image/SizeX').text
        except AttributeError:
            return 0

    def setYSize(self):
        try:
            return self.root.find('./Metadata/Information/Image/SizeY').text
        except AttributeError:
            return 0

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

    def findFiltersInRoot(self):
        filters = []
        try:
            root = self.root.find('./Metadata/Information/Instrument/Filters')
            if self.checkIfElementHasChildren(root):
                for filter in root:
                    filterId = filter.attrib['Id']

                    filters.append(CZIFilter(filterId, self.root))
            return filters
        except AttributeError:
            print('Atribute error in findFiltersInRoot')
        except KeyError:
            print('Key error in findFiltersInRoot')

    def findChannelsInRoot(self):
        channels = []
        try:
            root = self.root.find('./Metadata/Information/Image/Dimensions/Channels')
            if self.checkIfElementHasChildren(root):
                for channel in root:
                    channelInformation = [channel.attrib['Id'], channel.attrib['Name'], self.fileNameAnalysis.name]
                    channels.append(CZIChannel(channelInformation, self.filters, self.root))
            return channels
        except AttributeError:
            print('Attribute error in findChannelsInRoot.')
        except KeyError:
            print('Key error in findChannelsInRoot.')
