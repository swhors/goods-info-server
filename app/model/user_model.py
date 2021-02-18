import sqlite3
from app.model.data.user import User
from app.model import _db_name_ as db_name
from app.util.sqlite.sqlite import SqLite, WhereConType, WheresData


class UserModel(SqLite):
    def __init__(self):
        pass
