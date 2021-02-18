import json

from app.model.data.goods import Goods

class GoodsResponse:

    len: int
    goods: []


    def __init__(self, len: int, goods: []):
        self.len = len
        self.goods = goods


    def __del__(self):
        pass


    def __str__(self):
        return f'len={self.len},' + \
               f'goods={self.goods}'


    def toJson(self):
        return json.dumps(self,
                          default=lambda o: o.__dict__,
                          sort_keys=True,
                          indent=4)


if __name__=='__main__':
    print(__name__)
    goods = GoodsResponse(1, [Goods(1, "test", 1)])
    print(goods)
    print(goods.toJson())
