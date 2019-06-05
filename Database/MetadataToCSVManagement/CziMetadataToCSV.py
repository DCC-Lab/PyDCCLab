from metadata import Metadata as mtdt
import reader as rdr
import os
# We want to take a metadata object or list of metadata objects with their attributes.
# We want to extract all of he relevant information.
# We want to put it in a csv.file.
# That CSV file can then be read by other scripts to get added to the database relevant table.

if __name__ == '__main__':
    # Setup for tests
    #directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    #path = os.path.join(directory, 'testData')
    #path = 'P:\\injection AAV\\résultats bruts\\2019-01-23'
    path = 'P:\\'
    metadata = rdr.getMetadataFromCzis(path)

    metafile = open('meta.csv', 'w+', encoding='UTF-8')
    channelfile = open('channel.csv', 'w+', encoding='UTF-8')

    metaKeys = ['name', 'mouse_id', 'path', 'microscope', 'objective', 'x_size', 'y_size', 'x_scale', 'y_scale',
                'x_scaled', 'y_scaled', 'vectors']
    metaTypes = ['TEXT', 'INT', 'TEXT', 'TEXT', 'TEXT', 'INT', 'INT', 'INT', 'INT', 'INT', 'INT', 'TEXT']
    channelKeys = ['file_id', 'channel_id', 'channel_name', 'ex_wavelength_filter', 'em_wavelength_filter',
                   'beamsplitter', 'reflector', 'contrast_method', 'light_source', 'light_source_intensity', 'dye_name',
                   'channel_color', 'ex_wavelength', 'em_wavelength', 'effective_na', 'imaging_device',
                   'camera_adapter', 'exposure_time', 'binning_mode']
    channelTypes = ['TEXT', 'TEXT', 'TEXT', 'TEXT', 'TEXT', 'INT', 'TEXT', 'TEXT', 'TEXT', 'TEXT', 'TEXT', 'TEXT', 'INT',
                    'INT', 'INT', 'TEXT', 'TEXT', 'INT', 'TEXT']

    # Setting up the headers
    metaHeader = ''
    for key in metaKeys:
        metaHeader += key + ','
    metaHeader = metaHeader.rstrip(',')
    metaHeader += '\n'
    metafile.write(metaHeader)

    metaLine = ''
    for type in metaTypes:
        metaLine += type + ','
    metaLine = metaLine.rstrip(',')
    metaLine += '\n'
    metafile.write(metaLine)

    channelHeader = ''
    for key in channelKeys:
        channelHeader += key + ','
    channelHeader = channelHeader.rstrip(',')
    channelHeader += '\n'
    channelfile.write(channelHeader)

    channelLine = ''
    for type in channelTypes:
        channelLine += type + ','
    channelLine = channelLine.rstrip(',')
    channelLine += '\n'
    channelfile.write(channelLine)

    # Getting the dictionaries out of the metadata objects.
    for entry in metadata:
        dictioMeta = entry.exportDataAsDict()
        data = ''
        for key in metaKeys:
            data += str(dictioMeta[key]) + ','
        data = data.rstrip(',') + '\n'
        metafile.write(data)

        channels = entry.getChannels()
        for channel in channels:
            chnlData = ''
            dictioChnl = channel.exportDataAsDict()
            for key in channelKeys:
                chnlData += str(dictioChnl[key]) + ','
            chnlData = chnlData.rstrip(',') + '\n'
            channelfile.write(chnlData)

    metafile.close()
    channelfile.close()
    #os.remove('meta.csv')
    #os.remove('channel.csv')
