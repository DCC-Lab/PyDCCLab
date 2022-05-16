from .database import *
import numpy as np
import requests
import re


class LabdataDB(Database):
    """
    This is a general database tool to access all information about projects,
    files, and spectral datasets of the DCCLab. The database is on Cafeine3
    and can be accessed with the dcclab username and normal password via a
    secure shell, and then via mysql also with dcclab and the same password.
    The database is called labdata.

    mysql://dcclab@cafeine3.crulrg.ulaval.ca/dcclab@labdata
    
    which can be interpreted as:
    mysql://ssh_username@host/mysql_user@mysql_database

    If the host is on the CERVO network, the actual host will be cafeine2 and the mysql
    connection will be forwarded to the provided host.
    You can provide your own link if you have a local version on your computer, such as:
    
    db = LabdataDB("mysql://127.0.0.1/dcclab@labdata")

    In the case of 127.0.0.1 (or localhost), it will not use ssh and will connnect
    directly. However, as of May 13th 2022, it is not possible on cafeine3.
    """
    def __init__(self, databaseURL=None):
        """
        The Database is a MySQL database called `labdata`.
        """
        if databaseURL is None:
            databaseURL = "mysql://dcclab@cafeine3.crulrg.ulaval.ca/dcclab@labdata"

        self.constraints = []
        super().__init__(databaseURL)

    @classmethod
    def showHelp(cls):
        help(cls)

    def getFrequencies(self, datasetId):
        self.execute(
            r"select distinct(x) from datapoints left join spectra on spectra.spectrumId = datapoints.spectrumId where spectra.datasetId = %s",
            (datasetId,),
        )
        rows = self.fetchAll()
        nTotal = len(rows)

        freq = np.zeros(shape=(nTotal))
        for i, row in enumerate(rows):
            freq[i] = row["x"]

        return freq

    def getProjectIds(self):
        self.execute("select projectId from projects")
        rows = self.fetchAll()
        projects = []
        for row in rows:
            projects.append(row["projectId"])

        return projects

    def describeProjects(self):
        self.execute("select projectId, description from projects order by projectId")
        rows = self.fetchAll()
        datasets = []
        for row in rows:
            description = "Dataset: {0}".format(row["projectId"])
            print(description)
            print("-"*len(description))
            print("{0}\n".format(row["description"]))

    def getDatasets(self):
        self.execute("select datasetId from datasets")
        rows = self.fetchAll()
        datasets = []
        for row in rows:
            datasets.append(row["datasetId"])

        return datasets

    def describeDatasets(self):
        self.execute("select datasetId, description from datasets order by datasetId")
        rows = self.fetchAll()
        datasets = []
        for row in rows:
            description = "Dataset: {0}".format(row["datasetId"])
            print(description)
            print("-"*len(description))
            print("{0}\n".format(row["description"]))

    def getSpectrumIds(self, datasetId):
        self.execute("select spectrumId from spectra where datasetId=%s", (datasetId,))
        rows = self.fetchAll()
        spectrumIds = []
        for row in rows:
            spectrumIds.append(row["spectrumId"])

        return spectrumIds

    def getDataTypes(self):
        self.execute("select distinct dataType from spectra")
        rows = self.fetchAll()
        dataTypes = []
        for row in rows:
            dataTypes.append(row["dataType"])

        return dataTypes

    def getDatasetId(self, spectrumId):
        return self.executeSelectOne(
            "select datasetId from spectra where spectrumId = %s", (spectrumId,)
        )

    def createNewDataset(
        self, datasetId, id1Label, id2Label, id3Label, id4Label, description, projectId
    ):
        self.execute(
            """
            insert into datasets (datasetId, id1Label, id2Label, id3Label, id4Label, description, projectId)
            values(%s, %s, %s, %s, %s, %s, %s)
            """,
            (datasetId,
            id1Label,
            id2Label,
            id3Label,
            id4Label,
            description,
            projectId)
        )

    def getSpectrum(self, spectrumId):
        datasetId = self.getDatasetId(spectrumId)

        whereConstraints = []
        whereConstraints.append("spectra.spectrumId = '{0}'".format(spectrumId))

        if len(whereConstraints) != 0:
            whereClause = "where " + " and ".join(whereConstraints)
        else:
            whereClause = ""

        stmnt = """
        select x, y from datapoints left join spectra on datapoints.spectrumId = spectra.spectrumId
        {0} 
        order by x """.format(
            whereClause
        )

        self.execute(stmnt)

        rows = self.fetchAll()
        intensity = []
        for i, row in enumerate(rows):
            intensity.append(float(row["y"]))

        return np.array(intensity)

    def getSpectra(self, spectrumIds):
        spectra = None

        for spectrumId in spectrumIds:
            spectrum = self.getSpectrum(spectrumId)
            if spectra is None:
                spectra = spectrum
            else:
                spectra = np.concat(spectra, spectrum, axis = 1)

        return spectra,  spectrumIds

    def getFrequencies(self, datasetId=None, spectrumId=None):
        if datasetId is not None:
            self.execute(
                r"select distinct(x) from datapoints left join spectra on spectra.spectrumId = datapoints.spectrumId where spectra.datasetId = %s",
                (datasetId,)
            )
        else:
            self.execute(
                r"select distinct(x) from datapoints where spectrumId = %s",
                (spectrumId,)
            )

        rows = self.fetchAll()
        nTotal = len(rows)

        freq = np.zeros(shape=(nTotal))
        for i, row in enumerate(rows):
            freq[i] = row["x"]

        return freq

    def getPossibleIdValues(self, datasetId):
        self.execute(r"select id1Label, id2Label, id3Label, id4Label from datasets where datasetId = %s", (datasetId,))
        row = self.fetchOne()
        
        id1Label, id2Label, id3Label, id4Label = (row["id1Label"],row["id2Label"],row["id3Label"],row["id4Label"])

        id1s = self.executeSelectFetchOneField(r"select distinct(id1) from spectra where datasetId = %s", (datasetId,))
        id2s = self.executeSelectFetchOneField(r"select distinct(id2) from spectra where datasetId = %s", (datasetId,))
        id3s = self.executeSelectFetchOneField(r"select distinct(id3) from spectra where datasetId = %s", (datasetId,))
        id4s = self.executeSelectFetchOneField(r"select distinct(id4) from spectra where datasetId = %s", (datasetId,))

        return {id1Label:id1s, id2Label:id2s, id3Label:id3s, id4Label:id4s}


