from datetime import datetime

import peewee as pw

db = pw.SqliteDatabase("new_history.db")


class ModelBase(pw.Model):
    created_at = pw.DateField(default=datetime.now())

    class Meta:
        database = db


class History(ModelBase):
    date = pw.TextField()
    movie_info = pw.TextField()
