import sqlite3
from app.model.category import Category
from app.model import _db_name_ as db_name
from app.model.sqlite.sqlite import SqLite, WhereConType, WheresData


class CategoryModel(SqLite):


    def __init__(self):
        super(CategoryModel, self).__init__(Category._table_name_,Category.create_table())
        print("create CategoryModel")
        # self.conn = sqlite3.connect(db_name, check_same_thread=False)
        # cur = self.conn.cursor() # 2. 커서 생성 (트럭, 연결로프)
        # cur.execute(Category.create_table())
        # cur.close()


    def __del__(self):
        print("delete CategoryModel")
        # self.conn.close()


    """
    Used Query
        sql1 =f"select * from {Category._table_name_} \n" + \
              f"    where title=\'{title}\';"
        sql2 =f"update {Category._table_name_} \n" +\
              f"    set {Category._col_cnt_}={Category._col_cnt_} + 1 \n" +\
              f"    where {Category._col_title_} = \'{title}\'"
        sql3 =f"insert into {Category._table_name_}({Category._col_title_})\n"+\
              f"    values(\'{title}\');"
    """
    def incCategoryCount(self, title: str):

        """
        def insert(self, table_name: str, keyval:{}):

        def select(self,
                   cols: [],
                   table_name: str,
                   wheres: [],
                   orderby: str,
                   limit_num: int):
        """

        rows = super().select(None,
            Category._table_name_,
            [WheresData(Category._col_title_,title, WhereConType.NONE)],
            "", 0)
        if len(rows) <= 0:
            super().insert(Category._table_name_,
                {Category._col_title_:title})
        else:
            pass


    def incCategoryCount1(self, title: str):
        sql1 =f"select * from {Category._table_name_} \n" + \
              f"    where title=\'{title}\';"
        sql2 =f"update {Category._table_name_} \n" +\
              f"    set {Category._col_cnt_}={Category._col_cnt_} + 1 \n" +\
              f"    where {Category._col_title_} = \'{title}\'"
        sql3 =f"insert into {Category._table_name_}({Category._col_title_})\n"+\
              f"    values(\'{title}\');"

        cur = self.conn.cursor()
        cur.execute(sql1)
        rows = cur.fetchall()
        if len(rows) > 0:
            cur.execute(sql2)
        else:
            cur.execute(sql3)
        self.conn.commit()
        cur.close()


    def getCategories(self):
        categories = []
        sql =f"select * from {Category._table_name_}\n" + \
             f"    order by {Category._col_cnt_} desc limit 10;"
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            if len(row) == 3:
                categories.append(Category(row[0],row[1], row[2]))
        cur.close()
        return categories


    def insertCategory(self, title: str):
        sql1 =f"select * from {Category._table_name_} \n" + \
              f"    where {Category._col_title_}=\'{title}\';"

        sql2 =f"insert into {Category._table_name_}(\n" + \
              f"            {Category._col_title_})\n" + \
              f"    values(\'{title}\');"
        cur = self.conn.cursor()
        cur.execute(sql1)
        rows = cur.fetchall()
        if len(rows) <= 0:
            cur.execute(sql2)
            self.conn.commit()
        cur.close()

if __name__=="__main__":
    category = CategoryModel()
    title: str = input("Type something to test this ( to exit type exit): ")
    while title != 'exit':
        category.incCategoryCount(title)
        category.incCategoryCount(title)
        category.incCategoryCount(title)
        categories = category.getCategories()
        for ca in categories:
            print(ca)
        title: str = input("Type something to test this ( to exit type exit): ")
