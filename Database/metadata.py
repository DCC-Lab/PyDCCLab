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

        self.channels = []
        self.filters = []

        self.microscope = self.setMicroscope()
        self.objective = self.setObjective()
        self.xScale, self.yScale = self.setXYScale()
        self.xSize, self.ySize = self.setXYSize()
        self.xScaled, self.yScaled = self.setXYScaled()

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


class Filter:
    def __init__(self, min, max):
        self.min = min
        self.max = max


class Channel:
    def __init__(self, name, root):
        self.name = name
        self.root = root

        self.exWavelengthFilter = None
        self.emWavelengthFilter = None

        self.reflector = None
        self.beamsplitter = None
        self.contrastMethod = None
        self.lightSource = None
        self.lightSourceIntensity = None
        self.dyeName = None
        self.channelColor = None
        self.exWavelength = None
        self.emWavelength = None
        self.effectiveNA = None
        self.imagingDevice = None
        self.cameraAdapter = None
        self.exposureTime = None
        self.depthOfFocuse = None
        self.binningMode = None


if __name__ == '__main__':
    '''
    # We create a temporary XML file to use with iterparse.
    # Going directly through a string didn't work.
    cziImageObject = czi.readCziImage('testCziFile.czi')
    stringXML = czi.extractMetadataFromCziFileObject(cziImageObject, 'temp_full')

    root = ET.fromstring(stringXML)

    lstData = []

    # Finding all the channels, their id and name.
    # Then we check for the info we want in those channels.
    tags = ['ExcitationWavelength', 'EmissionWavelength', 'DyeId', 'Color', 'Fluor', 'ExposureTime', 'Reflector',
            'IlluminationType']
    for channel in root.find('./Metadata/Information/Image/Dimensions/Channels'):
        lstChannel = [[channel.attrib['Id'], channel.attrib['Name']]]
        # Finding all of the relevant channel infos.
        for channelData in channel:
            if channelData.tag in tags:
                lstChannel.append([channelData.tag, channelData.text])
            if channelData.tag == 'LightSourcesSettings':
                intensity = channelData.find('LightSourceSettings/Intensity')
                lstChannel.append([intensity.tag, intensity.text])
        lstData.append(lstChannel)

    # Finding all of the filters CutIn and CutOut.
    for filter in root.find('./Metadata/Information/Instrument/Filters'):
        lstFilter = []
        for cut in filter.find('./TransmittanceRange'):
            lstFilter.append([cut.tag, cut.text])
        lstData.append(lstFilter)

    # Finding informations relevant to the Dichroic.
    for dichroic in root.find('./Metadata/Information/Instrument/Dichroics'):
        lstDichroic = [dichroic.attrib['Id']]
        for wavelength in dichroic.find('./Wavelengths'):
            lstDichroic.append(wavelength.text)
        lstData.append(lstDichroic)

    for entry in lstData:
        print(entry)
    '''

    mdata = Metadata('testCziFile.czi')

