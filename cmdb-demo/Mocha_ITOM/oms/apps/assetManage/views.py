#!/usr/bin/env python3 
# -*- coding: utf-8 -*- 
# @Time : 2020/4/30 17:29 
# @Author : zqy 
from flask import request, jsonify, current_app, render_template, g
from sqlalchemy import and_, not_

from oms.models import HostList, NetworkAsset, IdcAsset
from oms.response_code import RET
from oms.utils.common import commit, get_user_info
from . import index_bp


# todo ------------------ Host 主机 ----------------------
# /assetManage/host
@index_bp.route("/host", methods=["GET", "POST"])
@get_user_info
def host_info():
    """展示host详情"""

    if request.method == "GET":
        return render_template("hostList.html", username=g.user.username)

    param_dict = request.json
    ip = param_dict.get("ip")
    if ip:
        host = HostList.query.filter(HostList.ip == ip).first()
        return jsonify(errno=RET.OK, errmsg=u'OK', data=[host.to_basic_dict()], count=1)

    page = int(param_dict.get("page", 1))  # 当前页码（默认值：1）
    limit = int(param_dict.get("limit", 10))  # 每一页多少条新闻（默认值：10）
    try:
        paginate = HostList.query.filter(not_(HostList.status == -1)) \
            .order_by(HostList.id.desc()).paginate(page, limit, False)
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


# /assetManage/host/add
@index_bp.route("/host/add", methods=["POST"])
@get_user_info
def add_host():
    """新增主机"""
    param_dict = request.json
    ip = param_dict.get("ip")
    ip1 = param_dict.get("ip1")
    product = param_dict.get("product")
    application = param_dict.get("application")
    idc_jg = param_dict.get("idc_jg")
    status = param_dict.get("status")
    remark = param_dict.get("remark")

    if not ip:
        return jsonify(errno=RET.PARAMERR, errmsg=u'请输入IP值！')

    host = HostList.query.filter_by(ip=ip).first()
    if host:
        return jsonify(errno=RET.PARAMERR, errmsg="ip值已经存在！")

    host_param = {
        "ip": ip,
        "ip1": ip1,
        "product": product,
        "application": application,
        "idc_jg": idc_jg,
        "status": status,
        "remark": remark,
    }

    host_info = HostList(**host_param)

    commit(host_info)

    return jsonify(errno=RET.OK, errmsg="OK")


# /assetManage/host/1
@index_bp.route("/host/<string:host_id>", methods=["GET"])
@get_user_info
def host_detail(host_id):
    """展示host详情"""
    host = HostList.query.filter(and_(HostList.status != -1, HostList.id == host_id)).first()
    if host is None:
        return jsonify(errno=RET.PARAMERR, errmsg=u'操作错误！！')
    return jsonify(errno=RET.OK, errmsg='OK', data=host.to_basic_dict())
    # return render_template("editHost.html", data=host.to_basic_dict())


# /assetManage/host/1
@index_bp.route("/host/<string:host_id>", methods=["PUT"])
@get_user_info
def host_change(host_id):
    """修改host"""

    host = HostList.query.get(host_id)
    if host is None:
        return jsonify(errno=RET.PARAMERR, errmsg=u'操作错误！！')

    param_dict = request.json
    ip = param_dict.get("ip")
    ip1 = param_dict.get("ip1")
    product = param_dict.get("product")
    application = param_dict.get("application")
    idc_jg = param_dict.get("idc_jg")
    status = param_dict.get("status")
    remark = param_dict.get("remark")

    host.ip = ip
    host.ip1 = ip1
    host.product = product
    host.application = application
    host.idc_jg = idc_jg
    host.status = status
    host.remark = remark

    commit(host)

    return jsonify(errno=RET.OK, errmsg="OK")


# /assetManage/host/1
@index_bp.route("/host/<string:host_id>", methods=["DELETE"])
@get_user_info
def host_delete(host_id):
    """逻辑删除host"""

    host = HostList.query.get(host_id)

    if host is None:
        return jsonify(errno=RET.PARAMERR, errmsg=u'操作错误！！')

    host.status = -1

    commit(host)

    return jsonify(errno=RET.OK, errmsg="OK")


# todo ------------ network  网络设备资产---------------------
# /assetManage/network
@index_bp.route("/network", methods=['GET', 'POST'])
@get_user_info
def network_info():
    if request.method == "GET":
        return render_template("networkList.html", username=g.user.username)

    param_dict = request.args
    page = int(param_dict.get("page", 1))  # 当前页码（默认值：1）
    limit = int(param_dict.get("limit", 10))  # 每一页多少条新闻（默认值：10）
    try:
        paginate = NetworkAsset.query.filter(not_(NetworkAsset.status == -1)) \
            .order_by(NetworkAsset.id.desc()).paginate(page, limit, False)
    except Exception as e:
        current_app.logger.error("查询 NetworkAsset 信息错误，错误信息：{}".format(e))
        return jsonify(errno=RET.DBERR, errmsg="操作失败！")

    network_info_list = paginate.items  # 当前页码所有数据
    current_page = paginate.page  # 当前页码
    total_page = paginate.pages  # 总页数
    data_list = []

    for network_info in network_info_list if network_info_list else []:
        data_list.append(network_info.to_basic_dict())

    return jsonify(errno=RET.OK, errmsg="OK", count=total_page * 10, data=data_list)


