#!/usr/bin/env python3 
# -*- coding: utf-8 -*- 
# @Time : 2020/5/8 15:51 
# @Author : zqy 
from flask import request, render_template, jsonify

from oms.response_code import RET
from oms.utils.common import get_user_info
from . import index_bp

from oms.script.ssl_conn import conn


# todo --------------- 智能硬件模块发布 ---------------
# /deployManage/smart
@index_bp.route("/smart", methods=["GET", "POST"])
@get_user_info
def smart_info():
    """命令执行"""

    if request.method == "GET":
        return render_template("smartHardware.html")

    params_dict = request.json
    target_host = params_dict.get("target_host")
    version = params_dict.get("version")

    # todo, 然后这边我要怎么做。。。找运维了解对接


# todo --------------- 远程管理 命令执行 ---------------
# /deployManage/command
@index_bp.route("/command", methods=["GET", 'POST'])
@get_user_info
def command_perform():
    """命令执行"""
    if request.method == "GET":
        return render_template("commandPerform.html")

    params_dict = request.json

    host = params_dict.get("host")
    code = params_dict.get("code")

    ip = "106.12.54.221"
    username = "root"
    password = "zqy@123456"
    cmd = ["pwd", "ifconfig"]
    res = conn(ip, username, password, cmd)

    return {"errno": RET.OK, "errmsg": u'OK', "result": res}


# todo --------------- 代码发布 ---------------
# /deployManage/code
@index_bp.route("/code", methods=["GET", 'POST'])
@get_user_info
def code_release():
    """代码发布"""
    if request.method == "GET":
        return render_template("codeRelease.html")

    params_dict = request.json

    host = params_dict.get("host")
    code = params_dict.get("code")

    ip = "106.12.54.221"
    username = "root"
    password = "zqy@123456"
    cmd = ["pwd", "ifconfig"]
    res = conn(ip, username, password, cmd)

    return {"errno": RET.OK, "errmsg": u'OK', "result": res}
