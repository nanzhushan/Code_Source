#!/usr/bin/env python3 
# -*- coding: utf-8 -*- 
# @Time : 2020/4/27 11:06 
# @Author : zqy 
from datetime import datetime

from flask import request, current_app, jsonify, session, g, render_template

from oms.models import Users
from oms.response_code import RET
from oms.utils.common import commit, get_user_info
from . import index_bp


# /user/login
@index_bp.route("/login", methods=['POST', 'GET'])
def login():
    """登录后端接口"""

    if request.method == "GET":
        return render_template("login.html")

    param_dict = request.json
    name = param_dict.get("name")
    password = param_dict.get("password")

    if not all([name, password]):
        current_app.logger.error("参数不足")
        return jsonify(errno=RET.PARAMERR, errmsg="参数不足")

    try:
        user = Users.query.filter(Users.username == name).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="操作失败！")

    if not user:
        return jsonify(errno=RET.USERERR, errmsg="用户不存在")

    # 存在：根据用户对象，校验密码是否正确
    if user.check_password(password) is False:
        return jsonify(errno=RET.DATAERR, errmsg="密码错误")

    # 3.2 更新最后一次登录时间 [将修改操作保存回数据]
    # 注意配置数据库字段：SQLALCHEMY_COMMIT_ON_TEARDOWN = True 自动提交数据db.session.commit()
    user.last_login = datetime.now()

    commit(user)

    session["user_id"] = user.id
    session["name"] = user.username

    return jsonify(errno=RET.OK, errmsg="登录成功")


# /user/logout
@index_bp.route("/logout", methods=['GET'])
@get_user_info
def logout():
    # 1.将session中键值对数据删除
    session.pop("user_id", "")
    session.pop("name", "")

    # 退出登录记得清楚管理员权限
    session.pop("is_admin", "")

    return render_template("login.html")


# /user/registered_lala
@index_bp.route("/registered_lala", methods=['POST'])
def registered():
    param_dict = request.json
    name = param_dict.get("name")
    password = param_dict.get("password")

    # 2.1 非空判断
    if not all([name, password]):
        current_app.logger.error("参数不足")
        return jsonify(errno=RET.PARAMERR, errmsg="参数不足")

    try:
        user = Users.query.filter(Users.username == name).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="操作失败！")
    else:
        if user:
            return jsonify(errno=RET.USERERR, errmsg="用户已经存在！")

    user = Users()
    user.username = name
    # TODO: 密码加密
    user.set_password_hash(password)

    user.last_login = datetime.now()

    commit(user)

    session["user_id"] = user.id
    session["name"] = user.username
    return jsonify(errno=RET.OK, errmsg="注册成功")


# /user/changePassword
@index_bp.route("/changePassword", methods=['POST'])
@get_user_info
def change_password():
    """修改密码后端接口"""

    # 当前登录的用户对象, old_password:旧密码， new_password:新密码
    user = g.user  # type:Users
    if not user:
        return jsonify(errno=RET.SESSIONERR, errmsg="用户未登录")

    old_password = request.json.get("old_password")
    new_password = request.json.get("new_password")

    if not all([old_password, new_password]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不足")

    if not user.check_password(old_password):
        return jsonify(errno=RET.DATAERR, errmsg="旧密码填写错误")

    user.set_password_hash(new_password)

    commit(user)

    return jsonify(errno=RET.OK, errmsg="修改密码成功")
