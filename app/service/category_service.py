import sqlite3
from app.model.category import Category
from app.model import _db_name_ as db_name
from app.util.sqlite.sqlite import SqLite, WhereConType, WheresData


class CategoryService(SqLite):

    def __init__(self):
        print("create CategoryService")
        super(CategoryService, self).\
            __init__(Category._table_name_,Category.create_table())


    def __del__(self):
        super(CategoryService, self).__del__()
        print("delete CategoryService")


    def inc_category_count(self, title: str):
        rowsCnt, rows = super().select(None,
            [WheresData(Category._col_title_,title, WhereConType.NONE)],
            "", 0)
        print(f'result = {rowsCnt}, {rows}')
        if rowsCnt <= 0:
            super().insert({Category._col_title_:title})
        else:
            super().update(
               {Category._col_cnt_:f'{Category._col_cnt_}+1'},
               [WheresData(Category._col_title_,title, WhereConType.NONE)])


    def del_category(self, title: str = None):
        if (title != None):
            wheres = {Category._col_title_:title}
        super().delete(wheres = wheres)


    @classmethod
    def row_2_category_all(cls, items:[]) -> Category:
        if len(items) == 3:
            return Category(items[0],items[1], items[2])
        return None


    def get_categories(self):
        rowsCnt, categories = super().select_all(
            f'order by {Category._col_cnt_} desc', 10,
            CategoryService.row_2_category_all
        )
        return categories


if __name__=="__main__":
    category = CategoryService()
    title: str = input("Type something to test this ( to exit type exit): ")
    while title != 'exit':
        category.incCategoryCount(title)
        category.incCategoryCount(title)
        category.incCategoryCount(title)
        categories = category.getCategories()
        for ca in categories:
            print(ca)
        title: str = input("Type something to test this ( to exit type exit): ")
