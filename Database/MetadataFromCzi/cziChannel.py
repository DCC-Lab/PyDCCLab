class CZIChannel:
    def __init__(self, channelInformation: list, filters, root):
        self.channelId = channelInformation[0]
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
        return '{};{};{};{}'.format(self.channelId, self.channelName, self.exWavelengthFilter, self.emWavelengthFilter)

    def __eq__(self, other):
        return repr(self) == repr(other)

    def exportAsDict(self):
        return {'file_id': self.fileId, 'channel_id': self.channelId, 'channel_name': self.channelName,
                'ex_wavelength_filter': self.exWavelengthFilter, 'em_wavelength_filter': self.emWavelengthFilter,
                'beamsplitter': self.beamsplitter, 'reflector': self.reflector, 'contrast_method': self.contrastMethod,
                'light_source': self.lightSource, 'light_source_intensity': self.lightSourceIntensity,
                'dye_name': self.dyeName, 'channel_color': self.channelColor, 'ex_wavelength': self.exWavelength,
                'em_wavelength': self.emWavelength, 'effective_na': self.effectiveNA,
                'imaging_device': self.imagingDevice, 'camera_adapter': self.cameraAdapter,
                'exposure_time': self.exposureTime, 'binning_mode': self.binningMode}

    def setExWavelengthFilter(self, filters):
        try:
            if not filters:
                return -1
            for filter in filters:
                if filter.getType() == 'Excitation' and self.channelId == filter.getChannelId():
                    return filter.getFilterRange()
                else:
                    return 0
        except AttributeError:
            return -1

    def setEmWavelengthFilter(self, filters):
        try:
            if not filters:
                return -1
            for filter in filters:
                if filter.getType() == 'Emission' and self.channelId == filter.getChannelId():
                    return filter.getFilterRange()
                else:
                    return 0
        except AttributeError:
            return -1

    def setBeamsplitter(self, filters):
        try:
            if not filters:
                return -1
            for filter in filters:
                if self.channelId == filter.getChannelId():
                    return filter.getDichroic()
                else:
                    return 0
        except AttributeError:
            return -1

    def setReflector(self):
        try:
            return self.root.find('./Metadata/Information/Image/Dimensions/Channels/Channel[@Id="{}"]'
                                  '/Reflector'.format(self.channelId)).text
        except AttributeError:
            return 'Missing attribute or key.'

    def setContrastMethod(self):
        try:
            return self.root.find('./Metadata/Information/Image/Dimensions/Channels/Channel[@Id="{}"]'
                                  '/ContrastMethod'.format(self.channelId)).text
        except AttributeError:
            return 'Missing attribute or key.'

    def setLightSource(self):
        try:
            lightId = self.root.find('./Metadata/Information/Image/Dimensions/Channels/Channel[@Id="{}"]'
                                     '/LightSourcesSettings/LightSourceSettings/LightSource'.format(self.channelId)).attrib['Id']
            return self.root.find('./Metadata/Information/Instrument/LightSources'
                                  '/LightSource[@Id="{}"]'.format(lightId)).attrib['Name']
        except AttributeError:
            return ''
        except KeyError:
            return ''

    def setLightSourceIntensity(self):
        try:
            return self.root.find('./Metadata/Information/Image/Dimensions/Channels/Channel[@Id="{}"]'
                                  '/LightSourcesSettings/LightSourceSettings/Intensity'.format(self.channelId)).text
        except AttributeError:
            return ''

    def setDyeName(self):
        try:
            return self.root.find('./Metadata/DisplaySetting/Channels/Channel[@Id="{}"]'
                                  '/DyeName'.format(self.channelId)).text
        except AttributeError:
            return ''

    def setChannelColor(self):
        try:
            return self.root.find('./Metadata/Information/Image/Dimensions/Channels/Channel[@Id="{}"]'
                                  '/Color'.format(self.channelId)).text
        except AttributeError:
            return ''

    def setExWavelength(self):
        try:
            return self.root.find('./Metadata/Information/Image/Dimensions/Channels/Channel[@Id="{}"]'
                                  '/ExcitationWavelength'.format(self.channelId)).text
        except AttributeError:
            return 0

    def setEmWavelength(self):
        try:
            return self.root.find('./Metadata/Information/Image/Dimensions/Channels/Channel[@Id="{}"]'
                                  '/EmissionWavelength'.format(self.channelId)).text
        except AttributeError:
            return 0

    def setExposureTime(self):
        try:
            return self.root.find('./Metadata/Information/Image/Dimensions/Channels/Channel[@Id="{}"]'
                                  '/ExposureTime'.format(self.channelId)).text
        except AttributeError:
            return 0

    def setEffectiveNA(self):
        try:
            return self.root.find('./Metadata/Information/Instrument/Objectives/Objective/LensNA').text
        except AttributeError:
            return 0

    def setImagingDevice(self):
        try:
            return self.root.find('./Metadata/Information/Instrument/Detectors/Detector').attrib['Name']
        except KeyError:
            return ''
        except AttributeError:
            return ''

    def setCameraAdapter(self):
        try:
            return self.root.find('./Metadata/Information/Instrument/Detectors/Detector/Adapter/Manufacturer/Model').text
        except AttributeError:
            return ''

    def setBinningMode(self):
        try:
            return self.root.find('./Metadata/Information/Image/Dimensions/Channels/Channel/DetectorSettings/Binning').text
        except AttributeError:
            return 0
