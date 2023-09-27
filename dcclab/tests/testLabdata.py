import env
from dcclab.database import *
import unittest
import numpy as np

class TestLabdataDatabaseFunctionality(env.DCCLabTestCase):
    def setUp(self):
        self.db = SpectraDB()

    def tearDown(self) -> None:
        self.db.disconnect()

    def testInitDB(self):
        self.assertIsNotNone(LabdataDB())

    def testConnectDBWithoutException(self):
        db = LabdataDB()
        db.connect()
        db.disconnect()

    def testConnectDBBadURL(self):
        with self.assertRaises(Exception):
            db = LabdataDB("abd://blabla")
            db.disconnect()

    def testConnectDBBadHost(self):
        with self.assertRaises(Exception):
            db = LabdataDB("mysql://somehost")
            db.disconnect()

    # def testConnectDBGoodHost(self):
    #     db = LabdataDB("mysql://127.0.0.1/root@labdata")
    #     db.disconnect()

    def testLocalConnectOnCafeine2(self):
        if self.isAtCERVO():
            with self.assertRaises(Exception):  # access denied, only localhost as of May 17th
                db = LabdataDB("mysql://cafeine3.crulrg.ulaval.ca/dcclab@labdata")
        else:
            self.skipTest("Not at CERVO: skipping local connections")

    # def testConnectOnCafeine3ViaSSH(self):
    #     db = LabdataDB("mysql+ssh://dcclab@cafeine3.crulrg.ulaval.ca:127.0.0.1/dcclab@labdata")
    #     db.disconnect()

    def isAtCERVO(self, local_ip=None):
        import ipaddress
        if local_ip is None:
            import socket
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = ipaddress.ip_address(s.getsockname()[0])
        else:
            local_ip = ipaddress.ip_address(local_ip)

        cervoNet = ipaddress.IPv4Network("172.16.1.0/24")

        return (local_ip in cervoNet)

    def testIsAtCervo(self):
        self.assertTrue(self.isAtCERVO("172.16.1.106")) # cafeine2
        self.assertFalse(self.isAtCERVO("192.168.2.1"))

    def testLocalConnectOnCafeine3(self):
        if self.isAtCERVO():
            db = LabdataDB("mysql://cafeine3.crulrg.ulaval.ca/dcclab@labdata")
        else:
            self.skipTest("Not at CERVO: skipping local connections")

    def testConnectOnCafeine3ViaSSH(self):
        db = LabdataDB("mysql+ssh://dcclab@cafeine2.crulrg.ulaval.ca:cafeine3.crulrg.ulaval.ca/dcclab@labdata")

    def testExecute(self):
        self.db.execute("show tables")
        rows = self.db.fetchAll()
        self.assertTrue(len(rows) > 0)

    def testExecuteOnDefaultServer(self):
        db = LabdataDB()
        db.execute("show tables")
        rows = db.fetchAll()
        self.assertTrue(len(rows) > 0)

    def testDeniedCreateAnythingUsername_dcclab(self):
        with self.assertRaises(AccessDeniedError):
            db = LabdataDB() # defaults to dcclab
            db.execute("CREATE TABLE test (testfield int)")


    def testCreateNewProject(self):
        # Basic connection is without write privilege
        with self.assertRaises(Exception):
            try:
                self.db.execute("insert into projects (projectId, description) values('test','This project is solely for unit testing the database and should never be used')")
                elements = self.db.getProjectIds()
                self.assertTrue("test" in elements)
            finally:
                self.db.execute("delete from projects where projectId = 'test'")

    def testCreateNewDataset(self):
        # Basic connection is without write privilege
        with self.assertRaises(Exception):
            try:
                self.db.execute("insert into projects (projectId, description) values('test','This project is solely for unit testing the database and should never be used')")
                self.db.createNewDataset("TEST-001", "id1", "id2", "id3", "id4", "description", "test")
                datasets = self.db.getDatasets()
                self.assertTrue("TEST-001" in datasets)
            finally:
                self.db.execute("delete from datasets where datasetId = 'TEST-001'")
                self.db.execute("delete from projects where projectId = 'test'")

    def testDescribeProjects(self):
        self.db.describeProjects()
        self.db.describeDatasets()

    @unittest.expectedFailure
    def testIdValues(self):
        idValues  = self.db.getPossibleIdValues("DRS-001")
        self.assertIsNotNone(idValues)

        self.db.getPossibleIdValues("SHAVASANA-001")
        self.db.getPossibleIdValues("WINE-001")

    def testGetFormatString(self):
        formatString = self.db.getSpectrumIdFormat(datasetId="DRS-001")
        self.assertIsNotNone(formatString)

    def testUseSpecificFormatString(self):
        spectrumId = self.db.formatSpectrumId(datasetId="WINE-001", id1="A", id2=1)

    def testGetIdTypes(self):
        print(self.db.getIdTypes("WINE-001"))
        print(self.db.getIdTypesFromDatasetFormatString("WINE-001"))

    def testFormatStringAcceptsLetterSAsType(self):
        self.assertEqual("{0:s}".format("test"), "test")

    def testDevelopGetIdTypesFromFormatString(self):
        formatString = "{0}-{1:04d}-{2:04d}"
        elements = formatString.split("-")
        self.assertTrue(len(elements) == 3)
        idTypes = {}
        ids = ["id1", "id2", "id3", "id4"]
        for i,singleFormat in enumerate(elements):
            match = re.match(r"\{(\d):?.*?([sfd]?)\}", singleFormat)
            formatTypeAsString = match.groups()[1]
            if formatTypeAsString == '':
                idTypes[ids[i]] = str
            elif formatTypeAsString == 'd':
                idTypes[ids[i]] = int
            elif formatTypeAsString == 'f':
                idTypes[ids[i]] = float

        print(idTypes)


        datasets = ['WINE-001']

        for datasetId in datasets:
            idTypes = self.db.getIdTypes(datasetId)
            self.db.execute("select datasetId, id1, id2, id3, id4 from spectra where datasetId = %s limit 5", (str(datasetId),))

            rows = self.db.fetchAll()
            for row in rows:
                try:
                    spectrumId = self.db.formatSpectrumId(**row)
                except Exception as err:
                    print(err)

    @unittest.expectedFailure
    def testInferTypes(self):
        self.assertTrue( self.db._inferListType(["1","2","3"]) == int)
        self.assertFloat( self.db._inferListType(["1.0","2.0","3.0"]) == int)
        self.assertTrue( self.db._inferListType(["1","2","3.1"]) == float)
        self.assertTrue( self.db._inferListType(["1","2", "allo"]) == str )
        self.assertTrue( self.db._inferListType(["5.2", "4.2", "3.1"]) == float )

    def testShowInfo(self):
        self.db.showDatabaseInfo()

