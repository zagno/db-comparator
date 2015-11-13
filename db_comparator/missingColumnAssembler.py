class MissingColumnAssembler:

    def populate(self, dto):

        result = {}

        for table in dto.sourceTables:
            if table in dto.excludedTables:
                continue

            if table in dto.missingTables:
                continue

            sourceColumns  = dto.sourceInspector.get_columns(table)
            destColumns    = dto.destInspector.get_columns(table)
            missingColumns = self._missingColumns(sourceColumns, destColumns)

            if missingColumns:
                result[table] = missingColumns

        dto.missingColumns = result

    def _missingColumns(self, sourceColumns, destColumns):
        missingColumns  = []

        for sourceColumn in sourceColumns:
            destColumnExists = self._columnExist(sourceColumn['name'], destColumns)

            if not destColumnExists:
                 missingColumns.append(sourceColumn['name'])

        return missingColumns


    def _columnExist(self, columnName, columns):
        for column in columns:
            if columnName != column['name']:
                continue

            return column
        return False
