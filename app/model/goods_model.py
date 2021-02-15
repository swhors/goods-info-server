import sqlite3
from app.model.goods import Goods
from app.model import _db_name_ as db_name
from app.model.sqlite.sqlite import SqLite, WhereConType, WheresData
from multipledispatch import dispatch
from multimethods import multimethod


class GoodsModel(SqLite):
    def __init__(self):
        print("create GoodsModel")
        super(GoodsModel, self).__init__(Goods._table_name_,Goods.create_table())


    def __del__(self):
        super(GoodsModel, self).__del__()
        print("delete GoodsModel")


    @classmethod
    def rowToGoodsAll(self, items:[]) -> Goods:
        print(f'conver items = {items}')
        if len(items) == 10:
            goods = Goods(items[0], items[1],
                         items[2], items[3],
                         items[4], items[5],
                         items[6], items[7],
                         items[9])
            goods.cnt = items[8]
            return goods
        return None


    def getGoods(self,
                 name: str = None,
                 goods_id: int = -1,
                 sel_limit: int = 10):
        if name == None:
            cnt, categories = super().selectAll(
                orderby = f'order by {Goods._col_goods_id_} desc',
                limit_num = sel_limit,
                conv_callback = GoodsModel.rowToGoodsAll)
        else:
            wheres = {Goods._col_name_:name}
            if goods_id > 0:
                wheres[Goods._col_goods_id_] = goods_id
            cnt, categories = super().select(
                cols = None,
                wheres = wheres,
                orderby = f'order by {Goods._col_goods_id_} desc',
                limit_num = sel_limit,
                conv_callback = GoodsModel.rowToGoodsAll)
        return cnt, categories


    def deleteGoods(self, name: str, goods_id: int, mall_name: str):
        sql = f"delete from {Goods._table_name_} \n" +\
              f"    where {Goods._col_name_}={name} and \n" +\
              f"          {Goods._col_id_}={goods_id} and \n" +\
              f"          {Goods._col_mall_name_}={mall_name};"
        cur = self.conn.cursor()
        cur.execute(sql)
        cur.close()


    def deleteAll(self):
        super().deleteAll()


    def insertGoodsClass(self, goods: Goods):
        self.insertGoods(name = goods.name,\
                        goods_id = goods.goods_id,\
                        goods_url = goods.goods_url,\
                        image_url = goods.image_url,\
                        mall_name = goods.mall_name,\
                        lprice = goods.lprice,\
                        hprice = goods.hprice,\
                        updated = goods.updated)


    def insertGoods(self, name: str, goods_id: int,
                    goods_url: str, image_url: str,
                    mall_name: str, lprice: int,
                    hprice: int, updated: int):
        wheres = [WheresData(Goods._col_name_,name, WhereConType.AND),\
                  WheresData(Goods._col_goods_id_,goods_id, WhereConType.NONE)]

        allcolums = {
            Goods._col_name_:name,
            Goods._col_goods_id_:goods_id,
            Goods._col_goods_url_:goods_url,
            Goods._col_image_url_:image_url,
            Goods._col_mall_name_:mall_name,
            Goods._col_lprice_:lprice,
            Goods._col_hprice_:hprice,
            Goods._col_updated_:updated
        }

        updateColumns = {
            Goods._col_lprice_:lprice,
            Goods._col_hprice_:hprice,
            Goods._col_updated_:updated
        }

        rowsCnt, rows = super().select(None, wheres, "", 0)

        print(f'insertGoods = {rowsCnt}, {rows}')

        if rowsCnt <= 0:
            super().insert(keyval=allcolums)
        else:
            super().update(keyval = updateColumns, wheres = wheres)


@dispatch(GoodsModel, Goods)
def insertGoods(self, goods: Goods):
    self.insertGoods(name = goods.name,\
                     goods_id = goods.goods_id,\
                     goods_url = goods.goods_url,\
                     image_url = goods.image_url,\
                     mall_name = goods.mall_name,\
                     lprice = goods.lprice,\
                     hprice = goods.hprice,\
                     updated = goods.updated)



user_guide = [\
        "Type goods name to test this ( to exit type exit): ",\
        "Type goods_id(integer) to test this ( to exit type exit): ",\
        "Type goods_url to test this ( to exit type exit): ",\
        "Type image_url to test this ( to exit type exit): ",\
        "Type mall_name to test this ( to exit type exit): ",\
        "Type lprice(integer) to test this ( to exit type exit): ",\
        "Type hprice(integer) to test this ( to exit type exit): ",\
        "Type updated(integer) to test this ( to exit type exit): "\
    ]


def get_insert_item() -> Goods:
    input_vals = []
    cnt = 0
    user_input = input(user_guide[cnt])
    while user_input != 'exit':
        input_vals.append(user_input)
        cnt += 1
        if cnt == 8:
            break
        else:
            print(f'cnt={cnt}')
            user_input = input(user_guide[cnt])

    if len(input_vals) == 8:
        return Goods(\
            name = input_vals[0], goods_id = int(input_vals[1]),\
            goods_url = input_vals[2], image_url = input_vals[3],\
            mall_name = input_vals[4], lprice = int(input_vals[5]),\
            hprice = int(input_vals[6]), updated = int(input_vals[7])
        )
    return None


if __name__=="__main__":
    goods = GoodsModel()
    user_guide0 = "Type enter or anything to input goods info " + \
                  "( to exit type exit): "
    title: str = input(user_guide0)
    while title != 'exit':
        item = get_insert_item()
        if item != None:
            print(f'Goods = {item}')
            goods.insertGoodsClass(goods = item)
        else:
            print('Illegal goods info.')
        title = input(user_guide0)
