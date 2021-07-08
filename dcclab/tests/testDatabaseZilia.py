import env
from dcclab.database import *
from datetime import date
from zipfile import ZipFile
import unittest
import os

dbPath = 'test.db'

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
        
        print(db.tables)
        print(db.columns('table1'))

    # def testCreateDatabaseAddTable(self):
    #     db = Database(dbPath, writePermission=True)
    #     self.assertIsNotNone(db)

    #     column = Column("column1", Type.Integer, Key.Primary)
    #     db.createSimpleTable(name="table1", columns=[column])

if __name__ == '__main__':
    unittest.main()
