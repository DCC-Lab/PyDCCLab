from dcclab.database import *
import re

db = SpectraDB("mysql://127.0.0.1/root@labdata")

rootDir = "/Users/dccote/Desktop/PegahAndAlexExperiment"

dateAcquired = "2022-05-10"

db.createNewDataset(
    datasetId="DRS-001",
    id1Label="region",
    id2Label="sampleId",
    id3Label="distance",
    id4Label=None,
    description="""
Experiments done by Pegah Eslami and Alexandre Bedard, week of May 8th 2022.
Diffuse reflectance spectra are acquired with an optical fiber at different distances 
from brain slices.  Distance is in millimeters. The regions are identified simply as 
white or grey, and several different points (identified with sampleId) are acquired 
and correspond to different sites on the brain slice.
""",
    projectId="dbs"
)

for currentPath, subdirs, files in os.walk(rootDir):
    for file in files:
        # Filenames must look like this: Grey1_5.54mm.txt
        match = re.search(r"(.+?)(\d+)_(.+?)mm\.txt", file)
        if match is not None:
            # We have a valid spectral file, where all the information is in the filename.
            region = match.group(1)
            sampleId = match.group(2)
            distance = match.group(3)

            spectrumId = "{0}-{1}-{2:04d}-{3:05.0f}".format(
                datasetId, region.upper(), int(sampleId), float(distance) * 1000
            )

            filePath = os.path.join(currentPath, file)
            x, y, userInfo = db.readOceanInsightFile(filePath)

            try:
                db.beginTransaction()

                db.execute(
                    """
                    insert into spectra (datasetId, spectrumId, id1, id2, id3, 
                    labdataPath, dateAcquired, userInfo) values(%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        datasetId,
                        spectrumId,
                        region,
                        sampleId,
                        distance,
                        file,
                        dateAcquired,
                        userInfo,
                    ),
                )
                db.insertSpectralData(spectrumId, x, y)

                db.endTransaction()

            except Exception as err:
                print(err)
                db.rollbackTransaction()
