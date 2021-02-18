# from app.main import db
import datetime

"""
Token Model for storing JWT tokens
"""
class BlacklistToken:

    _table_name_='blacklist'
    _col_id_='id'
    _col_token_='token'
    _col_created_='created'


    @property
    def id(self):
        return self._id_


    @id.setter
    def id(self, _id):
        self._id_ = _id


    @property
    def token(self):
        return self._token_


    @property
    def token(self, _token):
        self._token_ = _token


    @property
    def created(self):
        return self._created_


    @created.setter
    def created(self, _created):
        self._created_ = _created


    def __init__(self, token):
        self._id_ = 0
        self._token_ = token
        self._created_ = datetime.datetime.now()


    def __repr__(self) -> str:
        return "{" + \
               f'    \"id\":{self._id_},' +\
               f'    \"token\": {self._token_},' +\
               f'    \"creted\":{self._created_}' +\
               "}"


    @classmethod
    def create_table(cls) -> str:
        return f'create table if not exists {cls._table_name_} ( \n' +\
               f'    {cls._col_id_} integer primary key autoincrement, \n' +\
               f'    {cls._col_token_} text,  \n' +\
               f'    {cls._col_created_} datetime default current_timestamp);'


    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False
