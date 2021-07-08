import env
from dcclab import Database
from datetime import date
from zipfile import ZipFile
import unittest
import os

class TestDatabase(env.DCCLabTestCase):
    def testEmptyDatabaseNoWritePermission(self):
        with self.assertRaises(Exception):
            db = Database('test.db', writePermission=False)

    def testEmptyDatabaseWritePermission(self):
        db = Database('test.db', writePermission=True)
        self.assertIsNotNone(db)
        self.assertTrue(os.path.exists('test.db'))
        os.remove('test.db')

    def setUp(self):
        self.db = None

    def tearDown(self):
        if self.db is not None:
            if os.path.exists(self.db.path):
                os.remove('test.db')

        if os.path.exists('test.db'):
            os.remove('test.db')

    def testCreateEmptyDatabase(self):
        db = Database('test.db', writePermission=True)
        self.assertIsNotNone(db)
        self.assertTrue(os.path.exists('test.db'))
        

if __name__ == '__main__':
    unittest.main()
