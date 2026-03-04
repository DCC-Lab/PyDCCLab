import env
from dcclab import Database as db
from dcclab import Database, Engine, MySQLDatabase
import unittest
import os
import socket

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


@unittest.skipUnless(env.canAccessLabdata(), "Requires access to cafeine2 for SSH tunnel")
class TestMySQLDatabase(env.DCCLabTestCase):
    def setUp(self):
        super().setUp()

        self.db = MySQLDatabase("mysql+ssh://dcclab@cafeine2.crulrg.ulaval.ca/dcclab@cafeine3.crulrg.ulaval.ca/labdata")

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

def isLocalMySQLRunning():
    try:
        s = socket.create_connection(("127.0.0.1", 3306), timeout=2)
        s.close()
        return True
    except (socket.timeout, socket.error, OSError):
        return False


def canAccessLocalMySQL():
    try:
        import mysql.connector
        conn = mysql.connector.connect(host="127.0.0.1", user="test", password="test", database="test")
        conn.close()
        return True
    except Exception:
        return False


class TestLocalMySQLPrerequisites(env.DCCLabTestCase):
    def testLocalMySQLIsRunning(self):
        if not isLocalMySQLRunning():
            self.fail(
                "MySQL is not running on 127.0.0.1:3306.\n"
                "Start it with one of:\n\n"
                "  brew services start mysql        # macOS with Homebrew\n"
                "  sudo systemctl start mysql       # Linux with systemd\n"
                "  mysql.server start               # macOS alternate\n"
            )

    def testLocalMySQLTestUserIsAvailable(self):
        if not isLocalMySQLRunning():
            self.skipTest("MySQL is not running")
        if not canAccessLocalMySQL():
            self.fail(
                "Cannot connect to local MySQL as user 'test'.\n"
                "An administrator must run the following commands to set up the test environment:\n\n"
                "  mysql -u root -p -e \"\n"
                "    CREATE DATABASE IF NOT EXISTS test;\n"
                "    CREATE USER IF NOT EXISTS 'test'@'127.0.0.1' IDENTIFIED BY 'test';\n"
                "    CREATE USER IF NOT EXISTS 'test'@'localhost' IDENTIFIED BY 'test';\n"
                "    GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER, INDEX, REFERENCES,\n"
                "          CREATE TEMPORARY TABLES, LOCK TABLES, EXECUTE, CREATE VIEW, SHOW VIEW,\n"
                "          CREATE ROUTINE, ALTER ROUTINE, EVENT, TRIGGER\n"
                "          ON test.* TO 'test'@'127.0.0.1';\n"
                "    GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER, INDEX, REFERENCES,\n"
                "          CREATE TEMPORARY TABLES, LOCK TABLES, EXECUTE, CREATE VIEW, SHOW VIEW,\n"
                "          CREATE ROUTINE, ALTER ROUTINE, EVENT, TRIGGER\n"
                "          ON test.* TO 'test'@'localhost';\n"
                "    FLUSH PRIVILEGES;\n"
                "  \"\n"
            )


