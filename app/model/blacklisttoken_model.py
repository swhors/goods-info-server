import sqlite3
from app.model.data.blacklisttoken import BlacklistToken
from app.model import _db_name_ as db_name
from app.util.sqlite.sqlite import SqLite, WhereConType, WheresData


class BlacklistTokenModel(SqLite):
    def __init__(self):
        pass
