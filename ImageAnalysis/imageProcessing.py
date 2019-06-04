import DCCImagesFromFiles

cziImages = DCCImagesFromFiles.DCCImagesFromCZIFile(
    r"A:\injection AAV\résultats bruts\AAV\AAV498AAV455\AAV498AAV455_S95\AAV498-455_S95_C-09.czi")
cziImages.showImages()
image1 = cziImages[0]
image2 = cziImages[1]
image3 = cziImages[2]
print(image1.getMaximumIntensityPixels())
image1.getIsodataThresholding().showImage(True)
image2.getXAxisDerivative().showImage()
image3.getBothDirectionsSobelFiltering().showImage()
