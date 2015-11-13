from sqlalchemy.engine import reflection

class DatabaseComparisonDTO:
    def __init__(self, sourceSession, destSession):
        self.sourceTables     = []
        self.destTables       = []
        self.missingTables    = []
        self.excludedTables   = []
        self.missingColumns   = {}
        self.incorrectColumns = {}
        self.sourceInspector  = self.getInspectorFromSession(sourceSession)
        self.destInspector    = self.getInspectorFromSession(destSession)

    def getInspectorFromSession(self, session):
        return reflection.Inspector.from_engine(session.bind)

    def getValidTables(self):
         return tuple(set(self.sourceTables) - set(self.destTables) -  set(self.excludedTables) - set(self.missingTables))

    def __str__(self):
        stringy = ""
        tables  = list(self.incorrectColumns.keys()) + list(self.missingColumns.keys())

        for table in tables:
            stringy += table + '\n'

            if table in self.missingColumns:
                stringy += '\tMissing Columns:\n'
                for column in self.missingColumns[table]:
                    stringy += '\t\t' + column + '\n'

            if table in self.incorrectColumns:
                stringy += "\tIncorrect Columns:\n"
                for column, attributes in self.incorrectColumns[table].items():
                    stringy += '\t\t' + column + ' ('

                    for attribute, items in attributes.items():
                        stringy += attribute + " '" + items[0] + "' vs '" + items[1] + "', "

                    stringy = stringy[:-2]
                    stringy += ')\n'

        if self.missingTables:
            stringy += '\nMissing Tables:\n'

            for table in self.missingTables:
                stringy += '\t' + table + '\n'

        return stringy



