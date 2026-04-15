from business import ImportService
from data_access import CsvPostReader, SqlAlchemyPostRepository
from interfaces import IImportService


def build_import_service(db_url: str) -> IImportService:
    csv_reader = CsvPostReader()
    repository = SqlAlchemyPostRepository(db_url=db_url)
    return ImportService(csv_reader=csv_reader, repository=repository)
