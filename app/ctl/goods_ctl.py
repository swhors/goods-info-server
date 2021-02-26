# app/goods/goods_ctl.py

from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import current_app as app
from flask import jsonify
from flask_jwt import JWT, jwt_required
from flask_ssl import *
from flask_login import current_user, login_required
from flask_jwt_extended import jwt_required

import json

from app.model.goods import Goods
from app.model.goods_response import GoodsResponse
from app.service.goods_service import GoodsService

goods_service = GoodsService()

goods_ctl=Blueprint('goods_ctl', __name__, url_prefix='/goods')


@goods_ctl.route('/add_goods', methods=['POST'])
@jwt_required()
def add_goods_with_id():
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
        goods_service.insert_goods(
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


def get_goods_with_id_internal(request):
    params = request.args.to_dict()

    if len(params) == 0 or Goods._col_name_ not in params.keys():
        return josnify({"result":"false", "reson":"no parameter"})
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
        cnt, goods_list = goods_service.get_goods(name = None,
                                                goods_id = -1,
                                                sel_limit = sel_limit)
    else:
        cnt, goods_list = goods_service.get_goods(name = name,
                                                goods_id = goods_id,
                                                sel_limit = sel_limit)
    print(f'result={cnt}, \n       {goods_list}')

    goods_json_list = []

    for goods in goods_list:
        print(goods.toJson())
        goods_json_list.append(goods.toJson())

    return jsonify({"len":cnt, "goods":goods_json_list})


def del_goods_with_id_internal(request):

    params = request.args.to_dict()

    if len(params) == 0 or Goods._col_name_ not in params.keys():
        return josnify({"result":"false", "reson":"no parameter"})

    name = params[Goods._col_name_]

    if Goods._col_mall_name_ in params.keys():
        mall_name = params[Goods._col_mall_name_]
    else:
        mall_name = None

    if Goods._col_goods_id_ in params.keys():
        goods_id = int(params[Goods._col_goods_id_])
    else:
        goods_id = -1

    if name == '*':
        goods_service.delete_goods(name = None,
                                 goods_id = -1,
                                 mall_name = None)
    else:
        goods_service.delete_goods(name = name,
                                 goods_id = goods_id,
                                 mall_name = mall_name)

    return jsonify({"result":"ok"})


@goods_ctl.route('/get_goods_with_id', methods=['POST'])
@jwt_required()
def get_goods_with_id():
    return get_goods_with_id_internal(request)


@goods_ctl.route('/get_goods_with_id_with_login', methods=['POST'])
@login_required
def get_goods_with_id_with_login():
    return get_goods_with_id_internal(request)


@goods_ctl.route('/del_goods_with_id', methods=['POST'])
@jwt_required()
def del_goods_with_id():
    return del_goods_with_id_internal(request)


@goods_ctl.route('/del_goods_with_id_with_login', methods=['POST'])
@login_required
def del_goods_with_id_with_login():
    return del_goods_with_id_internal(request)
