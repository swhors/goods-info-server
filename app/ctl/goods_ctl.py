# app/goods/goods.py

from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import current_app as app
from flask import jsonify
import json

from app.lib.sqlite.category import Category
from app.lib.sqlite.category_model import CategoryModel
from app.lib.sqlite.goods import Goods
from app.lib.sqlite.goods_model import GoodsModel

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

@goods_ctl.route('/add_goods')
def add_goods_with_id():
    params = json.loads(request.get_data(), encoding='utf-8')
    if len(params) == 0:
        return josnify({"result":"false", "reson":"no parameter"})
    goods_name = param[Goods._col_name_]
    return josnify({"result":"ok"})
