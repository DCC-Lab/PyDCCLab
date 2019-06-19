'''
THIS FILE IS OBSOLETE.
SOME OF THE CODE MIGHT BE USEFUL LATER SO THE FILE IS KEPT FOR NOW.
ONCE THERE IS NO MORE USE FOR THE CODE, IT SHOULD BE DELETED.
'''
import sqlite3 as lite
import csv


def ExportTableToCSV(table):
    filename = str(table) + '.csv'
    with open(filename, 'w') as file:
        conn = lite.connect('test.db')
        cur = conn.cursor()

        file.write(CreateCSVHeader(cur))

        for row in cur.execute('SELECT * FROM ' + str(table)):
            line = ""
            for cell in row:
                line += str(cell) + ","
            line = str(line)[:-1] + "\n"
            file.write(line)
        file.close()
        cur.close()
        conn.close()


def CreateCSVHeader(dbCursor):
    reader = dbCursor.execute('PRAGMA TABLE_INFO({})'.format(table))
    firstline = ''
    secondline = ''
    for x in reader.fetchall():
        firstline += x[1] + ","
        secondline += x[2] + ","
    return firstline.rstrip(",") + "\n" + secondline.rstrip(",") + "\n"


def CSV_reader(filePath):
    with open(filePath) as file:
        return csv.reader(file)


def ReformatData(data):
    newData = []
    for line in data:
        line = str(line).replace('\n', '')
        line = str(line).split(',')
        if line[0] != '':
            newData.append(line)
    return newData


def ExtractColumns(data):
    columns = []
    for i in range(len(data[0])):
        columns.append([data[0][i], data[1][i]])
    return columns, data[2:]


def CommandCreateTable(columns, tablename):
    i = 0
    command = 'CREATE TABLE IF NOT EXISTS ' + tablename + ' ('
    for col in columns:
        if col[0] != "" and i == 0:
            command += col[0] + " " + col[1] + " PRIMARY KEY, "
        elif col[0] != "":
            command += col[0] + " " + col[1] + ", "
        else:
            command += "param_" + str(i) + " " + col[1] + ", "
        i += 1

    if tablename == 'souris':
        command = command.rstrip(", ")
        command += ")"
    elif tablename == 'utilisation':
        command += "FOREIGN KEY (no_souris) REFERENCES souris(no_souris_int))"
    return str(command)


def CommandInsertData(entry, entryType, tablename):
    command = "INSERT INTO " + tablename + " ("
    for type in entryType:
        command += "'" + str(type[0]) + "', "
    command = command.rstrip(", ") + ") VALUES ("
    for ent in entry:
        command += "'" + str(ent) + "', "
    command = command.rstrip(", ") + ")"
    return command


if __name__ == '__main__':
    # Last change on injections and souris db.
    # Create a use db?
    # Should non-injected mice still be in injections?
    lstFiles = ['Data_plateforme - souris.csv', 'Data_plateforme - utilisation.csv']
    lstTables = ['souris', 'utilisation']

    CreateTable = False
    if CreateTable:
        con = lite.connect('file:test.db?mode=rwc', uri=True)
        cursor = con.cursor()
        i = 0
        for file in lstFiles:
            lines = open(file).readlines()
            newlines = ReformatData(lines)
            columns, data = ExtractColumns(newlines)

            command = CommandCreateTable(columns, lstTables[i])
            i += 1
            cursor.execute(command)
            con.commit()

        cursor.close()
        con.close()

    FillTable = False
    if FillTable:
        con = lite.connect('file:test.db?mode=rwc', uri=True)
        cursor = con.cursor()
        i = 0
        for file in lstFiles:
            lines = open(file).readlines()
            newlines = ReformatData(lines)
            columns, data = ExtractColumns(newlines)
            for entry in data:
                comm = CommandInsertData(entry, columns, lstTables[i])
                cursor.execute(comm)
                con.commit()

            i += 1

        cursor.close()
        con.close()

    TabletoCSV = False
    if TabletoCSV:
        for table in lstTables:
            ExportTableToCSV(table)

