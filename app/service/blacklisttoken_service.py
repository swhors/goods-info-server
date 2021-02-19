import sqlite3
from app.model.blacklisttoken import BlacklistToken
from app.model import _db_name_ as db_name
from app.util.sqlite.sqlite import SqLite, WhereConType, WheresData


class BlacklistTokenService(SqLite):

    def __init__(self):
        print("create BlacklistTokenService")
        super(BlacklistTokenService, self).\
            __init__(BlacklistToken._table_name_,\
                     BlacklistToken.create_table())

    @classmethod
    def row_2_token(cls, items:[]) -> BlacklistToken:
        if len(items) == 3:
            token = BlacklistToken(items[1])
            token.id = items[0]
            token.created = items[2]
            return token
        return None


    def make_where_with_token(self, token: str) -> []:
        wheres = []
        where1 = WheresData(BlacklistToken._col_token_,
                            token,
                            WhereConType.NONE)
        wheres.append(where1)
        return wheres


    def is_blacklist(self, token: str) -> bool:
        wheres = self.make_where_with_token(token)
        cols = [BlacklistToken._col_token_]

        cnt, tokens = super().select(cols = cols,\
                                     wheres = wheres,\
                                     orderby = None,\
                                     limit_num = 0,\
                                     conv_callback = None)

        if cnt > 0:
            return True

        return False


    def get_all_blacklist(self) -> []:
        len1, lists = super().select_all(
                    orderby=None,
                    limit_num = 100,
                    conv_callback=BlacklistTokenService.row_2_token)

        if len1 > 0:
            return True, lists

        return False, None


    def add_blacklist(self, token: str) -> bool:
        if self.is_blacklist(token):
            return False
        else:
            allcolums = {
                BlacklistToken._col_token_:token
            }
            super().insert(keyval=allcolums)
        return True


    def del_blacklist(self, token:str) -> bool:
        if self.is_blacklist(token):
            wheres = self.make_where_with_token(token)
            super().delete(wheres = wheres)
            return True
        return False
