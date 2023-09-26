import env
from dcclab import Database as db
from dcclab import Database, Engine, MySQLDatabase
import unittest
import os

@unittest.skip
class TestSqliteDatabase(env.DCCLabTestCase):
    def setUp(self):
        self.filePath = os.path.join(str(self.tmpDir), 'unittest.db')
        self.fileURL = "sqlite3://" + self.filePath
        self.wrongFile = os.path.join(str(self.tmpDir), 'wrongfile.db')

        # with db("file://"+self.filePath, True) as testDB:
        #     # testDB.beginTransaction()
        #     testTable = {'test_table': {'column_1': 'INTEGER PRIMARY KEY', 'column_2': 'TEXT', 'column_3': 'REAL',
        #                                 'file_path': 'TEXT'}}
        #     testDB.createTable(testTable)
        #     # testDB.commit()
        #
        #     # testDB.beginTransaction()
        #     frstValue = {'column_1': 1234, 'column_2': 'abcd', 'column_3': 0.1234}
        #     scndValue = {'column_1': 5678, 'column_2': 'efgh', 'column_3': 0.5678}
        #     testDB.insert('test_table', frstValue)
        #     testDB.insert('test_table', scndValue)
        #     # testDB.commit()

    def tearDown(self):
        try:
            os.remove(self.filePath)
        except Exception as err:
            pass

    def test001_recognizeURL(self):
        with db(self.fileURL, True) as testDB:
            self.assertTrue(testDB.databaseEngine == Engine.sqlite3)

    def test002_showInfo(self):
        with db(self.fileURL, True) as testDB:
            testDB.showDatabaseInfo()

    def test003_create_table(self):
        with db(self.fileURL, True) as testDB:
            testDB.execute("create table testtable(x int) ")


    def testConnectSuccessful(self):
        database = db(self.fileURL)
        self.assertTrue(database.connect())
        database.disconnect()

    def testConnectUnsuccessful(self):
        with self.assertRaises(Exception):
            database = db(self.wrongFile)

    def testConnectWithWrongMode(self):
        with self.assertRaises(Exception):
            database = db(self.fileURL, 'wrongmode')
            self.assertFalse(database.connect())
            database.disconnect()

    def testConnectCreatesCursor(self):
        database = db(self.fileURL)
        database.connect()
        self.assertIsNotNone(database.cursor)
        database.disconnect()

    def testDisconnectSuccesfull(self):
        database = db(self.fileURL)
        database.connect()
        database.disconnect()
        self.assertFalse(database.isConnected)

    def testDisconnectRemovesCursor(self):
        database = db(self.fileURL)
        database.connect()
        database.disconnect()
        self.assertIsNone(database.cursor)

    def testIsConnected(self):
        database = db(self.fileURL)
        database.connect()
        self.assertTrue(database.isConnected)
        database.disconnect()

    def testIsConnectedOnInit(self):
        database = db(self.fileURL)
        self.assertTrue(database.isConnected)
        database.disconnect()

    def testIsNotConnected(self):
        with self.assertRaises(Exception):
            database = db("notADatabase")

    @unittest.expectedFailure
    def testChangeConnectionModeToValidMode(self):
        database = db(self.fileURL)
        database.connect()
        database.changeConnectionMode('rw')
        self.assertNotEqual(database.mode, 'ro')
        database.disconnect()

    # Linux and MacOS are 'posix', windows is 'nt'.
    @unittest.skipIf(os.name == 'posix', reason='Path is a Windows Path.')
    def testWindowsPathToPosix(self):
        database = db(r'C:\sqlite3\Database\test.db', writePermission=True)
        self.assertEqual(database.path, 'file:C:/sqlite3/Database/test.db?mode=rwc')
        database.disconnect()

    def testCommit(self):  # TODO Is there anything else we could test for Commit?
        database = db(self.fileURL, writePermission=True)
        database.connect()

        testValue = {'column_1': 9101, 'column_2': 'plop', 'column_3': 0.9101}
        database.insert('test_table', testValue)
        database.commit()

        row = database.select('test_table', 'column_1', 'column_1=9101')
        self.assertEqual(row[0]['column_1'], 9101)
        database.disconnect()

    def testRollback(self):
        database = db(self.fileURL, writePermission=True)
        database.connect()

        testValue = {'column_1': 9101, 'column_2': 'plop', 'column_3': 0.9101}
        database.beginTransaction()
        database.insert('test_table', testValue)
        database.rollback()

        database.beginTransaction()
        row = database.select('test_table', 'column_1', 'column_1=9101')
        database.endTransaction()
        self.assertFalse(row)
        database.disconnect()

    def testExecute(self):
        database = db(self.fileURL, writePermission=True)
        database.connect()

        statement = 'DROP TABLE IF EXISTS "test_table"'
        database.execute(statement)
        database.commit()

        self.assertFalse(database.tables)
        database.disconnect()

    def testTables(self):
        database = db(self.fileURL)
        database.connect()

        self.assertEqual(database.tables[0], 'test_table')
        database.disconnect()

    def testSelectResultsFound(self):
        database = db(self.fileURL)
        database.connect()

        rows = database.select('test_table', 'column_1', 'column_3<1')
        for row in rows:
            self.assertTrue(row['column_1'] == 1234 or 5678)
        database.disconnect()

    def testSelectNoResultsFound(self):
        database = db(self.fileURL)
        database.connect()

        rows = database.select('test_table', 'column_1', 'column_2="aaaa"')
        self.assertFalse(rows)
        database.disconnect()

    def testCreateTable(self):
        database = db(self.fileURL, writePermission=True)
        database.connect()

        newTable = {'new_table': {'column_1': 'INTEGER PRIMARY KEY', 'column_2': 'TEXT'}}
        database.createTable(newTable)
        database.commit()

        self.assertTrue(database.tables.index('new_table'))
        database.disconnect()

    def testDropTable(self):
        database = db(self.fileURL, writePermission=True)
        database.connect()

        database.dropTable('test_table')
        database.commit()

        self.assertFalse(database.tables)
        database.disconnect()

    def testInsert(self):
        database = db(self.fileURL, writePermission=True)
        database.connect()

        testValue = {'column_1': 1121, 'column_2': 'bleh', 'column_3': 0.1121}
        database.insert('test_table', testValue)
        database.commit()

        row = database.select('test_table', 'column_1', 'column_1=1121')
        self.assertEqual(row[0]['column_1'], 1121)
        database.disconnect()

    def testMode(self):
        database = db(self.fileURL, writePermission=True)
        database.connect()
        self.assertEqual(database.mode, 'rwc')
        database.disconnect()

    def testFetchAll(self):
        database = db(self.fileURL)
        database.connect()

        database.execute('SELECT * FROM test_table')
        rows = database.fetchAll()
        for row in rows:
            self.assertTrue(row['column_1'] == 1234 or 5678)
        database.disconnect()

    def testFetchOne(self):
        database = db(self.fileURL)
        database.connect()

        database.execute('SELECT * FROM test_table')
        row = database.fetchOne()
        self.assertTrue(row['column_1'] == 1234)

        row = database.fetchOne()
        self.assertTrue(row['column_1'] == 5678)

        row = database.fetchOne()
        self.assertFalse(row)

        database.disconnect()

    def testContextManager(self):
        with db(self.fileURL) as database:
            self.assertTrue(database.isConnected)

        self.assertFalse(database.isConnected)


class TestMySQLDatabase(env.DCCLabTestCase):
    def setUp(self):
        super().setUp()

        self.db = MySQLDatabase("mysql+ssh://dcclab@cafeine2.crulrg.ulaval.ca:cafeine3.crulrg.ulaval.ca/dcclab@labdata")

        self.assertIsNotNone(self.db)
        self.db.connect()
        self.assertTrue(self.db.isConnected)

    def tearDown(self):
        super().tearDown()
        self.db.disconnect()

    def testConnectDatabase(self):
        self.assertTrue(db.isConnected)

    def testDisconnectDatabase(self):
        self.assertTrue(self.db.isConnected)
        self.db.disconnect()
        self.assertFalse(self.db.isConnected)

    def testShowTables(self):
        names = self.db.tables
        self.assertTrue(len(names) > 1)

    def testEnforceForeignKeys(self):
        self.db.enforceForeignKeys()
        self.assertEqual(self.db.areForeignKeysEnforced(), 1)

    def testDisableForeignKeys(self):
        self.db.disableForeignKeys()
        self.assertEqual(self.db.areForeignKeysEnforced(), 0)

if __name__ == '__main__':
    unittest.main()
