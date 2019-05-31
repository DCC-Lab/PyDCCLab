class Filter:
    def __init__(self, filterId, cutIn, cutOut):
        self.filterId = filterId
        self.cutIn = cutIn
        self.cutOut = cutOut

        self.channelId = None
        self.filterSetId = None
        self.filterType = None
        self.dichroicId = None
        self.dichroic = None

    def __repr__(self):
        return '{};{};{};{}-{}'.format(self.filterId, self.channelId, self.dichroic, self.cutIn, self.cutOut)

    def __eq__(self, other):
        return repr(self) == repr(other)

    def setFilterData(self, root):
        self.setChannelId(root)
        self.setDichroic(root)

    def setFilterSetId(self, root):
        try:
            for filterSet in root.find('./Metadata/Information/Instrument/FilterSets'):
                if self.filterId == filterSet.find('./EmissionFilters/EmissionFilterRef').attrib['Id']:
                    self.filterSetId = filterSet.attrib['Id']
                    self.filterType = 'Emission'
                elif self.filterId == filterSet.find('./ExcitationFilters/ExcitationFilterRef').attrib['Id']:
                    self.filterSetId = filterSet.attrib['Id']
                    self.filterType = 'Excitation'
        except KeyError as error:
            raise error
        except AttributeError as error:
            raise error

    def setChannelId(self, root):
        self.setFilterSetId(root)
        try:
            for channel in root.find('./Metadata/Information/Image/Dimensions/Channels'):
                if channel.find('FilterSetRef').attrib['Id'] == self.filterSetId:
                    self.channelId = channel.attrib['Id']
        except KeyError:
            raise
        except AttributeError:
            raise

    def setDichroicId(self, root):
        try:
            self.dichroicId = root.find('./Metadata/Information/Instrument/FilterSets/FilterSet[@Id="{}"]/DichroicRef'.format(self.filterSetId)).attrib['Id']
        except KeyError:
            raise
        except AttributeError:
            raise

    def setDichroic(self, root):
        self.setDichroicId(root)
        try:
            self.dichroic = root.find('./Metadata/Information/Instrument/Dichroics/Dichroic[@Id="{}"]/Wavelengths/Wavelength'.format(self.dichroicId)).text
        except AttributeError:
            raise
        except KeyError:
            raise

    def getType(self):
        return self.filterType

    def getChannelId(self):
        return self.channelId

    def getFilterRange(self):
        return '{}-{}'.format(self.cutIn, self.cutOut)

    def getDichroic(self):
        return self.dichroic