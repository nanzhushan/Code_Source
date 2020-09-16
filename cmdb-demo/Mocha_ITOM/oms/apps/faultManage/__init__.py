#!/usr/bin/env python3 
# -*- coding: utf-8 -*- 
# @Time : 2020/4/25 14:36 
# @Author : zqy 
"""故障"""
from flask import Blueprint

index_bp = Blueprint("faultManage", __name__, url_prefix="/faultManage")

from .views import *
