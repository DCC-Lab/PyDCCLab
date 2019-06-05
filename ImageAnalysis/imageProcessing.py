import DCCImagesFromFiles
import DCCImageCollection

cziImages = DCCImagesFromFiles.DCCImagesFromCZIFile(
    r"A:\injection AAV\résultats bruts\AAV\AAV498AAV455\AAV498AAV455_S95\AAV498-455_S95_C-09.czi")
cziImages.showImages()
image1 = cziImages[0]
image2 = cziImages[1]
image3 = cziImages[2]
image3.getAdaptiveThresholdingMedian().showImage()
#image3.getEntropyFiltering(3)
print(image1.getMaximumIntensityPixels())
isodata = image1.getIsodataThresholding()
xDeriv = image2.getXAxisDerivative()
otsu_connected = image2.getOtsuThresholding().getConnectedComponents()[0]
DCCImageCollection.DCCImageCollection([image1, isodata]).showImages()
DCCImageCollection.DCCImageCollection([image2, xDeriv]).showImages()
DCCImageCollection.DCCImageCollection([image2, otsu_connected]).showImages(False)
