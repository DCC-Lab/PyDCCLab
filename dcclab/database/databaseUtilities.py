import os
import re


def findFiles(directory, extension) -> list:
    # Although os.walk is slow, I haven't found a faster way to find files in a directory and sub directories.
    # In python 3.x, os.walk was modified to use os.scandir, which greatly improved its performances. I doubt
    # there is a faster way to do this.
    filesFound = []
    for root, directories, files in os.walk(os.path.normpath(directory)):
        for file in files:
            if re.search(r'^.*\.{}$'.format(extension), file, re.IGNORECASE):
                filesFound.append(os.path.join(root, file))
    return filesFound


def sqliteDataTypes() -> list:
    # This is a list of data types and affinities for sqlite entries. Used to check if a type is valid.
    # A couple of precisions.
    # CHARACTER(20), VARCHAR(255), VARYING CHARACTER(255), NCHAR(55), NATIVE CHARACTER(70), NVARCHAR(100)
    # DECIMAL(10,5)
    return ['INT', 'INTEGER', 'TINYINT', 'SMALLINT', 'MEIDUMINT', 'BIGINT', 'UNSIGNED BIG INT', 'INT2', 'INT8',
            r'CHARACTER\(([1-9]|1\d|20)\)|CHARACTER$',
            r'VARCHAR\(([1-9]|\d{2}|1\d{2}|2[0-4]\d|2[0-5][0-5])\)|VARCHAR$',
            r'VARYING CHARACTER\(([1-9]|\d{2}|1\d{2}|2[0-4]\d|2[0-5][0-5])\)|VARYING CHARACTER$',
            r'NCHAR\(([1-9]|[1-4]\d|5[0-5])\)|NCHAR$', r'NATIVE CHARACTER\(([1-9]|[1-6]\d|70)\)|NATIVE CHARACTER$',
            r'NVARCHAR\(([1-9]|\d{2}|100)\)|NVARCHAR$', 'TEXT', 'CLOB', 'BLOB', 'REAL', 'DOUBLE', 'DOUBLE PRECISION',
            'FLOAT', 'NUMERIC', 'DECIMAL(10,5)', 'BOOLEAN', 'DATE', 'DATETIME']


def checkIfValidDataType(dataType: str) -> bool:
    for dType in sqliteDataTypes():
        if re.search(dType, dataType, re.IGNORECASE):
            return True
    return False


if __name__ == '__main__':
    dType = ''
    print(checkIfValidDataType(dType))
    dType = 'INT'
    print(checkIfValidDataType(dType))
    dType = 'character(20)'
    print(checkIfValidDataType(dType))
    dType = 'varChar(255)'
    print(checkIfValidDataType(dType))
    dType = 'Varying Character(255)'
    print(checkIfValidDataType(dType))
    dType = 'NCHAR(55)'
    print(checkIfValidDataType(dType))
    dType = 'NATIVE CHARACTER(70)'
    print(checkIfValidDataType(dType))
    dType = 'NVARchar(100)'
    print(checkIfValidDataType(dType))
    dType = 'Decimal(11,5)'
    print(re.search(r'DECIMAL\((\d|10,[1-5])\)|DECIMAL', dType, re.IGNORECASE))
    pass