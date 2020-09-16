#!/usr/bin/env python3 
# -*- coding: utf-8 -*- 
# @Time : 2020/5/11 14:34 
# @Author : zqy 
from flask import jsonify, current_app, request, render_template, g
from sqlalchemy import not_

from oms import db
from oms.models import InstallRecord, SystemInstall
from oms.response_code import RET
from oms.utils.common import get_user_info, commit
from . import index_bp


# todo ---------- 安装记录 --------------
# /installList/record
@index_bp.route("/record", methods=['POST', 'GET'])
@get_user_info
def record_info():
    if request.method == "GET":
        return render_template("recordList.html", username=g.user.username)

    param_dict = request.json
    page = int(param_dict.get("page", 1))  # 当前页码（默认值：1）
    limit = int(param_dict.get("limit", 10))  # 每一页多少条新闻（默认值：10）
    try:
        paginate = InstallRecord.query.filter(InstallRecord.status != -1).order_by(InstallRecord.id.desc()).paginate(
            page, limit, False)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="操作失败！")

    host_info_list = paginate.items  # 当前页码所有数据
    current_page = paginate.page  # 当前页码
    total_page = paginate.pages  # 总页数
    data_list = []

    for host_info in host_info_list if host_info_list else []:
        data_list.append(host_info.to_basic_dict())

    return jsonify(errno=RET.OK, errmsg="OK", count=total_page * 10, data=data_list)


# /installList/record/add
@index_bp.route("/record/add", methods=['POST'])
@get_user_info
def record_add():
    param_dict = request.json
    ip = param_dict.get("ip")
    systemVersion = param_dict.get("systemVersion")
    status = param_dict.get("status")
    remark = param_dict.get("remark")

    record_param = {
        "ip": ip,
        "systemVersion": systemVersion,
        "status": status,
        "remark": remark,
    }

    record_info = InstallRecord(**record_param)

    commit(record_info)

    return jsonify(errno=RET.OK, errmsg="OK")


# /assetManage/record/1
@index_bp.route("/record/<string:record_id>", methods=["PUT"])
@get_user_info
def record_change(record_id):
    record = InstallRecord.query.get(record_id)
    if record is None:
        return jsonify(errno=RET.PARAMERR, errmsg=u'操作错误！！')

    param_dict = request.json
    ip = param_dict.get("ip")
    systemVersion = param_dict.get("systemVersion")
    status = param_dict.get("status")
    remark = param_dict.get("remark")

    record.ip = ip
    record.systemVersion = systemVersion
    record.status = status
    record.remark = remark

    commit(record)

    return jsonify(errno=RET.OK, errmsg="OK")


# /assetManage/record/1
@index_bp.route("/record/<string:record_id>", methods=["DELETE"])
@get_user_info
def record_delete(record_id):
    """逻辑删除host"""

    record = InstallRecord.query.get(record_id)

    if record is None:
        return jsonify(errno=RET.PARAMERR, errmsg=u'操作错误！！')

    record.status = -1

    commit(record)

    return jsonify(errno=RET.OK, errmsg="OK")


# todo ---------- 系统安装 --------------
# /installList/system
@index_bp.route("/system", methods=['POST', 'GET'])
@get_user_info
def system_info():
    if request.method == "GET":
        return render_template("systemList.html", username=g.user.username)

    param_dict = request.json
    page = int(param_dict.get("page", 1))  # 当前页码（默认值：1）
    limit = int(param_dict.get("limit", 10))  # 每一页多少条新闻（默认值：10）
    try:
        paginate = SystemInstall.query.filter(SystemInstall.status != -1).order_by(SystemInstall.id.desc()).paginate(
            page, limit, False)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="操作失败！")

    host_info_list = paginate.items  # 当前页码所有数据
    current_page = paginate.page  # 当前页码
    total_page = paginate.pages  # 总页数
    data_list = []

    for host_info in host_info_list if host_info_list else []:
        data_list.append(host_info.to_basic_dict())

    return jsonify(errno=RET.OK, errmsg="OK", count=total_page * 10, data=data_list)


# /installList/system/add
@index_bp.route("/system/add", methods=['POST'])
@get_user_info
def system_add():
    param_dict = request.json
    ip = param_dict.get("ip")
    hostname = param_dict.get("hostname")
    macaddress = param_dict.get("macaddress")
    systemVersion = param_dict.get("systemVersion")
    status = param_dict.get("status")
    remark = param_dict.get("remark")

    system = SystemInstall.query.filter(SystemInstall.macaddress == macaddress).first()
    if system:
        return jsonify(errno=RET.PARAMERR, errmsg=u'操作错误！')

    system_param = {
        "ip": ip,
        "hostname": hostname,
        "macaddress": macaddress,
        "systemVersion": systemVersion,
        "status": status,
        "remark": remark,
    }

    system_info = SystemInstall(**system_param)

    commit(system_info)

    return jsonify(errno=RET.OK, errmsg="OK")


# /assetManage/system/1
@index_bp.route("/system/<string:system_id>", methods=["PUT"])
@get_user_info
def system_change(system_id):
    system = SystemInstall.query.get(system_id)
    if system is None:
        return jsonify(errno=RET.PARAMERR, errmsg=u'操作错误！！')

    param_dict = request.json
    ip = param_dict.get("ip")
    hostname = param_dict.get("hostname")
    macaddress = param_dict.get("macaddress")
    systemVersion = param_dict.get("systemVersion")
    status = param_dict.get("status")
    remark = param_dict.get("remark")

    system.ip = ip
    system.systemVersion = systemVersion
    system.hostname = hostname
    system.macaddress = macaddress
    system.status = status
    system.remark = remark

    commit(system)

    return jsonify(errno=RET.OK, errmsg="OK")


# /assetManage/system/1
@index_bp.route("/system/<string:system_id>", methods=["DELETE"])
@get_user_info
def system_delete(system_id):
    """逻辑删除host"""

    system = SystemInstall.query.get(system_id)

    if system is None:
        return jsonify(errno=RET.PARAMERR, errmsg=u'操作错误！！')

    system.status = -1

    commit(system)

    return jsonify(errno=RET.OK, errmsg="OK")
