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

    def testConnectOnCafeine2(self):
        with self.assertRaises(Exception): # access denied, only localhost as of May 17th
            db = LabdataDB("mysql://cafeine2.crulrg.ulaval.ca/dcclab@labdata")

    def testConnectOnCafeine2ViaSSH(self):
        db = LabdataDB("mysql+ssh://dcclab@cafeine2.crulrg.ulaval.ca:127.0.0.1/dcclab@labdata")

    def testConnectOnCafeine3(self):
        db = LabdataDB("mysql://cafeine3.crulrg.ulaval.ca/dcclab@labdata")

    def testConnectOnCafeine3ViaSSH(self):
        db = LabdataDB("mysql+ssh://dcclab@cafeine2.crulrg.ulaval.ca:cafeine3.crulrg.ulaval.ca/dcclab@labdata")

    def testExecute(self):
        db = LabdataDB("mysql://127.0.0.1/root@labdata")
        db.execute("show tables")
        rows = db.fetchAll()
        self.assertTrue(len(rows) > 0)

    def testExecuteOnCafeine3(self):
        db = LabdataDB("mysql://cafeine3.crulrg.ulaval.ca/dcclab@labdata")
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

    def testDeniedCreateAnythingDCCLab(self):
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
