import sqlite3
from app.model.user import User
from app.model import _db_name_ as db_name
from app.util.sqlite.sqlite import SqLite, WhereConType, WheresData


class UserService(SqLite):

    def __init__(self):
        print("create UserModel")
        super(UserService, self).\
              __init__(User.table_name, User.create_table())


    @classmethod
    def row_2_user(cls, items:[]) -> User:
        print(f'conver items = {items}')
        if len(items) == 10:
            user = User(items[1], items[2],
                        items[3], items[4])
            user.id = items[0]
            user.created = item[5]
            return user


    def find_user(self, user_id: str) -> User:
        wheres = {User.userid:user_id}
        cnt, user = super().select(
                cols = None,
                wheres = wheres,
                orderby = None,
                limit_num = 1,
                conv_callback = UserModel.row_2_user)

        return user
