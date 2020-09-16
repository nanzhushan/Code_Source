#!/usr/bin/env python3 
# -*- coding: utf-8 -*- 
# @Time : 2020/4/22 12:05 
# @Author : zqy
"""部署管理"""
from flask import Blueprint

index_bp = Blueprint("deployManage", __name__, url_prefix="/deployManage")

from .views import *
