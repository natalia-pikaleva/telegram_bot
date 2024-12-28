from database.utils.CRUD import CRUDInterface
from database.common.models import db, History

db.connect()
db.create_tables([History])

crud = CRUDInterface()

db_write = crud.create()
db_read = crud.retrieve()

if __name__ == "__main__":
    crud()
