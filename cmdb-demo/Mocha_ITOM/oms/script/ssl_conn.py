#!/usr/bin/env python3 
# -*- coding: utf-8 -*- 
# @Time : 2020/4/23 11:50 
# @Author : zqy
import paramiko
import time

from typing import Union


def conn(ip: str, username: str, password: str, terminal_command: Union[list, str]):
    """
    ssl连接远端服务器
    :param ip: 远端服务器IP
    :type ip: str
    :param username:
    :type username:
    :param password:
    :type password:
    :param terminal_command: 终端命令集合
    :type terminal_command: list str
    :return:
    :rtype:
    """

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh_client.connect(hostname=ip, username=username, password=password)
    except paramiko.ssh_exception.AuthenticationException as e:
        raise KeyError("身份验证失败！！")

    command = ssh_client.invoke_shell()

    if isinstance(terminal_command, list):
        for cmd in terminal_command:
            command.send(f"{cmd}\n")
    else:
        command.send(f"{terminal_command}\n")

    time.sleep(1)
    output = command.recv(65535)
    with open("tmp.txt", "wb") as f:
        f.write(output)

    ssh_client.close()

    return output.decode()


if __name__ == '__main__':
    ip = "106.12.54.221"
    username = "root"
    password = "zqy@123456"
    cmd = ["tree -FCN softs/tr-master"]
    conn(ip, username, password, cmd)
