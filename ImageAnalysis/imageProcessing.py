import DCCImagesFromFiles
import cziUtil

path = cziUtil.findAllCziFiles(r"A:\injection AAV\résultats bruts\AAV")
print(len(path))