@unittest.skipUnless(canAccessLocalMySQL(), "Requires local MySQL at 127.0.0.1")
class TestLocalMySQLWithDatabase(env.DCCLabTestCase):
    localURL = "mysql://test:test@127.0.0.1/test"
    tableName = "test_local_db"

    def setUp(self):
        super().setUp()
        self.db = Database(self.localURL)
        self.db.execute(f"CREATE TABLE IF NOT EXISTS {self.tableName} (id INT PRIMARY KEY, name VARCHAR(100), value DOUBLE)")
        self.db.execute(f"DELETE FROM {self.tableName}")
        self.db.execute(f"INSERT INTO {self.tableName} (id, name, value) VALUES (1, 'alpha', 1.5)")
        self.db.execute(f"INSERT INTO {self.tableName} (id, name, value) VALUES (2, 'beta', 2.5)")
        self.db.commit()

    def tearDown(self):
        if self.db.isConnected:
            self.db.execute(f"DELETE FROM {self.tableName}")
            self.db.commit()
            self.db.disconnect()
        super().tearDown()

    def testIsConnected(self):
        self.assertTrue(self.db.isConnected)

    def testDisconnect(self):
        self.db.disconnect()
        self.assertFalse(self.db.isConnected)
        self.assertIsNone(self.db.cursor)

    def testContextManager(self):
        with Database(self.localURL) as db2:
            self.assertTrue(db2.isConnected)
        self.assertFalse(db2.isConnected)

    def testTables(self):
        tables = self.db.tables
        self.assertIn(self.tableName, tables)

    def testSelect(self):
        rows = self.db.select(self.tableName)
        self.assertEqual(len(rows), 2)

    def testSelectWithCondition(self):
        rows = self.db.select(self.tableName, 'name', 'id=1')
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['name'], 'alpha')

    def testFetchAll(self):
        self.db.execute(f"SELECT * FROM {self.tableName}")
        rows = self.db.fetchAll()
        self.assertEqual(len(rows), 2)

    def testFetchOne(self):
        self.db.execute(f"SELECT * FROM {self.tableName} ORDER BY id")
        row = self.db.fetchOne()
        self.assertEqual(row['id'], 1)
        row = self.db.fetchOne()
        self.assertEqual(row['id'], 2)
        row = self.db.fetchOne()
        self.assertIsNone(row)

    def testExecuteSelectOne(self):
        result = self.db.executeSelectOne(f"SELECT name FROM {self.tableName} WHERE id=1")
        self.assertEqual(result, 'alpha')

    def testExecuteSelectFetchInt(self):
        result = self.db.executeSelectFetchInt(f"SELECT COUNT(*) FROM {self.tableName}")
        self.assertEqual(result, 2)

    def testExecuteSelectFetchOneRow(self):
        row = self.db.executeSelectFetchOneRow(f"SELECT * FROM {self.tableName} WHERE id=1")
        self.assertEqual(row['id'], 1)
        self.assertEqual(row['name'], 'alpha')

    def testExecuteSelectFetchOneField(self):
        values = self.db.executeSelectFetchOneField(f"SELECT name FROM {self.tableName} ORDER BY id")
        self.assertEqual(values, ['alpha', 'beta'])

    def testBeginEndTransaction(self):
        self.db.beginTransaction()
        self.db.execute(f"INSERT INTO {self.tableName} (id, name, value) VALUES (3, 'gamma', 3.5)")
        self.db.endTransaction()
        rows = self.db.select(self.tableName)
        self.assertEqual(len(rows), 3)

    def testRollbackTransaction(self):
        self.db.beginTransaction()
        self.db.execute(f"INSERT INTO {self.tableName} (id, name, value) VALUES (4, 'delta', 4.5)")
        self.db.rollbackTransaction()
        rows = self.db.select(self.tableName)
        self.assertEqual(len(rows), 2)

    def testEnforceForeignKeys(self):
        self.db.enforceForeignKeys()
        self.db.execute("SELECT @@SESSION.foreign_key_checks")
        row = self.db.fetchOne()
        self.assertEqual(list(row.values())[0], 1)

    def testDisableForeignKeys(self):
        self.db.disableForeignKeys()
        self.db.execute("SELECT @@SESSION.foreign_key_checks")
        row = self.db.fetchOne()
        self.assertEqual(list(row.values())[0], 0)


