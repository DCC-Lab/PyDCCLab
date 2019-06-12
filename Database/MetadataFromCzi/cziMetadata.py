import xml.etree.ElementTree as ET
import dcclab.cziUtil as czi
from cziChannel import CZIChannel
from cziFilter import CZIFilter
import re


class CZIMetadata:
    def __init__(self, path, name=''):
        self.name = name
        self.path = path
        self.root = self.createElementTreeRoot()

        # Filters and channels are lists of objects.
        self.filters = self.findFiltersInRoot()
        self.channels = self.findChannelsInRoot()

        self.mouseId = self.setMouseId()
        self.viralVectors = self.setViralVectors()
        self.injectionSite = self.setInjectionSite()
        self.microscope = self.setMicroscope()
        self.objective = self.setObjective()
        self.xScale = self.setXScale()
        self.yScale = self.setYScale()
        self.xSize = self.setXSize()
        self.ySize = self.setYSize()
        self.tags = self.setTags()

    def __repr__(self):
        return '{};{};{}'.format(self.path, self.filters, self.channels)

    def __eq__(self, other):
        return repr(self) == repr(other)

    def exportAsDict(self):
        return {'path': self.path, 'microscope': self.microscope, 'objective': self.objective, 'x_size': self.xSize,
                'y_size': self.ySize, 'x_scale': self.xScale, 'y_scale': self.yScale, 'x_scaled': self.xScaled,
                'y_scaled': self.yScaled, 'name': self.name, 'mouse_id': self.mouseId,
                'viral_vectors': self.formatViralVectors(), 'injection_site': self.injectionSite, 'tags': self.tags}

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

    def checkIfElementHasChildren(self, element):
        if element is None:
            return False
        try:
            if not list(element):
                return False
            return True
        except Exception:
            return False

    def setMouseId(self):
        # Pattern is s followed by 1 to 4 digits and ignoring lower or upper case.
        # Return the digits.
        try:
            return re.search(r's\d{1,4}', self.name, re.IGNORECASE).group()[1:]
        except AttributeError:
            return 0

    def setViralVectors(self):
        try:
            vectors = []
            vectors.extend(self.findAAVVectors())
            vectors.extend(self.findRabVectors())
            return vectors
        except Exception:
            pass

    def formatViralVectors(self):
        if self.viralVectors:
            vectorLine = ''
            for vector in self.viralVectors:
                vectorLine += vector + ';'
            return vectorLine.rstrip(';')

    def findRabVectors(self):
        # We can have either rab#.# or rabv#.# so we try to find either patterns.
        try:
            return re.findall(r'(rabv?\d(?:\.\d))', self.name, re.IGNORECASE)
        except Exception:
            return []

    def findAAVVectors(self):
        # We can have either very distinct AAV### patterns or AAV###+### or AAV###-###.
        # We have to search for all three. AAV###-### and AAV###+### are splitted into different vectors and their
        # names are normalized to AAV###.
        try:
            AAVs = re.findall(r'AAV\d{3,4}[+-]\d{3,4}|AAV\d{3,4}', self.name, re.IGNORECASE)
            for AAV in AAVs:
                if re.search(r'[+-]', AAV):
                    splitAAV = re.compile(r'[+-]').split(AAV)
                    for i in range(len(splitAAV)):
                        if re.match(r'^\d{3,4}', splitAAV[i]):
                            splitAAV[i] = splitAAV[i].replace(splitAAV[i], 'AAV' + splitAAV[i])
                    AAVs.remove(AAV)
                    AAVs.extend(splitAAV)
            return AAVs
        except Exception:
            return []

    def setInjectionSite(self):
        try:
            return re.search(r'patte|IV', self.name, re.IGNORECASE).group()
        except Exception:
            return ''

    def setMicroscope(self):
        try:
            return self.root.find('./Metadata/Information/Instrument/Microscopes/Microscope').attrib['Name']
        except Exception:
            return None

    def setObjective(self):
        try:
            return self.root.find('./Metadata/Information/Instrument/Objectives/Objective').attrib['Name']
        except Exception:
            return None

    def setXScale(self):
        try:
            return self.root.find('./Metadata/Scaling/Items/Distance[@Id="X"]/Value').text
        except Exception:
            return None

    def setYScale(self):
        try:
            return self.root.find('./Metadata/Scaling/Items/Distance[@Id="Y"]/Value').text
        except Exception:
            return None

    def setXSize(self):
        try:
            return self.root.find('./Metadata/Information/Image/SizeX').text
        except Exception:
            return None

    def setYSize(self):
        try:
            return self.root.find('./Metadata/Information/Image/SizeY').text
        except Exception:
            return None

    @property
    def xScaled(self):
        try:
            return float(self.xSize) * float(self.xScale)
        except Exception:
            return None

    @property
    def yScaled(self):
        try:
            return float(self.ySize) * float(self.yScale)
        except Exception:
            return None

    def findFiltersInRoot(self):
        newFilters = []
        try:
            filters = self.root.find('./Metadata/Information/Instrument/Filters')
            if self.checkIfElementHasChildren(filters):
                for filter in filters:
                    filterId = filter.attrib['Id']
                    newFilters.append(CZIFilter(filterId, self.root))
            return newFilters
        except Exception:
            return newFilters

    def findChannelsInRoot(self):
        newChannels = []
        try:
            channels = self.root.find('./Metadata/Information/Image/Dimensions/Channels')
            if self.checkIfElementHasChildren(channels):
                for channel in channels:
                    channelInformation = [channel.attrib['Id'], channel.attrib['Name'], self.name]
                    newChannels.append(CZIChannel(channelInformation, self.filters, self.root))
            return newChannels
        except Exception:
            return newChannels

    def setTags(self):
        try:
            tagLine = ''
            tags = re.findall(r'moelle|neurones|drg|BB|anti\s?mcherry|anti\s?rabbit|cre|cx3cr1', self.name, re.IGNORECASE)
            for tag in tags:
                trueTag = tag.replace(' ', '')
                if tagLine.find(trueTag) == -1:
                    tagLine += trueTag + ';'
            return tagLine.rstrip(';')
        except Exception:
            return []