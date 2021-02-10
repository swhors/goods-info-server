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

        rowsCnt, rows = super().select(None,
            Category._table_name_,
            [WheresData(Category._col_title_,title, WhereConType.NONE)],
            "", 0)
        if rowsCnt <= 0:
            super().insert(Category._table_name_,
                {Category._col_title_:title})
        else:
            super().update(Category._table_name_,
               {Category._col_cnt_:f'{Category._col_cnt_}+1'},
               [WheresData(Category._col_title_,title, WhereConType.NONE)])

    @classmethod
    def rowToCategoryAll(self, items:[]) -> Category:
        if len(items) == 3:
            return Category(items[0],items[1], items[2])
        return None


    """
    sql =f"select * from {Category._table_name_}\n" + \
         f"    order by {Category._col_cnt_} desc limit 10;"

    """
    def getCategories(self):
        rowsCnt, categories = super().select(None,
            Category._table_name_, None,
            f'order by {Category._col_cnt_} desc', 10,
            CategoryModel.rowToCategoryAll)
        return categories


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
