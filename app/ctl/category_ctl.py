# app/goods/category_ctl.py

from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import current_app as app
from flask import jsonify
from flask_ssl import *
from flask_login import current_user, login_required
from flask_jwt_extended import jwt_required

import json

from app.model.category import Category
from app.model.category_response import CategoryResonse
from app.service.category_service import CategoryService

category_service = CategoryService()

category_ctl=Blueprint('category_ctl', __name__, url_prefix='/category')


@category_ctl.route('/get', methods=['GET'])
@ssl_require
@login_required
def goods_get():
    return jsonify({"result":"Ok"})


def get_categories_internal() -> str:
    cas = category_service.get_categories()
    response = CategoryResonse(len(cas), cas)
    return response.toJson()


def del_category_internal(request) -> str:
    params = request.args.to_dict()
    if len(params) == 0 or Category._col_title_ not in params.keys():
        category_service.delete(None)
    else:
        category_service.delete(params[Category._col_title_])

    return jsonify({"result":"ok"})


def inc_category_count_internal(title: str):
    category_service.inc_category_count(title)
    return jsonify({"result":"Ok"})


@category_ctl.route('/get_categories_in_login', methods=['GET'])
@ssl_require
@login_required
def get_categories_in_login():
    return get_categories_internal()


@category_ctl.route('/get_categories', methods=['GET'])
@jwt_required()
def get_categories():
    return get_categories_internal()


@category_ctl.route('/del_category_in_login', methods=['POST'])
@ssl_require
@login_required
def del_category_in_login():
    del_category_internal(request)


@category_ctl.route('/del_category', methods=['POST'])
@jwt_required()
def del_category():
    del_category_internal(request)


@category_ctl.route('/inc_category_count/<title>', methods=['POST'])
@ssl_require
@login_required
def inc_category_count_in_login(title: str):
    return inc_category_count_internal(title)


@category_ctl.route('/inc_category_count/<title>', methods=['POST'])
@jwt_required()
def inc_category_count(title: str):
    return inc_category_count_internal(title)
