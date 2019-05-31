# Overview
The database folder contains everything relative to the database programming and the management of metadata sources which must then be added to the database.
* DatabaseManagement contains the files related to the management of access, connections, commits, executes and handling of anything related to the database itself. It also contains the files that enables reading from csv files and translating those to a table entry in the database.
* CziMetadataManagement contains the files related to the conversion of metadata from a Carl Zeiss Image format file to a metadata object.
* MetadataToCsvManagement contains the files related to turning a metadata object to a csv file, which can then be passed onto the database object and into a table of the database itself.