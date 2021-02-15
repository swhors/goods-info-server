import sqlite3
from app.model.category import Category
from app.model import _db_name_ as db_name
from app.model.sqlite.sqlite import SqLite, WhereConType, WheresData


class CategoryModel(SqLite):


    def __init__(self):
        print("create CategoryModel")
        super(CategoryModel, self).__init__(Category._table_name_,Category.create_table())


    def __del__(self):
        super(CategoryModel, self).__del__()
        print("delete CategoryModel")


    def incCategoryCount(self, title: str):
        rowsCnt, rows = super().select(None,
            [WheresData(Category._col_title_,title, WhereConType.NONE)],
            "", 0)
        if rowsCnt <= 0:
            super().insert({Category._col_title_:title})
        else:
            super().update(
               {Category._col_cnt_:f'{Category._col_cnt_}+1'},
               [WheresData(Category._col_title_,title, WhereConType.NONE)])


    @classmethod
    def rowToCategoryAll(self, items:[]) -> Category:
        if len(items) == 3:
            return Category(items[0],items[1], items[2])
        return None


    def getCategories(self):
        rowsCnt, categories = super().selectAll(
            f'order by {Category._col_cnt_} desc', 10,
            CategoryModel.rowToCategoryAll
        )
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
