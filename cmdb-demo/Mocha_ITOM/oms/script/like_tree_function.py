#!/usr/bin/env python3 
# -*- coding: utf-8 -*- 
# @Time : 2020/5/11 18:03 
# @Author : zqy 
"""类似linux tree的功能"""
import json, os


def list_dir(path, res):
    for i in os.listdir(path):
        temp_dir = os.path.join(path, i)
        if os.path.isdir(temp_dir):
            temp = {"dirname": i, 'child_dirs': [], 'files': []}
            res['child_dirs'].append(list_dir(temp_dir, temp))
        else:
            res['files'].append(i)
    return res


def get_config_dirs(path=None):
    if path is None:
        path = os.getcwd()
    res = {'dirname': path, 'child_dirs': [], 'files': []}
    return list_dir(path, res)


if __name__ == '__main__':
    print(json.dumps(get_config_dirs(path=r'/Users/zqy/PythonProject/Local/demo/11-18')))
