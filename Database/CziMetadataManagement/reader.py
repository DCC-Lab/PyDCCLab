from metadata import Metadata as mtdt
import cziUtil as czi
import re


def getMetadataFromCzis(path):
    cziFiles = czi.findAllCziFiles(path)
    metadata = getMetadataFromFiles(cziFiles)
    return metadata


def getMetadataFromFiles(cziFiles):
    metadataObjects = []
    for cziFile in cziFiles:
        newMetadata = mtdt(cziFile[1], cziFile[0])
        newMetadata.setAttributesFromXml()
        getMetadataFromFilesName(newMetadata)
        metadataObjects.append(newMetadata)
    return metadataObjects


def getMetadataFromFilesName(metadata):
    name = metadata.getName().split('_')
    vectors = []
    mouseId = ''
    for cell in name:
        if re.match(r'^\w{3}\d{3}', cell):
            vectors.append(re.match(r'^\w{3}\d{3}', cell).group())
        if re.match(r'^\w\d{3}', cell):
            mouseId = re.match(r'^\w\d{3}', cell).group()[1:]
    metadata.setMouseId(mouseId)
    metadata.setVectors(vectors)


if __name__ == '__main__':
    '''
    # We find all of the czi files in a given folder.
    allCziFiles = czi.findAllCziFiles('P:\\injection AAV\\résultats bruts\\2019-01-23')

    # We extract the metadata from the files and create a list of objects containing that metadata.
    mdata = []
    for cziFile in allCziFiles:
        newMData = mtdt(cziFile[1], cziFile[0])
        newMData.setAttributesFromXml()
        mdata.append(newMData)

    # Small function to print all of the files name, find matching components and print them.
    for m in mdata:
        name = str(m.getName()).split('_')
        vectors = []
        mouseId = ''
        for n in name:
            if re.match(r'^\w{3}\d{3}', n):
                vectors.append(re.match(r'^\w{3}\d{3}', n).group())
            if re.match(r'^\w\d{3}', n):
                mouseId = re.match(r'^\w\d{3}', n).group()[1:]
        m.setMouseId(mouseId)
        m.setVectors(vectors)
        print('-Metadata : ', m.exportDataAsDict())

        # Small function to print export all of the channel's testData.
        for c in m.getChannels():
            print('---Channel in Metdata : ', c.exportDataAsDict())
    '''
    path = 'P:\\injection AAV\\résultats bruts\\2019-01-23'
    metadatas = getMetadataFromCzis(path)

    for metadata in metadatas:
        print('THIS IS METADATA RELATED TO THE FILE : ', metadata.getName())
        for key, value in metadata.exportDataAsDict().items():
            print(key, " : ", value)
        print('ITS CHANNELS ARE : ')
        for channel in metadata.getChannels():
            print(channel.channelName)
            for key, value in channel.exportDataAsDict().items():
                print(key, " : ", value)
