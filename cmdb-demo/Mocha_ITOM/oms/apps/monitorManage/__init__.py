#!/usr/bin/env python3 
# -*- coding: utf-8 -*- 
# @Time : 2020/5/11 11:30 
# @Author : zqy 
"""监控管理"""
from flask import Blueprint

index_bp = Blueprint("monitorManage", __name__, url_prefix="/monitorManage")

from .views import *



