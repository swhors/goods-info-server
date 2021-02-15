# app/goods/category_ctl.py

from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import current_app as app
from flask import jsonify
import json

from app.model.category import Category
from app.model.category_model import CategoryModel

category_model = CategoryModel()


category_ctl=Blueprint('category_ctl', __name__, url_prefix='/category')


@category_ctl.route('/get', methods=['GET'])
def goods_get():
    return jsonify({"result":"Ok"})


@category_ctl.route('/get_categories', methods=['GET'])
def get_categories():
    cas = category_model.get_categories()
    cas_jsons = []
    for ca in cas:
        print(ca.toJson())
        cas_jsons.append(ca.toJson())
    return jsonify({"len":len(cas_jsons), "categories":cas_jsons})


@category_ctl.route('/del_category', methods=['POST'])
def del_category():
    params = request.args.to_dict()
    if len(params) == 0 or Category._col_title_ not in params.keys():
        category_model.delete(None)
    else:
        category_model.delete(params[Category._col_title_])

    return jsonify({"result":"ok"})


@category_ctl.route('/inc_category_count/<title>', methods=['POST'])
def inc_category_count(title: str):
    category_model.inc_category_count(title)
    return jsonify({"result":"Ok"})
