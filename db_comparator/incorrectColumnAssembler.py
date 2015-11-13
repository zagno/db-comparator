import pandas as pd

class IncorrectColumnAssembler:

    def populate(self, dto):

        result = {}

        for table in dto.sourceTables:
            incorrectColumns = {}
            missingColumns   = []

            if table in dto.excludedTables:
                continue

            if table in dto.missingTables:
                continue

            if table in dto.missingColumns:
                missingColumns = dto.missingColumns[table]

            sourceColumns  = dto.sourceInspector.get_columns(table)
            destColumns    = dto.destInspector.get_columns(table)

            incorrectColumns = self._incorrectColumns(sourceColumns, destColumns, missingColumns)

            if incorrectColumns:
                result[table] = incorrectColumns

        dto.incorrectColumns = result

    def _incorrectColumns(self, sourceColumns, destColumns, missingColumns):
        incorrectColumns = {}

        for sourceColumn in sourceColumns:
            if sourceColumn['name'] in missingColumns:
                continue

            destColumn  = self._getColumnByName(destColumns, sourceColumn['name'])
            differences = self._columnDifferent(sourceColumn, destColumn)

            if differences:
                data = {}

                for column in differences:
                    if column in sourceColumn and column in destColumn:
                        # print(column, sourceColumn[column], destColumn[column])
                        #column = str(column)
                        data[column] = [sourceColumn[column], destColumn[column]]

                incorrectColumns[sourceColumn['name']] = data

        return incorrectColumns

    def _columnDifferent(self, sourceColumn, destColumn):
        # Cast all value to string,  SqlAclchemy has its own objects for the `type`, which does not play well with Pandas
        for key in sourceColumn:
            sourceColumn[key] = str((sourceColumn[key]))

        for key in destColumn:
            destColumn[key] = str((destColumn[key]))

        dataFrame = pd.DataFrame.from_dict(
            [sourceColumn, destColumn],
            orient='columns'
        )

        differences           = dataFrame.eq(dataFrame.iloc[0], axis=1) #compare by row, obviously the first row will match
        columnList            = differences.apply(lambda x: x.argmin(), axis = 0)
        missingColumnNameList = columnList.index[columnList == 1].values

        if len(missingColumnNameList) > 0:
            return list(missingColumnNameList)

        return []

    def _getColumnByName(self, columns, name):

        for column in columns:
            if column['name'] != name:
                continue

            return column

        return []

