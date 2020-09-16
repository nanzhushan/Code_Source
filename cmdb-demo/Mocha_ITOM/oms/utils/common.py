#!/usr/bin/env python3 
# -*- coding: utf-8 -*- 
# @Time : 2020/4/27 11:02 
# @Author : zqy
import functools

from flask import session, current_app, jsonify, g, render_template

from oms import db
from oms.response_code import RET


def get_user_info(view_func):
    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):

        # 1.获取用户id
        user_id = session.get("user_id", None)

        if user_id is None:
            return render_template("login.html")

        from oms.models import Users
        user = None  # type: Users
        if user_id:
            try:
                user = Users.query.get(user_id)
            except Exception as e:
                current_app.error(e)
                return jsonify(errno=RET.DBERR, errmsg="操作失败！")

        # 使用全局的临时g对象存储user对象
        # 只要请求还未结束，就能获取到g对象中的内容
        g.user = user

        # 2.原有视图函数功能再次调用执行
        result = view_func(*args, **kwargs)
        return result

    return wrapper


def commit(obj):
    try:
        db.session.add(obj)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="操作失败")
