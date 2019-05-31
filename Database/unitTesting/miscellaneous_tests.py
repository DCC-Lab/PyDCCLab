import cziUtil as czi
import metadata as mtdt


if __name__ == '__main__':
    allCziFiles = czi.findAllCziFiles('P:\\injection AAV\\résultats bruts\\2019-01-23')
    print(allCziFiles)

    mdata = []
    for cziFile in allCziFiles:
        newMData = mtdt.Metadata(cziFile[1])
        newMData.setAttributesFromXml()
        mdata.append(newMData)

    for m in mdata:
        print(m)

    print(len(mdata))