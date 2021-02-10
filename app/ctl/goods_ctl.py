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
    #return json.dumps(ca)


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
    print(f'add_goods')
    if params != None:
        print(f'params={params}')
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
