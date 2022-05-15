from .database import *
import numpy as np
import requests
import re


class LabdataDB(Database):
    def __init__(self, databaseURL=None):
        """
        The Database is a MySQL database called `labdata`.
        """
        if databaseURL is None:
            databaseURL = "mysql://dcclab@cafeine3.crulrg.ulaval.ca/dcclab@labdata"

        self.progressStart = None
        self.constraints = []
        super().__init__(databaseURL)

    def showHelp(self):
        print(
            """
        This is a general database tool to access all information about projects, files,
        and spectral datasets of the DCCLab. The database is on Cafeine3 and can be accessed
        with the dcclab username and normal password via a secure shell, and then via
        mysql also with dcclab and the same password. Te database is called labdata.

        mysql://dcclab@cafeine3.crulrg.ulaval.ca/dcclab@labdata
        
        which can be interpreted as:
        mysql://ssh_username@ssh_host/mysql_user@mysql_database

        You can provide your own link if you have a local version on your computer, such as:
        
        db = LabdataDB("mysql://127.0.0.1/dcclab@labdata")

        In the case of 127.0.0.1 (or localhost), it will not use ssh and will connnect
        directly. However, as of May 13th 2022, it is not possible on cafeine3.
        """
        )

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

    def getDatasets(self):
        self.execute("select datasetId from datasets")
        rows = self.fetchAll()
        datasets = []
        for row in rows:
            datasets.append((row["name"], row["datasetId"]))

        return datasets

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

    def showProgressBar(
        self,
        iteration,
        total,
        prefix="",
        suffix="",
        decimals=1,
        length=100,
        fill="█",
        printEnd="\r",
    ):
        """
        From: https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console

        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        """

        if self.progressStart is None:
            self.progressStart = time.time()

        if time.time() > self.progressStart + 3:
            percent = ("{0:." + str(decimals) + "f}").format(
                100 * (iteration / float(total))
            )
            filledLength = int(length * iteration // total)
            bar = fill * filledLength + "-" * (length - filledLength)
            print(f"\r{prefix} |{bar}| {percent}% {suffix}", end=printEnd)

            if iteration == total:
                print()

        if iteration == total:
            self.progressStart = None


class SpectraDB(LabdataDB):
    def __init__(self, databaseURL=None):
        super().__init__(databaseURL)

    def readOceanInsightFile(self, filePath):
        # text_file = open(filePath, "br")
        # hash = hashlib.md5(text_file.read()).hexdigest()
        # text_file.close()

        # We collect all the extra lines and assumes they contain the header info
        userInfo = []
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
                    userInfo.append(line)

        return wavelengths, intensities, "\n".join(userInfo)

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
        self.beginTransaction()
        for i, j in zip(x, y):
            statement = (
                "insert into datapoints (spectrumId, x, y) values(%s, %s, %s, %s)"
            )
            self.execute(statement, (spectrumId, i, j))
        self.endTransaction()
