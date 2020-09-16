#!/usr/bin/env python3 
# -*- coding: utf-8 -*- 
# @Time : 2020/4/27 11:05 
# @Author : zqy 
from flask import Blueprint

index_bp = Blueprint("user", __name__, url_prefix="/user")

from .views import *
