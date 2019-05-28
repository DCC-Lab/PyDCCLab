import xml.etree.ElementTree as ET
import os
import fnmatch
import ImageAnalysis.cziUtil as czi


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

    def showData(self):
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


class Filter:
    def __init__(self, filterId, min, max):
        self.filterId = filterId
        self.min = min
        self.max = max

        self.channelId = None
        self.filterSetId = None
        self.type = None
        self.dichroicId = None
        self.dichroic = None

    def __repr__(self):
        return '{};{};{}-{}'.format(self.filterId, self.channelId, self.min, self.max)

    def setFilterData(self, root):
        self.setChannelId(root)
        self.setFilterSetId(root)
        self.setDichroicId(root)
        self.setDichroic(root)

    def setFilterSetId(self, root):
        for filterSet in root.find('./Metadata/Information/Instrument/FilterSets'):
            if self.filterId == filterSet.find('./EmissionFilters/EmissionFilterRef').attrib['Id']:
                self.filterSetId = filterSet.attrib['Id']
                self.type = 'Emission'
            elif self.filterId == filterSet.find('./ExcitationFilters/ExcitationFilterRef').attrib['Id']:
                self.filterSetId = filterSet.attrib['Id']
                self.type = 'Excitation'

    def setChannelId(self, root):
        self.setFilterSetId(root)

        for channel in root.find('./Metadata/Information/Image/Dimensions/Channels'):
            if channel.find('FilterSetRef').attrib['Id'] == self.filterSetId:
                self.channelId = channel.attrib['Id']

    def setDichroicId(self, root):
        for filterSet in root.find('./Metadata/Information/Instrument/FilterSets'):
            if filterSet.attrib['Id'] == self.filterSetId:
                self.dichroicId = filterSet.find('./DichroicRef').attrib['Id']
                self.setDichroic(root)

    def setDichroic(self, root):
        for dichroic in root.find('./Metadata/Information/Instrument/Dichroics'):
            if dichroic.attrib['Id'] == self.dichroicId:
                self.dichroic = dichroic.find('./Wavelengths/Wavelength').text

    def getType(self):
        return self.type

    def getChannelId(self):
        return self.channelId

    def getFilter(self):
        return '{}-{}'.format(self.min, self.max)

    def getDichroic(self):
        return self.dichroic


class Channel:
    def __init__(self, channelId, channelName, root):
        self.channelId = channelId
        self.channelName = channelName
        self.root = root

        # These variables get their data from filter objects.
        self.exWavelengthFilter = None
        self.emWavelengthFilter = None
        self.beamsplitter = None

        # These variables get their data from root.
        self.reflector = self.setReflector()
        self.contrastMethod = self.setContrastMethod()
        self.lightSource = self.setLightSource()
        self.lightSourceIntensity = self.setLightSourceIntensity()
        self.dyeName = self.setDyeName()
        self.channelColor = self.setChannelColor()
        self.exWavelength = self.setExWavelength()
        self.emWavelength = self.setEmWavelength()
        self.effectiveNA = self.setEffectiveNA()
        self.imagingDevice = self.setImagingDevice()
        self.cameraAdapter = self.setCameraAdapter()
        self.exposureTime = self.setExposureTime()
        self.depthOfFocus = None
        self.binningMode = self.setBinningMode()

    def __repr__(self):
        reprLine = '{} {} {} {} {}\n'.format(self.channelId, self.channelName, self.exWavelengthFilter,
                                             self.emWavelengthFilter, self.reflector)
        reprLine += '{} {} {} {} {}\n'.format(self.beamsplitter, self.contrastMethod, self.lightSource,
                                              self.lightSourceIntensity, self.dyeName)
        reprLine += '{} {} {} {} {}\n'.format(self.channelColor, self.exWavelength, self.emWavelength, self.effectiveNA,
                                              self.imagingDevice)
        reprLine += '{} {} {}'.format(self.cameraAdapter, self.exposureTime, self.binningMode)
        return reprLine

    def getDataFromFilters(self, filters):
        self.setExWavelengthFilter(filters)
        self.setEmWavelengthFilter(filters)
        self.setBeamsplitter(filters)

    def setExWavelengthFilter(self, filters):
        for filter in filters:
            if filter.getType() == 'Excitation' and self.channelId == filter.getChannelId():
                self.exWavelengthFilter = filter.getFilter()

    def setEmWavelengthFilter(self, filters):
        for filter in filters:
            if filter.getType() == 'Emission' and self.channelId == filter.getChannelId():
                self.emWavelengthFilter = filter.getFilter()

    def setBeamsplitter(self, filters):
        for filter in filters:
            if self.channelId == filter.getChannelId():
                self.beamsplitter = filter.getDichroic()

    def setReflector(self):
        for channel in self.root.find('./Metadata/Information/Image/Dimensions/Channels'):
            if channel.attrib['Id'] == self.channelId:
                return channel.find('./Reflector').text

    def setContrastMethod(self):
        for channel in self.root.find('./Metadata/Information/Image/Dimensions/Channels'):
            if channel.attrib['Id'] == self.channelId:
                return channel.find('./ContrastMethod').text

    def setLightSource(self):
        lightId = ''
        for channel in self.root.find('./Metadata/Information/Image/Dimensions/Channels'):
            if channel.attrib['Id'] == self.channelId:
                lightId = channel.find('./LightSourcesSettings/LightSourceSettings/LightSource').attrib['Id']

        for lightSource in self.root.find('./Metadata/Information/Instrument/LightSources'):
            if lightSource.attrib['Id'] == lightId:
                return lightSource.attrib['Name']

    def setLightSourceIntensity(self):
        for channel in self.root.find('./Metadata/Information/Image/Dimensions/Channels'):
            if channel.attrib['Id'] == self.channelId:
                return channel.find('./LightSourcesSettings/LightSourceSettings/Intensity').text

    def setDyeName(self):
        for channel in self.root.find('./Metadata/DisplaySetting/Channels'):
            if channel.attrib['Id'] == self.channelId:
                return channel.find('./DyeName').text

    def setChannelColor(self):
        for channel in self.root.find('./Metadata/Information/Image/Dimensions/Channels'):
            if channel.attrib['Id'] == self.channelId:
                return channel.find('./Color').text

    def setExWavelength(self):
        for channel in self.root.find('./Metadata/Information/Image/Dimensions/Channels'):
            if channel.attrib['Id'] == self.channelId:
                return channel.find('./ExcitationWavelength').text

    def setEmWavelength(self):
        for channel in self.root.find('./Metadata/Information/Image/Dimensions/Channels'):
            if channel.attrib['Id'] == self.channelId:
                return channel.find('./EmissionWavelength').text

    def setExposureTime(self):
        for channel in self.root.find('./Metadata/Information/Image/Dimensions/Channels'):
            if channel.attrib['Id'] == self.channelId:
                return channel.find('./ExposureTime').text

    def setEffectiveNA(self):
        return self.root.find('./Metadata/Information/Instrument/Objectives/Objective/LensNA').text

    def setImagingDevice(self):
        return self.root.find('./Metadata/Information/Instrument/Detectors/Detector').attrib['Name']

    def setCameraAdapter(self):
        return self.root.find('./Metadata/Information/Instrument/Detectors/Detector/Adapter/Manufacturer/Model').text

    def setBinningMode(self):
        return self.root.find('./Metadata/Information/Image/Dimensions/Channels/Channel/DetectorSettings/Binning').text


if __name__ == '__main__':
    mdata = Metadata('testCziFile.czi')
    mdata.showData()

