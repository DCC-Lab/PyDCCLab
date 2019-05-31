import cziUtil as czi
import metadata as mtdt
import re


if __name__ == '__main__':
    # We find all of the czi files in a given folder.
    allCziFiles = czi.findAllCziFiles('P:\\injection AAV\\résultats bruts\\2019-01-23')

    # We extract the metadata from the files and create a list of objects containing that metadata.
    mdata = []
    for cziFile in allCziFiles:
        newMData = mtdt.Metadata(cziFile[1], cziFile[0])
        newMData.setAttributesFromXml()
        mdata.append(newMData)

    # Small function to print all of the files name, find matching components and print them.
    """
    for m in mdata:
        name = str(m.getName()).split('_')
        vectors = []
        mouse = ''
        for n in name:
            if re.match(r'^\w{3}\d{3}', n):
                vectors.append(re.match(r'^\w{3}\d{3}', n).group())
            if re.match(r'^\w\d{3}', n):
                mouse = re.match(r'^\w\d{3}', n).group()
        print(name, vectors, mouse)
        
        # Small function to print export all of the channel's data.
        '''
        for c in m.getChannels():
            print(c.exportDataAsDict())
        '''
    """