class Filter:
    def __init__(self, filterId, cutIn, cutOut):
        self.filterId = filterId
        self.cutIn = cutIn
        self.cutOut = cutOut

        self.channelId = None
        self.filterSetId = None
        self.type = None
        self.dichroicId = None
        self.dichroic = None

    def __repr__(self):  # TODO This might need to be modified. Currently only for testing purpose.
        return '{};{};{};{}-{}'.format(self.filterId, self.channelId, self.dichroic, self.cutIn, self.cutOut)

    def __eq__(self, other):
        return repr(self) == repr(other)

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
        return '{}-{}'.format(self.cutIn, self.cutOut)

    def getDichroic(self):
        return self.dichroic