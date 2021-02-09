import sqlite3
import enum
from app.model.sqlite import _db_name_ as db_name

class WhereConType(enum.Enum):
    NONE = 0
    AND = 1
    OR = 3

class WheresData:
    def __init__(self, key: str, val, where_con_type: WhereConType ):
        self._key_ = key
        self._val_ = val
        self._where_con_type_ = where_con_type


    def key(self) -> str:
        return self._key_


    def val(self):
        return self._val_


    def where_con_type(self) -> WhereConType:
        return self._where_con_type_


class SqLite:
    _table_name_: str = ''

    def __init__(self, table_name: str, create_query: str):
        print("create SqLite")
        self._conn_ = sqlite3.connect(db_name, check_same_thread=False)
        cur = self._conn_.cursor() # 2. 커서 생성 (트럭, 연결로프)
        cur.execute(create_query)
        cur.close()


    def __del__(self):
        print("delete SqLite")
        self._conn_.close()

        cur = self.conn.cursor()
        cur.execute(sql1)
        rows = cur.fetchall()
        if len(rows) > 0:
            cur.execute(sql2)
        else:
            cur.execute(sql3)
        self.conn.commit()
        cur.close()


    def select(self,
               cols: [],
               table_name: str,
               wheres: [],
               orderby: str,
               limit_num: int):
        if cols == None or len(cols) == 0:
            select_cols = "*"
        else:
            select_cols = (',').join(cols)

        select_where = ""

        if wheres != None and len(wheres) == 1:
            select_where += "where "
            for where in wheres:
                if 'str' in str(type(where.val())):
                    select_where +=\
                        f'{where.key()}=\'{where.val()}\''
                else:
                    select_where +=\
                        f'{where.key()}={where.val()}'
                # if where.where_con_type() == WhereConType.None:
                #     select_where += ' '
                # else:
                #     select_where += f' {where.where_con_type().name}'

        limit_num_str = ""
        if limit_num > 0:
            limit_num_str = f'limit {limit_num}'

        sql = f'select {select_cols} from {table_name}' + \
              f' {select_where} {orderby} {limit_num_str};'

        print(f'query={sql}')

        cursor = self._conn_.cursor()

        cursor.execute(sql)

        datas = cursor.fetchall()

        cursor.close()

        return datas


    def insert(self, table_name: str, keyval:{}):

        keys = keyval.keys()

        table_cols = ", ".join(keys)

        table_vals_list = []
        for key in keys:
            if type(keyval[key]) == 'int':
                table_vals_list.append(f'{keyval[key]}')
            else:
                table_vals_list.append(f'\'{keyval[key]}\'')
        table_vals = ', '.join(table_vals_list)

        sql = f'insert into {table_name}({table_cols}) values({table_vals});'

        cursor = self._conn_.cursor()
        cursor.execute(sql)
        cursor.close()
        self._conn_.commit()

    def delete(self, table_name: str, wheres: []):
        delete_where =""
        if wheres != None and len(wheres) == 1:
            delete_where += "where "
            for where in wheres:
                if type(where.val()) == 'str':
                    delete_where +=\
                        f'{where.key()}=\'{where.val()}\''
                else:
                    delete_where +=\
                        f'{where.key()}={where.val()}'
                if where.where_con_type() != WhereConType.NONE:
                    delete_where += f' {where.where_con_type().name} '
                else:
                    delete_where += ' '

        sql = f'delete from {table_name} {delete_where};'

        cursor = self._conn_.cursor()
        cursor.execute(sql)
        cursor.close()

        self._conn_.commit()


    def deleteAll(self, table_name: str):
        self.delete(self, table_name=table_name, wheres=None)

    def selectAll(self, table_name: str, orderby: str, limit_num: int):
        return self.select(self, cols=None, table_name=table_name, \
                           wheres=None, orderby=orderby, limit_num=limit_num)