@unittest.skipUnless(canAccessLocalMySQL(), "Requires local MySQL at 127.0.0.1")
class TestLocalMySQLWithMySQLDatabase(env.DCCLabTestCase):
    localURL = "mysql://test:test@127.0.0.1/test"
    tableName = "test_local_mysqldb"

    def setUp(self):
        super().setUp()
        self.db = MySQLDatabase(self.localURL)
        self.db.execute(f"CREATE TABLE IF NOT EXISTS {self.tableName} (id INT PRIMARY KEY, name VARCHAR(100), value DOUBLE)")
        self.db.execute(f"DELETE FROM {self.tableName}")
        self.db.execute(f"INSERT INTO {self.tableName} (id, name, value) VALUES (1, 'alpha', 1.5)")
        self.db.execute(f"INSERT INTO {self.tableName} (id, name, value) VALUES (2, 'beta', 2.5)")
        self.db.commit()

    def tearDown(self):
        if self.db.isConnected:
            try:
                self.db.cursor.fetchall()
            except Exception:
                pass
            self.db.execute(f"DELETE FROM {self.tableName}")
            self.db.commit()
            self.db.disconnect()
        super().tearDown()

    def testIsConnected(self):
        self.assertTrue(self.db.isConnected)

    def testDisconnect(self):
        self.db.disconnect()
        self.assertFalse(self.db.isConnected)
        self.assertIsNone(self.db.cursor)

    def testContextManager(self):
        with MySQLDatabase(self.localURL) as db2:
            self.assertTrue(db2.isConnected)
        self.assertFalse(db2.isConnected)

    def testTables(self):
        tables = self.db.tables
        self.assertIn(self.tableName, tables)

    def testSelect(self):
        rows = self.db.select(self.tableName)
        self.assertEqual(len(rows), 2)

    def testSelectWithCondition(self):
        rows = self.db.select(self.tableName, 'name', 'id=1')
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['name'], 'alpha')

    def testFetchAll(self):
        self.db.execute(f"SELECT * FROM {self.tableName}")
        rows = self.db.fetchAll()
        self.assertEqual(len(rows), 2)

    def testFetchOne(self):
        self.db.execute(f"SELECT * FROM {self.tableName} ORDER BY id")
        row = self.db.fetchOne()
        self.assertEqual(row['id'], 1)
        row = self.db.fetchOne()
        self.assertEqual(row['id'], 2)
        row = self.db.fetchOne()
        self.assertIsNone(row)

    def testExecuteSelectOne(self):
        result = self.db.executeSelectOne(f"SELECT name FROM {self.tableName} WHERE id=1")
        self.assertEqual(result, 'alpha')

    def testExecuteSelectFetchInt(self):
        result = self.db.executeSelectFetchInt(f"SELECT COUNT(*) FROM {self.tableName}")
        self.assertEqual(result, 2)

    def testExecuteSelectFetchOneRow(self):
        row = self.db.executeSelectFetchOneRow(f"SELECT * FROM {self.tableName} WHERE id=1")
        self.assertEqual(row['id'], 1)
        self.assertEqual(row['name'], 'alpha')

    def testExecuteSelectFetchOneField(self):
        values = self.db.executeSelectFetchOneField(f"SELECT name FROM {self.tableName} ORDER BY id")
        self.assertEqual(values, ['alpha', 'beta'])

    def testBeginEndTransaction(self):
        self.db.beginTransaction()
        self.db.execute(f"INSERT INTO {self.tableName} (id, name, value) VALUES (3, 'gamma', 3.5)")
        self.db.endTransaction()
        rows = self.db.select(self.tableName)
        self.assertEqual(len(rows), 3)

    def testRollbackTransaction(self):
        self.db.beginTransaction()
        self.db.execute(f"INSERT INTO {self.tableName} (id, name, value) VALUES (4, 'delta', 4.5)")
        self.db.rollbackTransaction()
        rows = self.db.select(self.tableName)
        self.assertEqual(len(rows), 2)

    def testEnforceForeignKeys(self):
        self.db.enforceForeignKeys()
        self.assertEqual(self.db.areForeignKeysEnforced(), 1)

    def testDisableForeignKeys(self):
        self.db.disableForeignKeys()
        self.assertEqual(self.db.areForeignKeysEnforced(), 0)


if __name__ == '__main__':
    unittest.main()
