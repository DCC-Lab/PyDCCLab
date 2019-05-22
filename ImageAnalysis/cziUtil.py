"""
Python script containing utility functions to be used for handling .czi images.

These functions are supposed to work with the CZI format files used with POM images.
Since Python doesn't offer a lot of libraries (and those available are not well documented (some are just not) or
requiring weird stuff) to play with that format, I needed to do a little file so that it's easier to breath in the
.czi jungle.

The main object used in this file is the CziFile object from the czifile library

Hope it works correctly!
"""
"""
First, let's import the useful stuff
"""
import czifile
import numpy as np
import matplotlib.pyplot as plt
import tifffile
import xml.etree.ElementTree as ET


def readCziImage(filename):
    """
    Function that read a .czi file.
    :param filename: Name of the file.
    :return: CziFile object (from czifile package). The file must be closed at the end of the process.
    See close() function below.
    """
    czi = czifile.CziFile(filename)
    return czi


def closeCziFileObject(cziObject):
    """
    Function that closes a CziFile instance object. It must be closed according to the CziFile documentation.
    :param cziObject: The CziFile object to be closed
    :return: Nothing
    """
    cziObject.close()


def extractMetadataFromCziFileObject(cziObject, saveFileName=None):
    """
    Function that raeds the metadata form a CziFile object
    :param cziObject: The CziFile object
    :param saveFileName: Name of the file that is used to save the metadata (XML file). If None (default), doesn't
    save the metadata.
    :return: The metadata in XML formated string.
    """
    meta = cziObject.metadata
    if saveFileName is not None:
        file_xml = open("{}.xml".format(saveFileName), "w")
        file_xml.write(meta)
        file_xml.close()
    return meta


def getArrayFromCziFileObject(cziObject):
    """
    Function that transform a CziFile object into a numpy array. WARNING: The returning numpy array is tricky to use.
    It is multi-dimensional (like 5-6 dimensions) and each of the dimensions meaning are not well explained.

    This functions is not the best to get every image, since some mosaic image are recomposed. See below for another
    function that returns an array of every image.

    Example:

    czi = read_czi_file("filename.czi")
    array_czi = get_array_from_czi_image(czi)
    print(czi.shape)
    ->(1, 1, 2, 9585, 12690, 1)

    The first two dimensions don't seem to be important.
    The third dimensions seems to represent the number of images in the file
    The fourth and fifth dimensions are de size of the image.
    The last dimension is not important.

    When printing the array: it seems that the non important dimensions are just "wraping"
    the array, like:
    [[[[[x1]
        [x2]
        ...
        [xn]]
        [[y1]
         [y2]
        ...
        [yn]]]]]

    Arrays can have different dimensions, depending on the number of channel or z-plane in the original czi file.

    :param cziObject: The CziFile object
    :return: Numpy array representing the CziFile/image
    """
    images_array = cziObject.asarray()
    return images_array


def getImagesFromCziFileObject(cziObject):
    """
    Function that returns the images from a czi file object, with every channel.
    :param cziObject: The CziFile object
    :return: Numpy array containing the images
    """
    arrayReturn = []
    subblocksIters = cziObject.subblocks()
    for iterator in subblocksIters:
        arrayReturn.append(np.squeeze(iterator.data()))
    return np.array(arrayReturn)


def showImagesFromCziFileObject(cziObject):
    """
    Function that shows the images in a czi file object. The function shows them one by one, no subplots.
    :param cziObject: CziFile object
    :return: Numpy array of matplotlib.image.AxesImage (each of the matplotlib.image.AxesImage of the initial image)
    """
    subblocksIters = cziObject.subblocks()
    imagesReturn = []
    for iterator in subblocksIters:
        image = (np.squeeze(iterator.data()))
        image_return = plt.imshow(image)
        imagesReturn.append(image_return)
        plt.show()
    return np.array(imagesReturn)


def getFormatedMetadata(metadata):
    """
    Function that formats the XMl-string metadata in a more convenient way, easier to read and to browse.
    :param metadata: XML formatted string containing the metadata.
    :return: String containing the formatted metadata
    """
    returnString = ""
    try:
        tree = ET.ElementTree(ET.fromstringlist(metadata))
        for iterator in tree.iter():
            returnString += "{} : {}\n".format(iterator.tag, iterator.text)
    except ET.ParseError as exception:
        raise ValueError("Exception with string \"{}\"; {}".format(metadata, exception.msg))
    return returnString


def saveImagesToTIFF(imageArray, filename=None):
    """
    Function that saves every image in an array to a TIFF file.
    :param imageArray: Array of images to be saved. If the array is empty, nothing is done.
    :param filename: The file name to save the new tiff image. If None (default), a default name is given.
    :return: bool. True if the image is saved, False if nothing is done.
    """
    isSaved = False
    if len(imageArray) != 0:
        isSaved = True
        i = 0
        for image in imageArray:
            i += 1
            if filename is not None:
                tifffile.imwrite("{}_{}.tif".format(filename, i), image)
            else:
                tifffile.imwrite("array2tiff_{}.tif".format(i), image)
    return isSaved
