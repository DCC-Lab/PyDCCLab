'''
THIS FILE IS OBSOLETE.
SOME OF THE CODE MIGHT BE USEFUL LATER SO THE FILE IS KEPT FOR NOW.
ONCE THERE IS NO MORE USE FOR THE CODE, IT SHOULD BE DELETED.
'''
from dcclab import findAllCziFiles
from dcclab.metadata.cziMetadata.cziMetadata import CZIMetadata as mtdt
from dcclab.metadata import Metadata as imgMtdt
import os
import fnmatch


def createCSVFromCZIMetadata(path):
    metaFile = open('meta.csv', 'w+', encoding='UTF-8')
    channelFile = open('channel.csv', 'w+', encoding='UTF-8')
    setupCSVHeaders(metaFile, channelFile)
    cziPathsAndNames = getAllCzisFromFolder(path)

    for cziFile in cziPathsAndNames:
        writeMetadataInCSV(metaFile, channelFile, cziFile)

    metaFile.close()
    channelFile.close()


def writeMetadataInCSV(metaFile, channelFile, cziFile):
    metaKeys = ['name', 'mouse_id', 'injection_site', 'viral_vectors', 'microscope', 'objective', 'x_size', 'y_size',
                'x_scale', 'y_scale', 'x_scaled', 'y_scaled', 'tags', 'path']
    channelKeys = ['file_id', 'channel_id', 'channel_name', 'ex_wavelength_filter', 'em_wavelength_filter',
                   'beamsplitter', 'reflector', 'contrast_method', 'light_source', 'light_source_intensity', 'dye_name',
                   'channel_color', 'ex_wavelength', 'em_wavelength', 'effective_na', 'imaging_device',
                   'camera_adapter', 'exposure_time', 'binning_mode']
    try:
        newMtdt = getMetadataFromCzi(cziFile[1], cziFile[0])
        dictioMeta = newMtdt.asDict()
        data = ''
        for key in metaKeys:
            data += str(dictioMeta[key]) + ','
        data = data.rstrip(',') + '\n'
        metaFile.write(data)

        for channel in newMtdt.channels:
            chnlData = ''
            dictioChnl = channel.asDict()
            for key in channelKeys:
                chnlData += str(dictioChnl[key]) + ','
            chnlData = chnlData.rstrip(',') + '\n'
            channelFile.write(chnlData)
    except Exception:
        pass


def setupCSVHeaders(metaFile, channelFile):
    writeMetaFileHeader(metaFile)
    writeChannelFileHeader(channelFile)


def writeMetaFileHeader(metaFile):
    metaKeys = ['name', 'mouse_id', 'injection_site', 'viral_vectors', 'microscope', 'objective', 'x_size', 'y_size',
                'x_scale', 'y_scale', 'x_scaled', 'y_scaled', 'tags', 'path']
    metaTypes = ['TEXT', 'INT', 'TEXT', 'TEXT', 'TEXT', 'TEXT', 'INT', 'INT', 'INT', 'INT', 'INT', 'INT', 'TEXT',
                 'TEXT']

    metaHeader = ''
    for key in metaKeys:
        metaHeader += key + ','
    metaHeader = metaHeader.rstrip(',')
    metaHeader += '\n'
    metaFile.write(metaHeader)

    metaLine = ''
    for type in metaTypes:
        metaLine += type + ','
    metaLine = metaLine.rstrip(',')
    metaLine += '\n'
    metaFile.write(metaLine)


def writeChannelFileHeader(channelFile):
    channelKeys = ['file_id', 'channel_id', 'channel_name', 'ex_wavelength_filter', 'em_wavelength_filter',
                   'beamsplitter', 'reflector', 'contrast_method', 'light_source', 'light_source_intensity', 'dye_name',
                   'channel_color', 'ex_wavelength', 'em_wavelength', 'effective_na', 'imaging_device',
                   'camera_adapter', 'exposure_time', 'binning_mode']
    channelTypes = ['TEXT', 'TEXT', 'TEXT', 'TEXT', 'TEXT', 'INT', 'TEXT', 'TEXT', 'TEXT', 'TEXT', 'TEXT', 'TEXT',
                    'INT', 'INT', 'INT', 'TEXT', 'TEXT', 'INT', 'TEXT']

    channelHeader = ''
    for key in channelKeys:
        channelHeader += key + ','
    channelHeader = channelHeader.rstrip(',')
    channelHeader += '\n'
    channelFile.write(channelHeader)

    channelLine = ''
    for type in channelTypes:
        channelLine += type + ','
    channelLine = channelLine.rstrip(',')
    channelLine += '\n'
    channelFile.write(channelLine)


def getAllCzisFromFolder(path):
    print('Begining to search for .czi files in folder : {}'.format(path))
    try:
        cziPathsAndNames = findAllCziFiles(path)
        print(len(cziPathsAndNames), ' files were found!')
        return cziPathsAndNames
    except Exception as err:
        print('An unforseen error occured : ', type(err), err)


def getMetadataFromCzi(name, path):
    try:
        print('Proccessing file : {}'.format(name))
        newMetadata = mtdt(name, path)
        return newMetadata
    except OSError:
        print('An error occured. Could not pocess file : {}'.format(name))
        print(path)
        print('Path is invalid or the file was already open.')
    except KeyError:
        print('An error occured. Could not pocess file : {}'.format(name))
        print(path)
        print('A key attribute in the xml was not valid or could not be found.')
    except AttributeError:
        print('An error occured. Could not pocess file : {}'.format(name))
        print(path)
        print('An entry in the XML could not be reached or returned none.')


def findFiles(directory, extension) -> list:
    filesFound = []
    for root, directories, files in os.walk(os.path.normpath(directory)):
        for file in files:
            if fnmatch.fnmatch(file, extension):
                filesFound.append(os.path.join(root, file))
    return filesFound


if __name__ == '__main__':
    extension = '*.czi'
    #path = 'P:\\injection AAV\\résultats bruts'
    path = 'P:\\injection AAV\\résultats bruts\\AAV\\AAV498AAV455'
    #createCSVFromCZIMetadata(path)
    #print('Finished')
    for file in findFiles(path, extension):
        object = imgMtdt(file)
        print(object.getMetadata)
        for key, value in object.getChannels.items():
            print(value)
