from datetime import datetime

import peewee as pw

db = pw.SqliteDatabase("bot_history.db")


class ModelBase(pw.Model):
    created_at = pw.DateField(default=datetime.now())

    class Meta:
        database = db


class History(ModelBase):
    user_id = pw.TextField()
    date = pw.TextField()
    movie_info = pw.TextField()
