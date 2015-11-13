from db_comparator import DatabaseComparisonDTO
from db_comparator import MissingTableAssembler
from db_comparator import MissingColumnAssembler
from db_comparator import IncorrectColumnAssembler

if __name__ == '__main__':

    srcDatabaseSession  = None #SQL Alchemy Session
    destDatabaseSession = None #SQL Alchemy Session

    dc = DatabaseComparisonDTO(srcDatabaseSession, destDatabaseSession)

    mta = MissingTableAssembler()
    mca = MissingColumnAssembler()
    ica = IncorrectColumnAssembler()

    mta.populate(dc, '^.*_[0-9]+$')
    mca.populate(dc)
    ica.populate(dc)

    print(dc)