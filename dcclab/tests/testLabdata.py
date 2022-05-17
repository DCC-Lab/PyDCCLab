import env
from dcclab.database import *
import unittest
import os

class TestLabdataDatabase(env.DCCLabTestCase):

    def testInitDB(self):
        self.assertIsNotNone(LabdataDB())

    def testConnectDBWithoutException(self):
        db = LabdataDB()
        db.connect()

    def testConnectDBBadURL(self):
        with self.assertRaises(Exception):
            db = LabdataDB("abd://blabla")

    def testConnectDBBadHost(self):
        with self.assertRaises(Exception):
            db = LabdataDB("mysql://somehost")

    def testConnectDBGoodHost(self):
        db = LabdataDB("mysql://127.0.0.1/root@labdata")

    def testLocalConnectOnCafeine2(self):
        if self.isAtCERVO():
            with self.assertRaises(Exception):  # access denied, only localhost as of May 17th
                db = LabdataDB("mysql://cafeine2.crulrg.ulaval.ca/dcclab@labdata")
        else:
            self.skipTest("Not at CERVO: skipping local connections")

    def testConnectOnCafeine2ViaSSH(self):
        db = LabdataDB("mysql+ssh://dcclab@cafeine2.crulrg.ulaval.ca:127.0.0.1/dcclab@labdata")

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
        db = LabdataDB("mysql://127.0.0.1/root@labdata")
        db.execute("show tables")
        rows = db.fetchAll()
        self.assertTrue(len(rows) > 0)

    def testExecuteOnDefaultServer(self):
        db = LabdataDB()
        db.execute("show tables")
        rows = db.fetchAll()
        self.assertTrue(len(rows) > 0)

    def setUp(self):
        self.db = LabdataDB("mysql+ssh://dcclab@cafeine2.crulrg.ulaval.ca:cafeine3.crulrg.ulaval.ca/dccadmin@labdata")

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
        elements = self.db.getDatasets()
        for datasetId in elements:
            data, ids = self.db.getSpectra(datasetId)
            self.assertTrue(data.shape[0] > 10)

    def testDeniedCreateAnythingUsername_dcclab(self):
        with self.assertRaises(AccessDeniedError):
            db = LabdataDB()
            db.execute("CREATE TABLE test (testfield int)")

    def testCreateNewProject(self):
        try:
            self.db.execute("insert into projects (projectId, description) values('test','This project is solely for unit testing the database and should never be used')")
            elements = self.db.getProjectIds()
            self.assertTrue("test" in elements)
        finally:
            self.db.execute("delete from projects where projectId = 'test'")

    def testCreateNewDataset(self):
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

class TestMySQLDatabase(env.DCCLabTestCase):
    def testLocalMySQLDatabase(self):
        db = Database("mysql://127.0.0.1/root@raman")
        db.execute("select * from spectra where datatype = 'raw'")

        rows = []
        row = db.fetchOne()
        i = 0
        while row is not None:
            if i % 10000 == 0:
                print(i)
            i += 1
            rows.append(row)
            row = db.fetchOne()

        self.assertTrue(len(rows) > 0)

if __name__ == '__main__':
    unittest.main()
