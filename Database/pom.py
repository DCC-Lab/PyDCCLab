import xml.etree.cElementTree as cet
import os
import fnmatch
import ImageAnalysis.cziUtil as czi


def findAllCZI(path):
    print('Walking the directory...')
    allCZIs = []
    for root, directories, files in os.walk(os.path.normpath(path)):
        for file in files:
            if fnmatch.fnmatch(file, '*.czi'):
                allCZIs.append([file, os.path.join(root, file)])
    print('...Done! ' + str(len(allCZIs)) + ' files found!')
    return allCZIs


def xmlParser(cziFilePath, filter=None):  # TODO filter
    try:
        # We create a temporary XML file to use with iterparse.
        # Going directly through a string didn't work.
        cziImageObject = czi.readCziImage(cziFilePath)
        czi.extractMetadataFromCziFileObject(cziImageObject, 'temp')

        # TODO searchResults = []
        iterable = cet.iterparse('temp.xml', events=('start', 'end'))
        iterator = iter(iterable)

        event, root = iterator.__next__()

        for event, elem in iterator:
            if event == 'end':  # TODO and element.tag == filter:
                # TODO searchResults.append([elem.tag, elem.text])
                print(elem.tag, elem.text)
                elem.clear()
                root.clear()
        # TODO return searchResults
    except cet.ParseError as error:
        return error
    finally:
        # In all cases, we delete the temporary xml file.
        os.remove('temp.xml')


if __name__ == '__main__':
    xmlParser('testCziFile.czi')
