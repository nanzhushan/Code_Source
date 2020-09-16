#!/usr/bin/env python3 
# -*- coding: utf-8 -*- 
# @Time : 2020/4/28 11:08 
# @Author : zqy 
"""
资产管理
"""
from flask import Blueprint

index_bp = Blueprint("assetManage", __name__, url_prefix="/assetManage")

from .views import *