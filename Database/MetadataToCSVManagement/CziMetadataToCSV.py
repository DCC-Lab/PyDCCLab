from metadata import Metadata as mtdt
import reader as rdr
import os
# We want to take a metadata object or list of metadata objects with their attributes.
# We want to extract all of he relevant information.
# We want to put it in a csv.file.
# That CSV file can then be read by other scripts to get added to the database relevant table.

if __name__ == '__main__':
    # Setup for tests
    directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    path = os.path.join(directory, 'testData')
    metadata = rdr.getMetadataFromCzis(path)

    metafile = open('meta.csv', 'w+')
    channelfile = open('channel.csv', 'w+')

    metaKeys = ['name', 'mouse_id', 'path', 'microscope', 'objective', 'x_size', 'y_size', 'x_scale', 'y_scale',
                'x_scaled', 'y_scaled', 'vectors']
    channelKeys = ['entry_id', 'channel_id', 'channel_name', 'ex_wavelength_filter', 'em_wavelength_filter',
                   'beamsplitter', 'reflector', 'contrast_method', 'light_source', 'light_source_intensity', 'dye_name',
                   'channel_color', 'ex_wavelength', 'em_wavelength', 'effective_na', 'imaging_device',
                   'camera_adapter', 'exposure_time', 'binning_mode']

    # Setting up the headers
    metaHeader = ''
    for key in metaKeys:
        metaHeader += key + ','
    metaHeader.rstrip(',')
    metafile.write(metaHeader)

    channelHeader = ''
    for key in channelKeys:
        channelHeader += key + ','
    channelHeader.rstrip(',')
    channelfile.write(channelHeader)

    # Getting the dictionaries out of the metadata objects.
    for entry in metadata:
        metaKeys = []
        for key, value in entry.exportDataAsDict().items():
            metaKeys.append(key)

        channels = entry.getChannels()
        for channel in channels:
            channelKeys = []
            for key, value in channel.exportDataAsDict().items():
                channelKeys.append(key)
            print(channelKeys)
        print(metaKeys)

    metafile.close()
    channelfile.close()
    #os.remove('meta.csv')
    #os.remove('channel.csv')
