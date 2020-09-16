#!/usr/bin/env python3 
# -*- coding: utf-8 -*- 
# @Time : 2020/5/11 11:30 
# @Author : zqy 
from flask import jsonify, current_app, request, render_template, g

from oms.models import InterfaceList
from oms.response_code import RET
from oms.utils.common import get_user_info
from . import index_bp


# /monitorManage/hardware
@index_bp.route("/hardware", methods=['GET', 'POST'])
@get_user_info
def monitor_info():
    if request.method == "GET":
        return render_template("hardwareMonitor.html", username=g.user.username)

    param_dict = request.json
    # module = param_dict.get("module")
    # url = param_dict.get("url")
    # headers = param_dict.get("headers")
    # body = param_dict.get("body")
    # method = param_dict.get("method")
    # update_interval = param_dict.get("update_interval")
    # status = param_dict.get("status")
    # create_time = param_dict.get("create_time")
    # remark = param_dict.get("remark")

    page = int(param_dict.get("page", 1))  # 当前页码（默认值：1）
    limit = int(param_dict.get("limit", 10))  # 每一页多少条新闻（默认值：10）
    try:
        paginate = InterfaceList.query.filter().order_by(InterfaceList.id.desc()).paginate(page, limit, False)
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
