# app/goods/category_ctl.py

from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import current_app as app
from flask import jsonify
from flask_ssl import *
from flask_login import current_user, login_required

import json

from app.model.category import Category
from app.model.category_response import CategoryResonse
from app.service.category_service import CategoryService


category_model = CategoryService()


category_ctl=Blueprint('category_ctl', __name__, url_prefix='/category')


@category_ctl.route('/get', methods=['GET'])
@ssl_require
@login_required
def goods_get():
    return jsonify({"result":"Ok"})


@category_ctl.route('/get_categories', methods=['GET'])
@ssl_require
@login_required
def get_categories():
    cas = category_model.get_categories()
    response = CategoryResonse(len(cas), cas)
    return response.toJson()


@category_ctl.route('/del_category', methods=['POST'])
@ssl_require
@login_required
def del_category():
    params = request.args.to_dict()
    if len(params) == 0 or Category._col_title_ not in params.keys():
        category_model.delete(None)
    else:
        category_model.delete(params[Category._col_title_])

    return jsonify({"result":"ok"})


@category_ctl.route('/inc_category_count/<title>', methods=['POST'])
@ssl_require
@login_required
def inc_category_count(title: str):
    category_model.inc_category_count(title)
    return jsonify({"result":"Ok"})
