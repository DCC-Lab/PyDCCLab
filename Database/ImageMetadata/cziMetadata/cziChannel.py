class CZIChannel:
    def __init__(self, channelInformation, filters, root):
        self.channelId = '{};{}'.format(channelInformation[2], channelInformation[0])
        self.channel = channelInformation[0]
        self.channelName = channelInformation[1]
        self.fileId = channelInformation[2]
        self.root = root

        # These variables get their testData from filter objects.
        self.exWavelengthFilter = self.setExWavelengthFilter(filters)
        self.emWavelengthFilter = self.setEmWavelengthFilter(filters)
        self.beamsplitter = self.setBeamsplitter(filters)

        # These variables get their testData from root.
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
        self.binningMode = self.setBinningMode()

    def __repr__(self):
        return '{};{};{};{}'.format(self.channel, self.channelName, self.exWavelengthFilter, self.emWavelengthFilter)

    def __eq__(self, other):
        return repr(self) == repr(other)

    def asDict(self):
        return {'file_id': self.fileId, 'channel_id': self.channelId, 'channel_name': self.channelName,
                'ex_wavelength_filter': self.exWavelengthFilter, 'em_wavelength_filter': self.emWavelengthFilter,
                'beamsplitter': self.beamsplitter, 'reflector': self.reflector, 'contrast_method': self.contrastMethod,
                'light_source': self.lightSource, 'light_source_intensity': self.lightSourceIntensity,
                'dye_name': self.dyeName, 'channel_color': self.channelColor, 'ex_wavelength': self.exWavelength,
                'em_wavelength': self.emWavelength, 'effective_na': self.effectiveNA,
                'imaging_device': self.imagingDevice, 'camera_adapter': self.cameraAdapter,
                'exposure_time': self.exposureTime, 'binning_mode': self.binningMode}

    @property
    def keys(self):
        return {'file_id': 'TEXT', 'channel_id': 'TEXT', 'channel_name': 'TEXT', 'ex_wavelength_filter': 'TEXT',
                'em_wavelength_filter': 'TEXT', 'beamsplitter': 'INTEGER', 'reflector': 'TEXT',
                'contrast_method': 'TEXT', 'light_source': 'TEXT', 'light_source_intensity': 'TEXT', 'dye_name': 'TEXT',
                'channel_color': 'TEXT', 'ex_wavelength': 'INTEGER', 'em_wavelength': 'INTEGER', 'effective_na': 'REAL',
                'imaging_device': 'TEXT', 'camera_adapter': 'TEXT', 'exposure_time': 'TEXT', 'binning_mode': 'REAL'}

    def setExWavelengthFilter(self, filters):
        try:
            for filter in filters:
                if filter.getType() == 'Excitation' and self.channel == filter.getChannelId():
                    return filter.getFilterRange()
            return None
        except Exception:
            return None

    def setEmWavelengthFilter(self, filters):
        try:
            for filter in filters:
                if filter.getType() == 'Emission' and self.channel == filter.getChannelId():
                    return filter.getFilterRange()
            return None
        except Exception:
            return None

    def setBeamsplitter(self, filters):
        try:
            for filter in filters:
                if self.channel == filter.getChannelId():
                    return filter.getDichroic()
            return None
        except Exception:
            return None

    def setReflector(self):
        try:
            return self.root.find('./Metadata/Information/Image/Dimensions/Channels/Channel[@Id="{}"]'
                                  '/Reflector'.format(self.channel)).text
        except Exception:
            return None

    def setContrastMethod(self):
        try:
            return self.root.find('./Metadata/Information/Image/Dimensions/Channels/Channel[@Id="{}"]'
                                  '/ContrastMethod'.format(self.channel)).text
        except Exception:
            return None

    def setLightSource(self):
        try:
            lightId = self.root.find('./Metadata/Information/Image/Dimensions/Channels/Channel[@Id="{}"]'
                                     '/LightSourcesSettings/LightSourceSettings/LightSource'.format(self.channel)).attrib['Id']
            return self.root.find('./Metadata/Information/Instrument/LightSources'
                                  '/LightSource[@Id="{}"]'.format(lightId)).attrib['Name']
        except Exception:
            return None

    def setLightSourceIntensity(self):
        try:
            return self.root.find('./Metadata/Information/Image/Dimensions/Channels/Channel[@Id="{}"]'
                                  '/LightSourcesSettings/LightSourceSettings/Intensity'.format(self.channel)).text
        except Exception:
            return None

    def setDyeName(self):
        try:
            return self.root.find('./Metadata/DisplaySetting/Channels/Channel[@Id="{}"]'
                                  '/DyeName'.format(self.channel)).text
        except Exception:
            return None

    def setChannelColor(self):
        try:
            return self.root.find('./Metadata/Information/Image/Dimensions/Channels/Channel[@Id="{}"]'
                                  '/Color'.format(self.channel)).text
        except Exception:
            return None

    def setExWavelength(self):
        try:
            return self.root.find('./Metadata/Information/Image/Dimensions/Channels/Channel[@Id="{}"]'
                                  '/ExcitationWavelength'.format(self.channel)).text
        except Exception:
            return None

    def setEmWavelength(self):
        try:
            return self.root.find('./Metadata/Information/Image/Dimensions/Channels/Channel[@Id="{}"]'
                                  '/EmissionWavelength'.format(self.channel)).text
        except Exception:
            return None

    def setExposureTime(self):
        try:
            return self.root.find('./Metadata/Information/Image/Dimensions/Channels/Channel[@Id="{}"]'
                                  '/ExposureTime'.format(self.channel)).text
        except Exception:
            return None

    def setEffectiveNA(self):
        try:
            return self.root.find('./Metadata/Information/Instrument/Objectives/Objective/LensNA').text
        except Exception:
            return None

    def setImagingDevice(self):
        try:
            return self.root.find('./Metadata/Information/Instrument/Detectors/Detector').attrib['Name']
        except Exception:
            return None

    def setCameraAdapter(self):
        try:
            return self.root.find('./Metadata/Information/Instrument/Detectors/Detector/Adapter/Manufacturer/Model').text
        except Exception:
            return None

    def setBinningMode(self):
        try:
            return self.root.find('./Metadata/Information/Image/Dimensions/Channels/Channel/DetectorSettings/Binning').text
        except Exception:
            return None
