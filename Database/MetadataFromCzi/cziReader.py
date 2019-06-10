from cziMetadata import Metadata as mtdt
import cziUtil as czi


def getAllCzisFromFolder(path):
    print('Begining to search for .czi files in folder : {}'.format(path))
    try:
        cziPathsAndNames = czi.findAllCziFiles(path)
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


def getMetadataFromCzis(path):
    cziFiles = czi.findAllCziFiles(path)
    allMdata = []
    for cziFile in cziFiles:
        try:
            print('Proccessing file : {}'.format(cziFile[0]))
            allMdata.append(createMetadataObjectFromCziFile(cziFile))
        except Exception as err:
            print('En error occured. Could not pocess file : {}'.format(cziFile[0]))
            print(cziFile[1])
            print('See below : ')
            print(type(err), err)
            #input('Press a key to proceed...')
    return allMdata


def createMetadataObjectFromCziFile(cziFile):
    newMdata = mtdt(cziFile[1], cziFile[0])
    return newMdata
