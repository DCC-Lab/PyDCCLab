import env
from dcclab.database import *
from datetime import date
from zipfile import ZipFile
import unittest
import os
import numpy as np

dbPath = 'test.db'
ziliaDb = '/tmp/zilia.db'


class TestDatabase(env.DCCLabTestCase):
    def testEmptyDatabaseNoWritePermission(self):
        with self.assertRaises(Exception):
            db = Database(dbPath, writePermission=False)

    def testEmptyDatabaseWritePermission(self):
        db = Database('test.db', writePermission=True)
        self.assertIsNotNone(db)
        self.assertTrue(os.path.exists(dbPath))
        os.remove(dbPath)

    def setUp(self):
        self.db = None

    def tearDown(self):
        if os.path.exists(dbPath):
            os.remove(dbPath)

    def testCreateEmptyDatabase(self):
        db = Database(dbPath, writePermission=True)
        self.assertIsNotNone(db)
        self.assertTrue(os.path.exists(dbPath))

    def testCreateDatabaseAddTable(self):
        db = Database(dbPath, writePermission=True)
        self.assertIsNotNone(db)

        column1 = Column("column1", Type.Integer, Constraint.Primary)
        column2 = Column("column2", Type.Text)
        db.createSimpleTable(name="table1", columns=[column1, column2])
        
        self.assertEqual(db.tables,['table1'])
        self.assertEqual(db.columns('table1'),['column1','column2'])

    # def testCreateDatabaseAddTable(self):
    #     db = Database(dbPath, writePermission=True)
    #     self.assertIsNotNone(db)

    #     column = Column("column1", Type.Integer, Key.Primary)
    #     db.createSimpleTable(name="table1", columns=[column])

class ZiliaDB(Database):
    def __init__(self):
        super().__init__(ziliaDb, writePermission=False)

    def getMonkeyNames(self):
        self.execute("select name from monkeys order by name")
        return self.fetchAll()

    def getAllRawSpectra(self, nameOrId):
        # self.execute("select wavelength, intensity from spectra where name like '%{0}%' or id like '%{0}%'".format(nameOrId))
        self.execute(r"select wavelength, intensity, md5,column from spectra where md5 like '%d5f%' and column like '%raw%'".format(nameOrId))
        rows = self.fetchAll()
        nTotal = len(rows)
        print(nTotal)
        spectra = np.zeros(shape=(nTotal,2))
        for i,row in enumerate(rows):
            spectra[i,0] = row['wavelength']
            spectra[i,1] = row['intensity']
            print(row['md5'], row['column'])

        return spectra

class TestZilia(env.DCCLabTestCase):
    def testZiliaDBCreation(self):
        self.assertIsNotNone(ZiliaDB())

    def testZiliaGetMonkeyNames(self):
        db=ZiliaDB()
        self.assertIsNotNone(db)
        db.execute("select name from monkeys order by name")
        rows = db.fetchAll()
        self.assertTrue(len(rows) == 4)
        self.assertEqual([ r['name'] for r in rows], ['Bresil', 'Kenya', 'Rwanda', 'Somalie'])

    def testZiliaGetMonkeyNamesFromClass(self):
        db=ZiliaDB()
        self.assertIsNotNone(db)
        rows = db.getMonkeyNames()
        self.assertTrue(len(rows) == 4)
        self.assertEqual([ r['name'] for r in rows], ['Bresil', 'Kenya', 'Rwanda', 'Somalie'])

    def testGetSpectra(self):
        db=ZiliaDB()
        self.assertIsNotNone(db)
        spectra = db.getAllRawSpectra(nameOrId='Rwanda')
        print(spectra.shape)
if __name__ == '__main__':
    unittest.main()
