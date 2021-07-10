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
    statementFromAllJoin = "from spectra as s, spectralFiles as f, monkeys as m where s.md5 = f.md5 and f.monkeyId = m.id"
    statementFromSpectra = "from spectra as s"

    def __init__(self):
        super().__init__(ziliaDb, writePermission=False)
        self._wavelengths = None

    @property
    def wavelengths(self):
        if self._wavelengths is None:
            self._wavelengths = self.getWavelengths()

        return self._wavelengths

    def getWavelengths(self):
        self.execute(r"select distinct(wavelength) from spectra order by wavelength")
        rows = self.fetchAll()
        nTotal = len(rows)

        wavelengths = np.zeros(shape=(nTotal))
        for i,row in enumerate(rows):
            wavelengths[i] = row['wavelength']

        return wavelengths

    def getAcquisitionType(self):
        self.execute(r"select distinct(column) from spectra order by column")
        rows = self.fetchAll()
        nTotal = len(rows)

        types = set()
        for row in rows:
            type = row['column']
            if re.match('raw', type) is not None:
                type = 'raw'
            types.add(type)

        return sorted(types)

    def getMonkeyNames(self):
        self.execute("select name from monkeys order by name")
        rows = self.fetchAll()
        names = []
        for row in rows:
            names.append(row['name'])
        return names

    def getAllRawSpectra(self, monkey="%", target="%"):
        self.execute(r"select s.wavelength, s.intensity, s.md5, s.column {0} where s.md5 like '%d5f%' and s.column like '%raw%'".format(self.statementFromSpectra))
        rows = self.fetchAll()
        nTotal = len(rows)
        spectra = np.zeros(shape=(nTotal,2))
        for i,row in enumerate(rows):
            spectra[i,0] = row['wavelength']
            spectra[i,1] = row['intensity']

        return spectra

    def reshapeSpectraAsMatrix(self, spectra):
        for i,  in enumerate(spectra.shape[0]):
            spectra[i,0]
            spectra[i,1]


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

    def testGetMonkeyNames(self):
        db=ZiliaDB()
        self.assertIsNotNone(db)
        names = db.getMonkeyNames()
        self.assertEqual(names, ['Bresil', 'Kenya', 'Rwanda', 'Somalie'])

    def testGetWavelengths(self):
        db=ZiliaDB()
        self.assertIsNotNone(db)
        wavelengths = db.getWavelengths()
        self.assertTrue(wavelengths.shape == (512,))

    def testGetSpectra(self):
        db=ZiliaDB()
        self.assertIsNotNone(db)
        spectra = db.getAllRawSpectra()
        self.assertIsNotNone(spectra)
        
    def testGetAcquisitionType(self):
        db=ZiliaDB()
        self.assertIsNotNone(db)
        types = db.getAcquisitionType()
        self.assertEqual(types, ['bg','raw','ref'])

if __name__ == '__main__':
    unittest.main()
