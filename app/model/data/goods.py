import json
from datetime import datetime
from collections import namedtuple
from json import JSONEncoder
from multipledispatch import dispatch


class Goods:
    _col_id_='id'
    _col_name_='name'
    _col_goods_id_='goods_id'
    _col_goods_url_='goods_url'
    _col_image_url_='image_url'
    _col_mall_name_='mall_name'
    _col_lprice_='lprice'
    _col_hprice_='hprice'
    _col_cnt_='cnt'
    _col_updated_='updated'
    _col_created_='created'
    _table_name_='goods'


    @classmethod
    def create_table(cls) -> str:
        return f"create table if not exists {cls._table_name_}( \n" +\
            f"    {cls._col_id_} integer primary key autoincrement, \n" +\
            f'    {cls._col_name_} text,  \n' +\
            f'    {cls._col_goods_id_} integer,  \n' +\
            f'    {cls._col_goods_url_} text,  \n' +\
            f'    {cls._col_image_url_} text,  \n' +\
            f'    {cls._col_mall_name_} text,  \n' +\
            f'    {cls._col_lprice_} integer,  \n' +\
            f'    {cls._col_hprice_} integer,  \n' +\
            f'    {cls._col_cnt_} integer,  \n' +\
            f'    {cls._col_updated_} datetime,  \n' +\
            f'    {cls._col_created_} datetime default current_timestamp);'


    def __init__(self,
                 name: str, goods_id: int,
                 goods_url: str, image_url: str,
                 mall_name: str, lprice: int,
                 hprice: int, cnt: int,
                 updated: int):
        self.id = 0
        self.name = name
        self.goods_id = goods_id
        self.goods_url = goods_url
        self.image_url = image_url
        self.mall_name = mall_name
        self.lprice = lprice
        self.hprice = hprice
        self.cnt = 1
        self.updated = updated
        self.created = 0


    def __del__(self):
        pass


    def __str__(self):
        return f'id={self.id},' + \
               f'name={self.name},' + \
               f'goods_id={self.goods_id},' + \
               f'goods_url={self.goods_url},' + \
               f'image_url={self.image_url},' + \
               f'mall_name={self.mall_name},' + \
               f'hprice={self.lprice},' + \
               f'hprice={self.hprice},' + \
               f'cnt={self.cnt},' + \
               f'updated={self.updated},' + \
               f'created={self.created}'


    def toJson(self):
        return json.dumps(self.__dict__)


    @staticmethod
    def fromJson(msg: str):
        return Goods()


class GoodsEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__


def goodsDecoder(goodsDict):
    return namedtuple('X', goodsDict.keys())(*goodsDict.values())


if __name__=='__main__':
    print(__name__)
    print(Goods.create_table())
    print(f'Table Name = {Goods._table_name_}')
    goods = Goods(1, "test", 123,
        "http:/1.1.1.1/your_shop.html",
        "http:/1.1.1.1/image.jpg",
        "your_shop",
        200, 300,
        19292929,1919119)
    print(goods)
    json_str = goods.toJson()
    print(f"Json = {json_str}")

    new_json_str = json.dumps(goods, indent=4, cls=GoodsEncoder)
    print(f"Json2 = {new_json_str}")

    new_goods = json.load(new_json_str, object_hook=goodsDecoder)

    print(new_goods)