class TestLabdataDatabaseContent(env.DCCLabTestCase):
    def setUp(self):
        self.db = SpectraDB()

    def tearDown(self) -> None:
        self.db.disconnect()

    def testInitDB(self):
        self.assertIsNotNone(LabdataDB())

    def testGetProjects(self):
        elements = self.db.getProjectIds()
        self.assertTrue(len(elements) > 10)

    def testGetDatasets(self):
        elements = self.db.getDatasets()

        for datasetId in elements:
            self.assertIsNotNone(r".+-\d+",datasetId)
        self.assertTrue("WINE-001" in elements)
        self.assertTrue("DRS-001" in elements)
        self.assertTrue("SHAVASANA-001" in elements)

    def testGetDataTypes(self):
        elements = self.db.getDataTypes()
        self.assertTrue("raw" in elements)
        self.assertTrue("dark-reference" in elements)
        self.assertTrue("white-reference" in elements)

    def testGetSpectra(self):
        data, ids = self.db.getSpectra("DRS-001")
        self.assertTrue(data.shape[0] > 10)

    def testGetWineSpectra(self):
        data, ids = self.db.getSpectra("WINE-001")
        self.assertTrue(data.shape[0] > 10)

    def testGetFrequencies(self):
        elements = self.db.getDatasets()

        for datasetId in elements:
            x = self.db.getFrequencies(datasetId=datasetId)
            self.assertTrue(len(x) >= 1, "for dataset {0}".format(datasetId))
            self.assertIsNotNone(r".+-\d+",datasetId)

    def testGetFrequenciesSpecificId(self):
        x = self.db.getFrequencies(datasetId="DRS-001", id1='White')
        self.assertTrue(len(x) > 10)

        x = self.db.getFrequencies(datasetId="DRS-001", id1='White', id2=1)
        self.assertTrue(len(x) > 10)

        x = self.db.getFrequencies(datasetId="DRS-001", region="White", sampleId=(1,2,3))
        self.assertTrue(len(x) > 10)

        x = self.db.getFrequencies(datasetId="SHAVASANA-001", modality='DRS')
        self.assertTrue(len(x) > 10)

    def testGetSpectrumIds(self):
        datasets = self.db.getDatasets()
        for datasetId in datasets:
            spectrumIds = self.db.getSpectrumIds(datasetId=datasetId)

    def testGetSpectrumIdsWithRestrictions(self):
        rows = self.db.getSpectrumIds(datasetId="DRS-001")
        self.assertIsNotNone(rows)
        self.assertTrue(len(rows) > 1)

        rows = self.db.getSpectrumIds(datasetId="DRS-001", id1='White')
        self.assertIsNotNone(rows)
        self.assertTrue(len(rows) > 1)

        rows = self.db.getSpectrumIds(datasetId="DRS-001", id2=1)
        self.assertIsNotNone(rows)
        self.assertTrue(len(rows) > 1)

        rows = self.db.getSpectrumIds(datasetId="DRS-001", id1='White', id2=1)
        self.assertIsNotNone(rows)
        self.assertTrue(len(rows) > 1)

    def testGetSpectrumIdsWithUserLabelRestrictions(self):
        rows = self.db.getSpectrumIds(datasetId="DRS-001", region='White')
        self.assertIsNotNone(rows)
        self.assertTrue(len(rows) > 1)

        rows = self.db.getSpectrumIds(datasetId="SHAVASANA-001", modality='CARS')
        self.assertIsNotNone(rows)
        self.assertTrue(len(rows) > 1)

        rows = self.db.getSpectrumIds(datasetId="SHAVASANA-001", modality='CARS', distance=1)
        self.assertIsNotNone(rows)
        self.assertTrue(len(rows) > 1)

    def testGetSpectrumIdsWithRestrictionsInSets(self):
        rows = self.db.getSpectrumIds(datasetId="DRS-001", id1='White', id2=(1,2,3,4))
        self.assertIsNotNone(rows)
        self.assertTrue(len(rows) > 1)

    def testGetSpectrumIdsWithRestrictionsInSetsOnly(self):
        rows = self.db.getSpectrumIds(datasetId="DRS-001", id2=(2,3))
        self.assertIsNotNone(rows)
        self.assertTrue(len(rows) > 1)

    def testGetSpectralDataFrom(self):
        self.db.getSpectralDataFrame(datasetId="WINE-001")

# class TestMySQLDatabase(env.DCCLabTestCase):
#     def testLocalMySQLDatabase(self):
#         db = Database("mysql://127.0.0.1/root@raman")
#         db.execute("select * from spectra where datatype = 'raw'")
#
#         rows = []
#         row = db.fetchOne()
#         i = 0
#         while row is not None:
#             if i % 10000 == 0:
#                 print(i)
#             i += 1
#             rows.append(row)
#             row = db.fetchOne()
#
#         self.assertTrue(len(rows) > 0)

if __name__ == '__main__':
    unittest.main()
