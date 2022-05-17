import env
from dcclab.database import LabdataDB, SpectraDB
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
