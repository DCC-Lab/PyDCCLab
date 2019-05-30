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
        self.depthOfFocus = None  # Couldn't find the data. Seems to be an internal formula in the microscope software.
        self.binningMode = self.setBinningMode()

    def __repr__(self):
        return '{};{};{};{}'.format(self.channelId, self.channelName, self.exWavelengthFilter, self.emWavelengthFilter)

    def __eq__(self, other):
        return repr(self) == repr(other)

    def getDataFromFilters(self, filters):
        self.setExWavelengthFilter(filters)
        self.setEmWavelengthFilter(filters)
        self.setBeamsplitter(filters)

    def setExWavelengthFilter(self, filters):
        for filter in filters:
            if filter.getType() == 'Excitation' and self.channelId == filter.getChannelId():
                self.exWavelengthFilter = filter.getFilterRange()

    def setEmWavelengthFilter(self, filters):
        for filter in filters:
            if filter.getType() == 'Emission' and self.channelId == filter.getChannelId():
                self.emWavelengthFilter = filter.getFilterRange()

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