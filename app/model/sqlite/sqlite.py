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
        self._table_name_ = table_name
        self._conn_ = sqlite3.connect(db_name, check_same_thread=False)
        cur = self._conn_.cursor() # 2. 커서 생성 (트럭, 연결로프)
        cur.execute(create_query)
        cur.close()


    def __del__(self):
        print("delete SqLite")
        self._conn_.close()


    def make_wheres(self, wheres:{}) -> str:
        delete_where =""
        if wheres != None and len(wheres) == 1:
            delete_where += "where "
            for where in wheres:
                if 'str' in str(type(where.val())):
                    delete_where +=\
                        f'{where.key()}=\'{where.val()}\''
                else:
                    delete_where +=\
                        f'{where.key()}={where.val()}'
                if where.where_con_type() != WhereConType.NONE:
                    delete_where += f' {where.where_con_type().name} '
                else:
                    delete_where += ' '
        return delete_where


    def make_keyval(self, keyval:[], update_key: bool=True) -> str:
        set_strs = []
        set_keys = keyval.keys()
        operands = ['+','-','*','/']
        for key in set_keys:
            if 'str' in str(type(keyval[key])):
                if update_key == True:
                    operand = [ope for ope in operands if (ope in keyval[key])]
                    if len(operand) > 0:
                        set_strs.append(f'{key}={keyval[key]}')
                    else:
                        set_strs.append(f'{key}=\'{keyval[key]}\'')
                else:
                    set_strs.append(f'\'{keyval[key]}\'')
            else:
                if update_key == True:
                    set_strs.append(f'{key}=\'{keyval[key]}\'')
                else:
                    set_strs.append(f'{keyval[key]}')
        if len(set_keys) == 0:
            return ""

        return ', '.join(set_strs)


    def select(self,
               cols: [],
               wheres: [],
               orderby: str,
               limit_num: int,
               conv_callback = None) -> []:

        if cols == None or len(cols) == 0:
            select_cols = "*"
        else:
            select_cols = (',').join(cols)

        select_where = self.make_wheres(wheres)

        limit_num_str = ""
        if limit_num > 0:
            limit_num_str = f'limit {limit_num}'

        sql = f'select {select_cols} from {self._table_name_}' + \
              f' {select_where} {orderby} {limit_num_str};'

        print(f'query={sql}')

        cursor = self._conn_.cursor()

        cursor.execute(sql)

        datas = cursor.fetchall()

        return_list = []

        if conv_callback != None:
            for data in datas:
                obj = conv_callback(data)
                if obj != None:
                    return_list.append(obj)

        cursor.close()

        data_size = len(return_list)
        if data_size <= 0:
            data_size = len(datas)
        return data_size, return_list


    def insert(self, keyval:{}):

        keys = keyval.keys()

        table_cols = ", ".join(keys)

        table_vals = self.make_keyval(keyval, False)

        sql = f'insert into {self._table_name_}({table_cols}) values({table_vals});'
        print(f'query={sql}')

        cursor = self._conn_.cursor()
        cursor.execute(sql)
        cursor.close()
        self._conn_.commit()


    def delete(self, wheres: {}):

        delete_where = self.make_wheres(wheres)

        sql = f'delete from {self._table_name_} {delete_where};'
        print(f'query={sql}')

        cursor = self._conn_.cursor()
        cursor.execute(sql)
        cursor.close()

        self._conn_.commit()


    def delete_all(self):
        self.delete(wheres=None)


    def select_all(self,
                  orderby: str,
                  limit_num: int,
                  conv_callback = None):

        return self.select(\
            cols=[], \
            wheres=None,\
            orderby=orderby,\
            limit_num=limit_num,\
            conv_callback=conv_callback)


    def update(self, keyval: {}, wheres: []):
        update_where = self.make_wheres(wheres)
        update_keyval = self.make_keyval(keyval)
        if len(update_keyval) > 0 and len(update_where) > 0:
            sql = f'update {self._table_name_} set {update_keyval}' +\
                  f'    {update_where};'
            print(f'query={sql}')

            cursor = self._conn_.cursor()
            cursor.execute(sql)
            cursor.close()
            self._conn_.commit()
