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


def xmlParser(cziFile, filter=None):  # TODO filter
    try:
        # We create a temporary XML file to use in iterparse.
        image = czi.readCziImage(cziFile)
        czi.extractMetadataFromCziFileObject(image, 'temp')

        # TODO searchResults = []
        iterable = cet.iterparse('temp.xml', events=('start', 'end'))
        iterator = iter(iterable)

        event, root = iterator.__next__()

        for event, elem in iterator:
            if event == 'end':  # and element.tag == filter:
                # searchResults.append([elem.tag, elem.text])
                print(elem.tag, elem.text)
                elem.clear()
                root.clear()
        # TODO return searchResults
    except cet.ParseError as error:
        return error
    finally:
        # In all cases, we delete the xml file.
        os.remove('temp.xml')


if __name__ == '__main__':
    xmlParser('testCziFile.czi')
