from typing import Any, Dict, List, TypeVar
from ..common.models import db
from peewee import ModelSelect
from database.common.models import ModelBase


T = TypeVar('T')

def _store_date(db: db, model: T, *data: List[Dict]) -> None:
    with db.atomic():
        model.insert_many(*data).execute()

def _retrieve_all_date(db: db, model: T, *columns: ModelBase) -> ModelSelect:
    with db.atomic():
        response = model.select(*columns)

    return response

class CRUDInterface():
    @staticmethod
    def create():
        return _store_date

    @staticmethod
    def retrieve():
        return _retrieve_all_date

if __name__ == '__main__':
    _store_date()
    _retrieve_all_date()
    CRUDInterface()



