#!/usr/bin/env python3 
# -*- coding: utf-8 -*- 
# @Time : 2020/5/11 14:33 
# @Author : zqy 
"""装机列表"""
from flask import Blueprint

index_bp = Blueprint("installList", __name__, url_prefix="/installList")

from .views import *