# /assetManage/network/add
@index_bp.route("/network/add", methods=["POST"])
@get_user_info
def add_network():
    """添加设备"""

    param_dict = request.json
    ip = param_dict.get("ip")
    hostname = param_dict.get("hostname")
    manufacturer = param_dict.get("manufacturer")
    productname = param_dict.get("productname")
    service_tag = param_dict.get("service_tag")
    idc_jg = param_dict.get("idc_jg")
    status = param_dict.get("status")
    remark = param_dict.get("remark")

    if not ip:
        return jsonify(errno=RET.PARAMERR, errmsg=u'请输入IP值！')

    network = NetworkAsset.query.filter_by(ip=ip).first()
    if network:
        return jsonify(errno=RET.PARAMERR, errmsg="ip值已经存在！")

    network_param = {
        "ip": ip,
        "hostname": hostname,
        "manufacturer": manufacturer,
        "productname": productname,
        "service_tag": service_tag,
        "idc_jg": idc_jg,
        "status": status,
        "remark": remark,
    }

    network_info = NetworkAsset(**network_param)

    commit(network_info)

    return jsonify(errno=RET.OK, errmsg="OK")


# /assetManage/network/1
@index_bp.route("/network/<string:net_id>", methods=['PUT'])
@get_user_info
def change_network(net_id):
    """修改网络设备信息"""

    net = NetworkAsset.query.get(net_id)
    if net is None:
        return jsonify(errno=RET.PARAMERR, errmsg=u'错误的id！！')

    param_dict = request.json
    ip = param_dict.get("ip")
    hostname = param_dict.get("hostname")
    manufacturer = param_dict.get("manufacturer")
    productname = param_dict.get("productname")
    service_tag = param_dict.get("service_tag")
    idc_jg = param_dict.get("idc_jg")
    status = param_dict.get("status")
    remark = param_dict.get("remark")

    net.ip = ip
    net.hostname = hostname
    net.productname = productname
    net.manufacturer = manufacturer
    net.idc_jg = idc_jg
    net.service_tag = service_tag
    net.status = status
    net.remark = remark

    commit(net)

    return jsonify(errno=RET.OK, errmsg="OK")


# /assetManage/network/1
@index_bp.route("/network/<string:net_id>", methods=["DELETE"])
@get_user_info
def delete_network(net_id):
    """逻辑删除网络设备"""

    net = NetworkAsset.query.get(net_id)

    if net is None:
        return jsonify(errno=RET.PARAMERR, errmsg=u'操作错误！！')

    net.status = -1

    commit(net)

    return jsonify(errno=RET.OK, errmsg="OK")


# todo ------------ IDC  数据中心资产---------------------
# /assetManage/idc
@index_bp.route("/idc", methods=['GET', 'POST'])
@get_user_info
def idc_info():
    if request.method == "GET":
        return render_template("idcList.html", username=g.user.username)

    """数据中心资产展示"""
    param_dict = request.json
    page = int(param_dict.get("page", 1))  # 当前页码（默认值：1）
    limit = int(param_dict.get("limit", 10))  # 每一页多少条新闻（默认值：10）
    try:
        paginate = IdcAsset.query.filter(IdcAsset.status != -1) \
            .order_by(IdcAsset.id.desc()).paginate(page, limit, False)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="操作失败！")

    date_info_list = paginate.items  # 当前页码所有数据
    current_page = paginate.page  # 当前页码
    total_page = paginate.pages  # 总页数
    data_list = []

    for date_info in date_info_list if date_info_list else []:
        data_list.append(date_info.to_basic_dict())

    return jsonify(errno=RET.OK, errmsg="OK", count=total_page * 10, data=data_list)


# /assetManage/idc/add
@index_bp.route("/idc/add", methods=["POST"])
@get_user_info
def add_idc():
    param_dict = request.json
    idc_name = param_dict.get("idc_name")
    idc_type = param_dict.get("idc_type")
    idc_location = param_dict.get("idc_location")
    contract_date = param_dict.get("contract_date")
    idc_contacts = param_dict.get("idc_contacts")
    status = param_dict.get("status")
    remark = param_dict.get("remark")

    idc_param = {
        "idc_name": idc_name,
        "idc_type": idc_type,
        "idc_location": idc_location,
        "contract_date": contract_date,
        "idc_contacts": idc_contacts,
        "status": status,
        "remark": remark,
    }

    idc_info = IdcAsset(**idc_param)

    commit(idc_info)

    return jsonify(errno=RET.OK, errmsg="OK")


# /assetManage/idc/1
@index_bp.route("/idc/<string:idc_id>", methods=["PUT"])
@get_user_info
def change_idc(idc_id):
    """修改"""

    param_dict = request.json
    idc_name = param_dict.get("idc_name")
    idc_type = param_dict.get("idc_type")
    idc_location = param_dict.get("idc_location")
    contract_date = param_dict.get("contract_date")
    idc_contacts = param_dict.get("idc_contacts")
    status = param_dict.get("status")
    remark = param_dict.get("remark")

    idc = IdcAsset.query.get(idc_id)
    if idc is None:
        return jsonify(errno=RET.PARAMERR, errmsg=u'操作错误！！')

    idc.idc_name = idc_name
    idc.idc_type = idc_type
    idc.idc_location = idc_location
    idc.contract_date = contract_date
    idc.idc_contacts = idc_contacts
    idc.status = status
    idc.remark = remark

    commit(idc)

    return jsonify(errno=RET.OK, errmsg="OK")


# # /assetManage/idc/1
@index_bp.route("/idc/<string:idc_id>", methods=["DELETE"])
@get_user_info
def delete_idc(idc_id):
    """逻辑删除host"""

    host = IdcAsset.query.get(idc_id)

    if host is None:
        return jsonify(errno=RET.PARAMERR, errmsg=u'操作错误！！')

    host.status = -1

    commit(host)

    return jsonify(errno=RET.OK, errmsg="OK")


