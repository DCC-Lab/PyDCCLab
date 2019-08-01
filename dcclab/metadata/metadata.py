from .cziMetadata import CZIMetadata
from .csvMetadata import CSVMetadata
from .xlsxMetadata import XLSXMetadata
from .rawMetadata import RAWMetadata
import os
try:
    import deprecated
except:
    exit("pip install deprecated")


class Metadata:
    # Supported research groups.
    supportedResearchGroup = ['POM', 'PDK']

    # Supported classes and formats for POM.
    pomSupportedClasses = [CZIMetadata, CSVMetadata]
    pomSupportedFormats = ['CZI', 'CSV']

    # Supported classes and formats for PDK.
    pdkSupportedClasses = [XLSXMetadata, RAWMetadata]
    pdkSupportedFormats = ['XLSX', 'RAW']

    supportedClasses = [CZIMetadata, CSVMetadata, XLSXMetadata, RAWMetadata]
    supportedFormats = ['CZI', 'CSV', 'XLSX', 'RAW']

    def __init__(self, path: str):
        if path is not None:
            if not os.path.exists(path):
                raise ValueError("Cannot load '{0}': file does not exist".format(path))
            self.path = path
            self.__fileObject = self.validateDataFile()
            if self.__fileObject is None:
                raise TypeError("Cannot read '{0}': not a recognized format ({1})".format(self.path, Metadata.supportedFormats))
        else:
            self.path = None
            self.__fileObject = None

    def validateDataFile(self):
        researchGroup = self.findResearchGroup(self.path)
        if researchGroup == 'POM':
            for supportedClass in Metadata.pomSupportedClasses:
                try:
                    fileObject = supportedClass(self.path)
                    return fileObject
                except:
                    continue
            return None
        elif researchGroup == 'PDK':
            for supportedClass in Metadata.pdkSupportedClasses:
                try:
                    fileObject = supportedClass(self.path)
                    return fileObject
                except:
                    continue
            return None
        else:
            return None

    def findResearchGroup(self, path: str):
        basename = os.path.basename(path)
        if basename == '':
            return False
        elif basename in Metadata.supportedResearchGroup:
            return basename
        else:
            return self.findResearchGroup(os.path.dirname(path))

    @property
    def metaType(self):
        fileType = type(self.__fileObject)
        if fileType == CZIMetadata:
            return 'CZI'
        elif fileType == CSVMetadata:
            return 'CSV'
        elif fileType == XLSXMetadata:
            return 'XLSX'
        elif fileType == RAWMetadata:
            return 'RAW'
        else:
            return None

    @property
    def metadata(self) -> dict:
        if isinstance(self.__fileObject, CZIMetadata):
            return self.__fileObject.asDict().get('metadata')
        elif isinstance(self.__fileObject, CSVMetadata) or isinstance(self.__fileObject, XLSXMetadata):
            return self.__fileObject.asDict
        else:
            return {}

    @property
    def channels(self) -> dict:
        if isinstance(self.__fileObject, CZIMetadata):
            return self.__fileObject.asDict().get('channels')
        else:
            return {}

    @property
    def keys(self) -> dict:
        if isinstance(self.__fileObject, CZIMetadata) or isinstance(self.__fileObject, CSVMetadata) or \
                isinstance(self.__fileObject, XLSXMetadata):
            return self.__fileObject.keys
        else:
            return {}
