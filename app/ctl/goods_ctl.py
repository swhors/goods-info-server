# app/goods/goods.py

from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import current_app as app
from flask import jsonify
import json

from app.model.category import Category
from app.model.category_model import CategoryModel
from app.model.goods import Goods
from app.model.goods_model import GoodsModel

category_model = CategoryModel()
goods_model = GoodsModel()

goods_ctl=Blueprint('goods_ctl', __name__, url_prefix='/goods')


@goods_ctl.route('/get', methods=['GET'])
def goods_get():
    #return render_template('/main/index.html')
    return jsonify({"result":"Ok"})
    #return "hello"


@goods_ctl.route('/get_categories', methods=['GET'])
def get_categories():
    cas = category_model.getCategories()
    cas_jsons = []
    for ca in cas:
        print(ca.toJson())
        cas_jsons.append(ca.toJson())
    return jsonify({"len":len(cas_jsons), "categories":cas_jsons})


@goods_ctl.route('/inc_category_count/<title>', methods=['POST'])
def inc_category_count(title: str):
    category_model.incCategoryCount(title)
    return jsonify({"result":"Ok"})


@goods_ctl.route('/add_goods', methods=['POST'])
def add_goods_with_id():
    # params = json.loads(request.get_data(), encoding='utf-8')
    # if len(params) == 0:
    #     return josnify({"result":"false", "reson":"no parameter"})
    params = request.get_json(force=True)
    if params != None:
        goods_name = params[Goods._col_name_]
        goods_id = params[Goods._col_goods_id_]
        goods_url = params[Goods._col_goods_url_]
        image_url = params[Goods._col_image_url_]
        mall_name = params[Goods._col_mall_name_]
        lprice = params[Goods._col_lprice_]
        hprice = params[Goods._col_hprice_]
        updated = params[Goods._col_updated_]
        goods_model.insertGoods(
            name = goods_name,
            goods_id = goods_id,
            goods_url = goods_url,
            image_url = image_url,
            mall_name = mall_name,
            lprice = lprice,
            hprice = hprice,
            updated = updated
            )
        return jsonify({"result":"ok"})
    return jsonify({"result":"fail"})


@goods_ctl.route('/get_goods_with_id', methods=['POST'])
def get_goods_with_id():
    params = request.args.to_dict()
    if len(params) == 0 or Goods._col_name_ not in params.keys():
        return josnify({"result":"false", "reson":"no parameter"})
    print(f'get_goods')
    name = params[Goods._col_name_]
    if Goods._col_goods_id_ in params.keys():
        goods_id = int(params[Goods._col_goods_id_])
    else:
        goods_id = -1
    if 'limit' in params.keys():
        sel_limit = int(params['limit'])
    else:
        sel_limit = 20
    if name == '*':
        cnt, goods_list = goods_model.getGoods(name = None,
                                               goods_id = -1,
                                               sel_limit = sel_limit)
    else:
        cnt, goods_list = goods_model.getGoods(name = name,
                                               goods_id = goods_id,
                                               sel_limit = sel_limit)
    print(f'result={cnt}, \n       {goods_list}')
    goods_json_list = []

    for goods in goods_list:
        print(goods.toJson())
        goods_json_list.append(goods.toJson())

    return jsonify({"len":cnt, "goods":goods_json_list})
