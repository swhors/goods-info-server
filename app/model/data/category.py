import json


class Category:
    _col_id_='id'
    _col_cnt_='cnt'
    _col_title_='title'
    _table_name_='category'


    @classmethod
    def create_table(cls) -> str:
        return f"create table if not exists {cls._table_name_} ( \n" +\
            f"    {cls._col_id_} integer primary key autoincrement, \n" +\
            f'    {cls._col_title_} text,  \n' +\
            f'    {cls._col_cnt_} integer default 1);'


    def __init__(self, id: int, title: str, cnt: int):
        self.title = title
        self.cnt = cnt
        self.id = id


    def __del__(self):
        pass


    def __str__(self):
        return f'{self._col_id_}={self.id},' + \
               f'{self._col_title_}={self.title},' + \
               f'{self._col_cnt_}={self.cnt}'


    def toJson(self):
        return json.dumps(self.__dict__)


if __name__=='__main__':
    print(__name__)
    print(Category.create_table())
    print(f'Table Name = {Category._table_name_}')
    print(Category(1, "test", 1))
    print(Category(1, "test", 1).toJson())
