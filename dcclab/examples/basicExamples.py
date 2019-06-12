"""
Basic image handling with DCCImages and DCCImageCollection


DCCImage:

DCCImage is a class used to handle a certain type of arrays and use them as images. It contains some basic image
analysis and processing tools, such as grayscale conversion, image splitting based on color channels, displaying the
histogram of an image, ...

It contains also some more complex processing tools, like convolution between the image and another matrix, applying an
entropy filter and a few thresholding methods (Otsu, isodata and adaptive ones). The goal of this class is to have some
processing methods all at the same place and independant of the file used to store the image. If the image format is
JPEG, PNG, or CZI, it can be read and converted to DCCImage quite simply. Then, one can apply filtering or thresholding
methods without modifying the source image and without having to search in different libraries to be able to modify the
image.


DCCImageCollection:

DCCImageCollection is a class that can hold many DCCImage instances. Then, they can be easily accessed and processed
because they are DCCImage objects.
"""

"""
First of all, let's import the file that can read images:
"""
import DCCImagesFromFiles

"""
Then, let's read images from a czi file and display them on screen.
"""
cziImages = DCCImagesFromFiles.DCCImagesFromCZIFile(
    r"A:\injection AAV\résultats bruts\AAV\AAV493AAV498\AAV493AAV498_S51\AAV493AAV498_S51\S51-06.czi", 3)
cziImages.showImages(showInGray=True)


"""
We can access images from the collection by the use of a function or by the use of []
"""

image01 = cziImages[0]
image02 = cziImages.getImageAtIndex(1)
image03 = cziImages[-1]

"""
We can now extract basic stats about images:
"""
# Get the number of channel in the image (1 if gray, 3 if RGB)
print(image01.getNumberOfChannel())
# Get the average value of the pixels
print(image02.getAverageValueOfImage())
# Get Shannon entropy of the image https://en.wiktionary.org/wiki/Shannon_entropy
print(image03.getShannonEntropyOfImage(base=2))

"""
Image histograms can also be really pertinent when analysing images
"""
# Let's display the histogram of the first image:
image01.displayGrayscaleHistogram(normed=True)

# It is

"""
We can also apply a filter on the image
"""
# Apply a gaussian filter of sigma = 1.78
gaussianFilter = image01.getGrayGaussianFiltering(sigma=1.78)
# Apply an entropy filter of size = 4
entropyFilter = image02.getEntropyFiltering(filterSize=4)
# Apply Y axis derivative
yAxisDeriv = image03.getYAxisDerivative()

"""
We can then threshold images
"""
otsuThresh = image02.getOtsuThresholding()
isodataThresh = image02.getIsodataThresholding()

"""
It is possible to use morphological techniques: "close" to fill small holes or "open" to remove small objects
"""
binOpened = otsuThresh.getBinaryOpening(windowSize=6)
binClosed = isodataThresh.getBinaryClosing(windowSize=7)

"""
We can now display all the images we obtained.
Let's import a class that allows us to display (and handle) multiple DCCImage instances.
"""
import DCCImageCollection

image01Related = DCCImageCollection.DCCImageCollection([image01, gaussianFilter])
image02Related = DCCImageCollection.DCCImageCollection(
    [image02, entropyFilter, otsuThresh, isodataThresh, binOpened, binClosed])
image03Related = DCCImageCollection.DCCImageCollection([image03, yAxisDeriv])

image01Related.showImages(False)
image02Related.showImages(False)
image03Related.showImages()
