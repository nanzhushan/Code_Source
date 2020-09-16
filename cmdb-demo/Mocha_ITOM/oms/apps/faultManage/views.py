#!/usr/bin/env python3 
# -*- coding: utf-8 -*- 
# @Time : 2020/4/25 14:37 
# @Author : zqy
from flask import jsonify, current_app, request, render_template, g

from oms import db
from oms.models import FaultContent, TypeInfo
from oms.response_code import RET
from oms.utils.common import get_user_info, commit
from . import index_bp


# todo ---------- 故障列表 ---------------------
# /faultManage/fault
@index_bp.route("/fault", methods=["GET", 'POST'])
@get_user_info
def fault_info():
    if request.method == "GET":
        return render_template("faultList.html", username=g.user.username)

    param_dict = request.json
    page = param_dict.get("page", 1)  # 当前页码（默认值：1）
    per_page = param_dict.get("per_page", 10)  # 每一页多少条新闻（默认值：10）
    try:
        paginate = FaultContent.query.filter().order_by(FaultContent.id.desc()).paginate(page, per_page, False)
    except Exception as e:
        current_app.logger.error("查询 FaultContent 信息错误，错误信息：{}".format(e))
        return jsonify(errno=RET.DBERR, errmsg="操作失败！")

    fault_info_list = paginate.items  # 当前页码所有数据
    current_page = paginate.page  # 当前页码
    total_page = paginate.pages  # 总页数
    data_list = []

    for fault_info in fault_info_list if fault_info_list else []:
        type_info = TypeInfo.query.get(fault_info.typeinfo)
        data = fault_info.to_basic_dict()
        data["typeinfo"] = type_info.faulttype
        data_list.append(data)

    return jsonify(errno=RET.OK, errmsg="OK", count=total_page * 10, data=data_list)


# /faultManage/fault/1
@index_bp.route("/fault/<string:fault_id>", methods=["GET"])
@get_user_info
def fault_detail(fault_id):
    """获取单个详情"""

    fault_info = FaultContent.query.get(fault_id)
    if fault_info is None:
        return jsonify(errno=RET.PARAMERR, errmsg=u'操作失败！')
    return jsonify(errno=RET.OK, errmsg=u'OK', data=fault_info.to_basic_dict())


# /assetManage/fault/add
@index_bp.route("/fault/add", methods=["POST"])
@get_user_info
def add_fault():
    """新增故障"""
    param_dict = request.json
    title = param_dict.get("title")
    level = param_dict.get("level")
    typeinfo = param_dict.get("typeinfo")
    project = param_dict.get("project")
    status = param_dict.get("status")
    faulttime = param_dict.get("faulttime")
    improve = param_dict.get("improve")
    effect = param_dict.get("effect")
    content = param_dict.get("content")
    solution = param_dict.get("solution")

    fault_param = {
        "title": title,
        "level": level,
        "typeinfo": typeinfo,
        "project": project,
        "faulttime": faulttime,
        "status": status,
        "improve": improve,
        "effect": effect,
        "content": content,
        "solution": solution,
    }

    fault_info = FaultContent(**fault_param)

    commit(fault_info)

    return jsonify(errno=RET.OK, errmsg="OK")


# todo ---------- 故障类型 ---------------------
# /faultManage/type/
@index_bp.route("/type", methods=["GET", 'POST'])
@get_user_info
def type_info():
    """故障类型"""

    if request.method == "GET":
        return render_template("faultType.html", username=g.user.username)

    param_dict = request.json
    page = param_dict.get("page", 1)  # 当前页码（默认值：1）
    per_page = param_dict.get("per_page", 10)  # 每一页多少条新闻（默认值：10）
    try:
        paginate = TypeInfo.query.filter(TypeInfo.status != -1) \
            .order_by(TypeInfo.id.desc()).paginate(page, per_page, False)
    except Exception as e:
        current_app.logger.error("查询 FaultContent 信息错误，错误信息：{}".format(e))
        return jsonify(errno=RET.DBERR, errmsg="操作失败！")

    type_info_list = paginate.items  # 当前页码所有数据
    current_page = paginate.page  # 当前页码
    total_page = paginate.pages  # 总页数
    data_list = []

    for type_infor in type_info_list if type_info_list else []:
        data_list.append(type_infor.to_basic_dict())

    return jsonify(errno=RET.OK, errmsg="OK", count=total_page * 10, data=data_list)


# /faultManage/type/add
@index_bp.route("/type/add", methods=["POST"])
@get_user_info
def type_add():
    """添加类型"""

    param_dict = request.json

    faulttype = param_dict.get("faulttype")

    typeinfo = TypeInfo.query.filter(TypeInfo.faulttype == faulttype).first()
    if typeinfo:
        return jsonify(errno=RET.DATAERR, errmsg=u'记录已存在！')

    typeinfo = TypeInfo(faulttype=faulttype)

    commit(typeinfo)

    return jsonify(errno=RET.OK, errmsg="OK")


# /faultManage/type/add
@index_bp.route("/type/<string:type_id>", methods=["DELETE"])
@get_user_info
def type_delete(type_id):
    """逻辑删除host"""

    host = TypeInfo.query.get(type_id)

    if host is None:
        return jsonify(errno=RET.PARAMERR, errmsg=u'操作错误！！')

    host.status = -1

    commit(host)

    return jsonify(errno=RET.OK, errmsg="OK")
