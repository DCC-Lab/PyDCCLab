import os
import fnmatch
import imageAnalysis.cziUtil as czi
from tifffile import xml2dict


def findAllCZI(path):
    print('Walking the directory...')
    allCZIs = []
    for root, directories, files in os.walk(os.path.normpath(path)):
        for file in files:
            if fnmatch.fnmatch(file, '*.czi'):
                allCZIs.append([file, os.path.join(root, file)])
    print('...Done! ' + str(len(allCZIs)) + ' files found!')
    return allCZIs

'''
def exportListToCSV(list):
    filename = 'list.csv'
    with open(filename, 'w') as file:

        file.write(CreateCSVHeader(cur))

        for row in cur.execute('SELECT * FROM ' + str(table)):
            line = ""
            for cell in row:
                line += str(cell) + ","
            line = str(line)[:-1] + "\n"
            file.write(line)
        file.close()
        cur.close()
        conn.close()
'''

if __name__ == '__main__':
    # Image Document et Metadata pourraient etre ignorer.
    czipath = 'testCziFile.czi'
    image = czi.readCziImage(czipath)
    metadata = czi.extractMetadataFromCziFileObject(image)
    open('test.txt', 'w').write(metadata)
    data = xml2dict(metadata)
    print(data)
    sousdata = data['ImageDocument']
    print(sousdata)
    soussousdata = sousdata['Metadata']
    print(soussousdata)
    keys = []
    for line in soussousdata:
        keys.append(line)
    for key in keys:
        print(soussousdata[key])

    #CZIs = findAllCZI('P:\\injection AAV\\résultats bruts')


    #for file in os.listdir('P:\injection AAV\S58_AAV595.numbers'):
    #    if fnmatch.fnmatch(file, '*.jpg'):
    #        print(file)
    '''
    # Example code
    some_dir = '/'
    ignore_list = ['*.tmp', 'tmp/', '*.py']
    for dirname, _, filenames in os.walk(some_dir):
        for filename in filenames:
            should_ignore = False
            for pattern in ignore_list:
                if fnmatch.fnmatch(filename, pattern):
                    should_ignore = True
            if should_ignore:
                print ('Ignore', filename)
                continue

    # Simplified loop
    for dirname, _, filenames in os.walk(some_dir):
        for filename in filenames:
            if any(fnmatch.fnmatch(filename, pattern) for pattern in ignore_list):
                print('Ignore', filename)
                continue

    # Other method
    files = [f for f in os.listdir('P:/') if re.match(r'*.czi', f)]
    '''