class SpectraDB(LabdataDB):
    def __init__(self, databaseURL=None):
        super().__init__(databaseURL)

    def readOceanInsightFile(self, filePath):
        # text_file = open(filePath, "br")
        # hash = hashlib.md5(text_file.read()).hexdigest()
        # text_file.close()

        # We collect all the extra lines and assumes they contain the header info
        acquisitionInfo = []
        with open(filePath, "r") as text_file:
            lines = text_file.read().splitlines()

            wavelengths = []
            intensities = []
            for line in lines:
                # FIXME? On some computers with French settings, a comma is used. We substitute blindly.
                line = re.sub(",", ".", line)

                match = re.match(r"^\s*(\d+[\.,]?\d+)\s+(-?\d*[\.,]?\d*)", line)
                if match is not None:
                    intensity = match.group(2)
                    wavelength = match.group(1)
                    wavelengths.append(wavelength)
                    intensities.append(intensity)
                else:
                    acquisitionInfo.append(line)

        return wavelengths, intensities, "\n".join(acquisitionInfo)

    def insertSpectralDataFromFiles(self, filePaths, dataType="raw"):
        inserted = 0
        for filePath in filePaths:
            match = re.search(r"([A-Z]{1,2})_?(\d{1,3})\.", filePath)
            if match is None:
                raise ValueError(
                    "The file does not appear to have a valid name: {0}".format(
                        filePath
                    )
                )

            wineId = int(ord(match.group(1)) - ord("A"))
            sampleId = int(match.group(2))
            spectrumId = "{0:04}-{1:04d}".format(wineId, sampleId)

            wavelengths, intensities = self.readOceanInsightFile(filePath)
            try:
                self.insertSpectralData(
                    wavelengths, intensities, dataType, wineId, sampleId
                )
                print("Inserted {0}".format(filePath))
                inserted += 1
            except ValueError as err:
                print(err)

        return inserted

    def insertSpectralData(self, spectrumId, x, y):
        try:
            for i, j in zip(x, y):
                statement = (
                    "insert into datapoints (spectrumId, x, y) values(%s, %s, %s)"
                )
                self.execute(statement, (spectrumId, i, j))
        except Exception as err:
            raise ValueError("Unable to insert spectral data: {0}".format(err))

    def subtractFluorescence(self, rawSpectra, polynomialDegree=5):

        """
        Remove fluorescence background from the data.
        :return: A corrected data without the background.
        """

        correctedSpectra = np.empty_like(rawSpectra)
        for i in range(rawSpectra.shape[1]):
            spectrum = rawSpectra[:, i]
            correctedSpectra[:, i] = BaselineRemoval(spectrum).IModPoly(
                polynomialDegree
            )

        return correctedSpectra
