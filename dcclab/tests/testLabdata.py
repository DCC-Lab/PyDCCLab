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
