import sqlite3
from app.lib.sqlite.goods import Goods
from app.lib.sqlite import _db_name_ as db_name


class GoodsModel:

    def __init__(self):
        print("create mydata_goods")
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        cur = self.conn.cursor() # 2. 커서 생성 (트럭, 연결로프)
        cur.execute(Goods.create_table())
        cur.close()

    def __del__(self):
        print("delete mydata_goods")
        self.conn.close()

    def incCategoryCount(self, title: str):
        sql1 =f"select * from {Goods._table_name_} where title=\'{title}\';"
        sql2 =f"update {Goods._table_name_} set cnt=cnt + 1 \n" +\
              f"    where title= \'{title}\'"
        sql3 =f"insert into {Goods._table_name_}(title, cnt)\n" +\
              f"    values(\'{title}\',1);"

        cur = self.conn.cursor()
        cur.execute(sql1)
        rows = cur.fetchall()
        if len(rows) > 0:
            cur.execute(sql2)
        else:
            cur.execute(sql3)
        self.conn.commit()
        cur.close()

    def getGoods(self):
        categories = []
        sql =f"select * from {Goods._table_name_} order by cnt desc;"
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            if len(row) == 3:
                categories.append(Category(row[0],row[1], row[2]))
        cur.close()
        return categories

    def deleteGoods(self, name: str, goods_id: int, mall_name: str):
        sql = f"delete from {Goods._table_name_} \n" +\
              f"    where {Goods._col_name_}={name} and \n" +\
              f"          {Goods._col_id_}={goods_id} and \n" +\
              f"          {Goods._col_mall_name_}={mall_name};"
        cur = self.conn.cursor()
        cur.execute(sql)
        cur.close()

    def insertGoods(self, name: str, goods_id: int,
                    goods_url: str, image_url: str,
                    mall_name: str, lprice: int,
                    hprice: int, updated: int):
        sql1 =f"select * from {Goods._table_name_} \n" +\
              f"    where {Goods._col_goods_id_}={goods_id};"
        sql2 =f"insert into {Goods._table_name_} \n" +\
              f"    values(\'{name}\',\n" +\
              f"           {goods_id},\n" +\
              f"           \'{goods_url}\',\n" +\
              f"           \'{image_url}\',\n" +\
              f"           \'{mall_name}\',\n" +\
              f"           {lprice},\n" +\
              f"           {hprice},\n" +\
              f"           {updated});"
        cur = self.conn.cursor()
        cur.execute(sql1)
        rows = cur.fetchall()
        if len(rows) <= 0:
            cur.execute(sql2)
            self.conn.commit()
        cur.close()

if __name__=="__main__":
    goods = GoodsModel()
    title: str = input("Type something to test this ( to exit type exit): ")
    while title != 'exit':
        goods.incCategoryCount(title)
        goods.incCategoryCount(title)
        goods.incCategoryCount(title)
        goods = category.getCategories()
        for ca in categories:
            print(ca)
        title: str = input("Type something to test this ( to exit type exit): ")
