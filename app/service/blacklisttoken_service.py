import sqlite3
from app.model.blacklisttoken import BlacklistToken
from app.model import _db_name_ as db_name
from app.util.sqlite.sqlite import SqLite, WhereConType, WheresData


class BlacklistTokenService(SqLite):
    def __init__(self):
        pass
