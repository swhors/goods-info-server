import sqlite3
from app.model.user import User
from app.model import _db_name_ as db_name
from app.util.sqlite.sqlite import SqLite, WhereConType, WheresData


class UserService(SqLite):

    def __init__(self):
        print("create UserService")
        super(UserService, self).\
              __init__(User._table_name_, User.create_table())


    @classmethod
    def row_2_user(cls, items:[]) -> User:
        print(f'conver items = {items}')
        if len(items) == 6:
            user = User(items[1], items[2],
                        items[3], items[4])
            user.id = items[0]
            user.created = items[5]
            print(f'row_2_user, user={user}')
            return user
        return None


    def get_where_only_id(self, userid: str) -> []:
        wheres = []
        where1 = WheresData(User._col_userid_,
                            userid,
                            WhereConType.NONE)
        wheres.append(where1)

        return wheres


    def get_user(self, userid: str, get_val: bool = True) -> (bool, User):
        print(f'find_user, user_id={userid}')

        if get_val == True:
            conv_callback = UserService.row_2_user
        else:
            conv_callback = None

        wheres = self.get_where_only_id(userid)

        cnt, user = super().select(
                cols = None,
                wheres = wheres,
                orderby = None,
                limit_num = 0,
                conv_callback = conv_callback)

        if cnt > 0:
            if user != None and len(user) > 0:
                print(f'get_user, user={user}')
                return True, user[0]
            else:
                return True, None

        return False, None


    def add_user(self,
                 userid: str,
                 username: str,
                 email: str,
                 password: str) -> bool:
        ret, user = self.get_user(userid, False)

        print(f'add_user = {ret}, {user}')

        if ret == True:
            return False

        allcolums = {
            User._col_userid_:userid,
            User._col_username_:username,
            User._col_email_:email,
            User._col_password_:password
        }

        super().insert(keyval=allcolums)

        return True


    def del_user(self, userid: str):

        ret, user = self.get_user(userid, False)

        print(f'del_user = {ret}, {user}')

        if ret == False:
            return False

        super().delete(self.get_where_only_id(userid))

        return True
