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


def read_czi_file(filename):
    """
    Function that read a .czi file.
    :param filename: Name of the file.
    :return: CziFile object (from czifile package). The file must be closed at the end of the process.
    See close() function below.
    """
    czi = czifile.CziFile(filename)
    return czi


def close(czi_object):
    """
    Function that closes a CziFile instance object. It must be closed according to the CziFile documentation.
    :param czi_object: The CziFile object to be closed
    :return: Nothing
    """
    czi_object.close()


def extract_metadata(czi_object, save_file_name=None):
    """
    Function that raeds the metadata form a CziFile object
    :param czi_object: The CziFile object
    :param save_file_name: Name of the file that is used to save the metadata (XML file). If None (default), doesn't
    save the metadata.
    :return: The metadata in XML format.
    """
    meta = czi_object.metadata
    if save_file_name is not None:
        file_xml = open("{}.xml".format(save_file_name), "w")
        file_xml.write(meta)
        file_xml.close()
    return meta


def get_array_from_czi_image(czi_object):
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

    :param czi_object: The CziFile object
    :return: Numpy array representing the CziFile/image
    """
    images_array = czi_object.asarray()
    return images_array


def get_images_from_czi_image(czi_object):
    """
    Function that returns the images from a czi file object, with every channel.
    :param czi_object: The CziFile object
    :return: Numpy array containing the images
    """
    array_return = []
    subblocks_iter = czi_object.subblocks()
    for iterator in subblocks_iter:
        array_return.append(np.squeeze(iterator.data()))
    return np.array(array_return)


def show_images_from_czi_image(czi_object):
    """
    Function that shows the images in a czi file object. The function shows them one by one, no subplots.
    :param czi_object: CziFile object
    :return: Numpy array of matplotlib.image.AxesImage (each of the matplotlib.image.AxesImage of the initial image)
    """
    subblocks_iter = czi_object.subblocks()
    images_return = []
    for iterator in subblocks_iter:
        image = (np.squeeze(iterator.data()))
        image_return = plt.imshow(image)
        images_return.append(image_return)
        plt.show()
    return np.array(images_return)


def save_image_array_to_TIFF(image_array, filename=None):
    """
    Function that saves every image in an array to a TIFF file.
    :param image_array: Array of images to be saved
    :return: Nothing
    """
    if len(image_array) == 0:
        raise ValueError("Image array empty.")
    i = 0
    for image in image_array:
        i += 1
        if filename is not None:
            tifffile.imwrite("{}_{}.tif".format(filename, i), image)
        else:
            tifffile.imwrite("array2tiff_{}.tif".format(i), image)


if __name__ == '__main__':
    czi = read_czi_file("test_czi.czi")
    image = get_images_from_czi_image(czi)[0]
    close(czi)
    print(image)
    image_2 = np.array(image, dtype=np.float32)
    print(image_2)
    image_3 = image == image_2
    print(np.where(image_3 is False))
