import xml.etree.ElementTree as ET
import os
import fnmatch
import ImageAnalysis.cziUtil as czi
'''
Important informations concerning the .czi file seems to be contained in :
<ImageDocument><Metadata><Information>
<ImageDocument><Metadata><Scaling>
<ImageDocument><Metadata><DisplaySetting>
These are the main branches that should be parsed and from which we should get the relevant data of the experiment.
'''


def findAllCziFiles(path):
    print('Walking the directory...')
    allCZIs = []
    for root, directories, files in os.walk(os.path.normpath(path)):
        for file in files:
            if fnmatch.fnmatch(file, '*.czi'):
                allCZIs.append([file, os.path.join(root, file)])
    print('...Done! ' + str(len(allCZIs)) + ' files found!')
    return allCZIs


def xmlParser(cziFilePath, filter):
    try:
        # We create a temporary XML file to use with iterparse.
        # Going directly through a string didn't work.
        cziImageObject = czi.readCziImage(cziFilePath)
        fullXml = czi.extractMetadataFromCziFileObject(cziImageObject, 'temp_full')

        root = ET.fromstring(fullXml)
        '''
        # Finding SizeX, SizeY, SizeB?, PixelType?
        tags = ['SizeX', 'SizeY', 'SizeB', 'PixelType']
        for data in root.find('./Metadata/Information/Image'):
            if data.tag in tags:
                print(data.tag, data.attrib, data.text)
        '''

        # Finding all the channels, their id and name.
        tags = ['ExcitationWavelength', 'EmissionWavelength', 'DyeId', 'Color', 'Fluor', 'ExposureTime', 'Reflector',
                'IlluminationType']
        for data in root.find('./Metadata/Information/Image/Dimensions/Channels'):
            print(data.attrib['Id'], data.attrib['Name'])
            # Finding all of the relevant channel infos.
            for subdata in data:
                if subdata.tag in tags:
                    print(subdata.tag, subdata.attrib, subdata.text)
                if subdata.tag == 'LightSourcesSettings':
                    intensity = subdata.find('LightSourceSettings/Intensity')
                    print(intensity.tag, intensity.attrib, intensity.text)

        '''
        metadata = extractRelevantDataFromRoot(fullXml)
        print(metadata)
        informationData = extractFromInformation(metadata[0])
        scalingData = extractFromScaling(metadata[1])
        displayData = extractFromDisplaySetting(metadata[2])

        searchResults = []
        iterable = ET.iterparse('temp_full.xml', events=('start', 'end'))
        iterator = iter(iterable)

        event, root = iterator.__next__()
        '''
        '''
        for event, elem in iterator:
            if event == 'end':
                for tag in filter:
                    if elem.tag == tag:
                        searchResults.append([elem.tag, elem.text])
                elem.clear()
                root.clear()
        '''
        #return searchResults
    except ET.ParseError as error:
        return error
    finally:
        # In all cases, we delete the temporary xml files.
        #os.remove('temp_full.xml')
        pass


'''
def extractRelevantDataFromRoot(xmlString):
    relevantTags = ['Information', 'Scaling', 'DisplaySetting']

    data = []
    tree = ET.fromstring(xmlString)

    for branch in tree[0]:
        for tag in relevantTags:
            if branch.tag == tag:
                data.append(branch)
    return data


def extractFromInformation(metadata):
    for elem in metadata:
        print(elem.tag)
    return 0


def extractFromScaling(metadata):
    return 0


def extractFromDisplaySetting(metadata):
    return 0
'''


if __name__ == '__main__':
    filter = ['ExposureTime', 'Intensity', 'ExcitationWavelength', 'EmissionWavelength', 'Reflector',
              'IlluminationType', 'ContrastMethod', 'Color', 'Medium', 'CutIn', 'CutOut', 'Objective']
    results = xmlParser('testCziFile.czi', filter)

    # Some possible tags that could be used.
    '''
    IlluminationType Fluorescence
    DyeMaxEmission 509
    DyeMaxExcitation 488
    DyeId McNamara-Boswell-0828
    DyeDatabaseId 66071726-cbd4-4c41-b371-0a6eee4ae9c5
    
    IlluminationType Fluorescence
    ContrastMethods ReflectedLightFluorescence
    
    ExposureTime 150
    
    IlluminationType Fluorescence
    DyeMaxEmission 610
    DyeMaxExcitation 587
    DyeId McNamara-Boswell-1238
    DyeDatabaseId 66071726-cbd4-4c41-b371-0a6eee4ae9c5
    
    Intensity 58.315789473684
    
    CameraPixelAccuracy
    CameraPixelMaximum
    CameraPixelType
    
    ImagePixelAccuracy
    ImagePixelType
    
    FrameRate
    
    NoiseFilter
    NoiseFilterThreshold
    
    Temperature
    TemperatureState
    
    LEDIntensity
    
    TotalMagnification
    DefaultScalingUnit
    '''
