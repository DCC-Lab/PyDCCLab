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
        try:
            for filter in filters:
                if filter.getType() == 'Excitation' and self.channelId == filter.getChannelId():
                    self.exWavelengthFilter = filter.getFilterRange()
        except Exception:
            raise

    def setEmWavelengthFilter(self, filters):
        try:
            for filter in filters:
                if filter.getType() == 'Emission' and self.channelId == filter.getChannelId():
                    self.emWavelengthFilter = filter.getFilterRange()
        except Exception:
            raise

    def setBeamsplitter(self, filters):
        try:
            for filter in filters:
                if self.channelId == filter.getChannelId():
                    self.beamsplitter = filter.getDichroic()
        except Exception:
            raise

    def setReflector(self):
        try:
            return self.root.find('./Metadata/Information/Image/Dimensions/Channels/Channel[@Id="{}"]'
                                  '/Reflector'.format(self.channelId)).text
        except AttributeError:
            raise

    def setContrastMethod(self):
        try:
            return self.root.find('./Metadata/Information/Image/Dimensions/Channels/Channel[@Id="{}"]'
                                  '/ContrastMethod'.format(self.channelId)).text
        except AttributeError:
            raise

    def setLightSource(self):
        try:
            lightId = self.root.find('./Metadata/Information/Image/Dimensions/Channels/Channel[@Id="{}"]'
                                     '/LightSourcesSettings/LightSourceSettings/LightSource'.format(self.channelId)).attrib['Id']
            return self.root.find('./Metadata/Information/Instrument/LightSources'
                                  '/LightSource[@Id="{}"]'.format(lightId)).attrib['Name']
        except AttributeError:
            raise
        except KeyError:
            raise

    def setLightSourceIntensity(self):
        try:
            return self.root.find('./Metadata/Information/Image/Dimensions/Channels/Channel[@Id="{}"]'
                                  '/LightSourcesSettings/LightSourceSettings/Intensity'.format(self.channelId)).text
        except AttributeError:
            raise

    def setDyeName(self):
        try:
            return self.root.find('./Metadata/DisplaySetting/Channels/Channel[@Id="{}"]'
                                  '/DyeName'.format(self.channelId)).text
        except AttributeError:
            raise

    def setChannelColor(self):
        try:
            return self.root.find('./Metadata/Information/Image/Dimensions/Channels/Channel[@Id="{}"]'
                                  '/Color'.format(self.channelId)).text
        except AttributeError:
            raise

    def setExWavelength(self):
        try:
            return self.root.find('./Metadata/Information/Image/Dimensions/Channels/Channel[@Id="{}"]'
                                  '/ExcitationWavelength'.format(self.channelId)).text
        except AttributeError:
            raise

    def setEmWavelength(self):
        try:
            return self.root.find('./Metadata/Information/Image/Dimensions/Channels/Channel[@Id="{}"]'
                                  '/EmissionWavelength'.format(self.channelId)).text
        except AttributeError:
            raise

    def setExposureTime(self):
        try:
            return self.root.find('./Metadata/Information/Image/Dimensions/Channels/Channel[@Id="{}"]'
                                  '/ExposureTime'.format(self.channelId)).text
        except AttributeError:
            raise

    def setEffectiveNA(self):
        try:
            return self.root.find('./Metadata/Information/Instrument/Objectives/Objective/LensNA').text
        except AttributeError:
            raise

    def setImagingDevice(self):
        try:
            return self.root.find('./Metadata/Information/Instrument/Detectors/Detector').attrib['Name']
        except KeyError:
            raise
        except AttributeError:
            raise

    def setCameraAdapter(self):
        try:
            return self.root.find('./Metadata/Information/Instrument/Detectors/Detector/Adapter/Manufacturer/Model').text
        except AttributeError:
            raise

    def setBinningMode(self):
        try:
            return self.root.find('./Metadata/Information/Image/Dimensions/Channels/Channel/DetectorSettings/Binning').text
        except AttributeError:
            raise
