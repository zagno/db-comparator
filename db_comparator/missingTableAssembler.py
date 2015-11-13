import re

class MissingTableAssembler:

    def populate(self, dto, excludeRegex = None):
        sourceTables = sorted(dto.sourceInspector.get_table_names())
        destTables   = sorted(dto.destInspector.get_table_names())

        dto.sourceTables = sourceTables
        dto.destTables   = destTables

        dto.missingTables = tuple(set(sourceTables) - set(destTables))

        for table in dto.sourceTables:
            if excludeRegex and re.match(excludeRegex, table):
                dto.excludedTables.append(table)
