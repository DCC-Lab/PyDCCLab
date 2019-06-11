class CZIFilter:
    def __init__(self, filterId, root):
        self.filterId = filterId
        self.root = root

        self.filterSetId, self.filterType = self.setFilterSetIdAndType()
        self.cutIn = self.setCutIn()
        self.cutOut = self.setCutOut()
        self.channelId = self.setChannelId()
        self.dichroicId = self.setDichroicId()
        self.dichroic = self.setDichroic()

    def __repr__(self):
        return '{};{};{};{}-{}'.format(self.filterId, self.channelId, self.dichroic, self.cutIn, self.cutOut)

    def __eq__(self, other):
        return repr(self) == repr(other)

    def setFilterSetIdAndType(self):
        try:
            for filterSet in self.root.find('./Metadata/Information/Instrument/FilterSets'):
                if self.filterId == filterSet.find('./EmissionFilters/EmissionFilterRef').attrib['Id']:
                    return filterSet.attrib['Id'], 'Emission'
                elif self.filterId == filterSet.find('./ExcitationFilters/ExcitationFilterRef').attrib['Id']:
                    return filterSet.attrib['Id'], 'Excitation'
        except KeyError:
            return 'Key not found.', 'Key not found.'
        except AttributeError:
            return 'Attribute not found.', 'Attribute not found.'

    def setCutIn(self):
        try:
            return self.root.find('./Metadata/Information/Instrument/Filters/Filter[@Id="{}"]'
                                  '/TransmittanceRange/CutIn'.format(self.filterId)).text
        except AttributeError:
            return 'Attribute not found.'
        except KeyError:
            return 'Key not found.'

    def setCutOut(self):
        try:
            return self.root.find('./Metadata/Information/Instrument/Filters/Filter[@Id="{}"]'
                                  '/TransmittanceRange/CutOut'.format(self.filterId)).text
        except AttributeError:
            return 'Attribute not found.'
        except KeyError:
            return 'Key not found.'

    def setChannelId(self):
        self.setFilterSetIdAndType()
        try:
            for channel in self.root.find('./Metadata/Information/Image/Dimensions/Channels'):
                if channel.find('FilterSetRef').attrib['Id'] == self.filterSetId:
                    return channel.attrib['Id']
        except KeyError:
            return 'Key not found.'
        except AttributeError:
            return 'Attribute not found.'

    def setDichroicId(self):
        try:
            return self.root.find('./Metadata/Information/Instrument/FilterSets/'
                                  'FilterSet[@Id="{}"]/DichroicRef'.format(self.filterSetId)).attrib['Id']
        except KeyError:
            return 'Key not found.'
        except AttributeError:
            return 'Attribute not found.'

    def setDichroic(self):
        try:
            return self.root.find('./Metadata/Information/Instrument/Dichroics/'
                                  'Dichroic[@Id="{}"]/Wavelengths/Wavelength'.format(self.dichroicId)).text
        except AttributeError:
            return 'Attribute not found.'
        except KeyError:
            return 'Key not found.'

    def getType(self):
        return self.filterType

    def getChannelId(self):
        return self.channelId

    def getFilterRange(self):
        return '{}-{}'.format(self.cutIn, self.cutOut)

    def getDichroic(self):
        return self.dichroic