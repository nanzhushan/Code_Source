#!/usr/bin/env python3 
# -*- coding: utf-8 -*- 
# @Time : 2019/8/21 15:28 
# @Author : zqy
# TODO gunicorn -c gunicorn_config.py manage:app
import multiprocessing
import os
import sys

path_of_current_file = os.path.abspath(__file__)
path_of_current_dir = os.path.split(path_of_current_file)[0]

_file_name = os.path.basename(__file__)

sys.path.insert(0, path_of_current_dir)

worker_class = 'sync'
# workers = multiprocessing.cpu_count() * 2 + 1
workers = 2

chdir = path_of_current_dir

worker_connections = 1000
timeout = 3600
max_requests = 2000
graceful_timeout = 30

loglevel = 'info'

reload = True
debug = False
daemon = True  #后台运作需要设置为True

bind = "%s:%s" % ("0.0.0.0", 8080)
pidfile = '%s/gunicorn.pid' % path_of_current_dir
errorlog = '%s/logs/%s_error.log' % (path_of_current_dir, _file_name)
accesslog = '%s/logs/%s_access.log' % (path_of_current_dir, _file_name)
