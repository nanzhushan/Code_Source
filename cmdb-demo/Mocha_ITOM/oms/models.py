#!/usr/bin/env python3 
# -*- coding: utf-8 -*- 
# @Time : 2020/4/23 16:32 
# @Author : zqy 
"""数据库模型"""
from datetime import datetime

# from sqlalchemy_utils.types.choice import ChoiceType  # 相当于django中的choices
from werkzeug.security import check_password_hash, generate_password_hash

from oms import db


class BaseModel(object):
    """模型基类，为每个模型补充创建时间与更新时间"""
    create_time = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 记录的更新时间


class HostList(BaseModel, db.Model):
    """主机"""
    __tablename__ = "HostList"

    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(21), unique=True)  # 内网IP地址
    ip1 = db.Column(db.String(21), nullable=True)  # 外网IP地址 允许为空
    product = db.Column(db.String(40))  # 主机配置
    application = db.Column(db.String(20))  # 应用
    idc_jg = db.Column(db.String(10), nullable=True)  # 主机可用区
    status = db.Column(db.String(10), default="online")  # 使用状态
    remark = db.Column(db.Text(50), nullable=True, default="阿里云")  # 备注

    def to_basic_dict(self):
        return {
            "id": self.id,
            "ip": self.ip,
            "ip1": self.ip1,
            "product": self.product,
            "application": self.application,
            "idc_jg": self.idc_jg,
            "status": self.status,
            "remark": self.remark,
            "create_time": str(self.create_time).split(".")[0],
        }

    def __repr__(self):
        return u'%s - %s - %s' % (self.ip, self.ip1, self.application)


class NetworkAsset(BaseModel, db.Model):
    """网络设备资产信息"""
    __tablename__ = "NetworkAsset"

    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(21))  # 内网IP地址
    hostname = db.Column(db.String(30))  # 主机名
    manufacturer = db.Column(db.String(20))  # 厂商
    productname = db.Column(db.String(20))  # 产品型号
    idc_jg = db.Column(db.String(10), unique=True)  # 机柜编号
    service_tag = db.Column(db.String(30), unique=True)  # 序列号
    status = db.Column(db.String(10), default=0)  # 使用状态
    remark = db.Column(db.Text(50), nullable=True, default="")  # 备注

    def __repr__(self):
        return self.ip

    def to_basic_dict(self):
        return {
            "id": self.id,
            "ip": self.ip,
            "hostname": self.hostname,
            "manufacturer": self.manufacturer,
            "productname": self.productname,
            "idc_jg": self.idc_jg,
            "service_tag": self.service_tag,
            "status": self.status,
            "remark": self.remark,
        }


class IdcAsset(BaseModel, db.Model):
    """IDC资产信息"""
    __tablename__ = "IdcAsset"

    id = db.Column(db.Integer, primary_key=True)
    idc_name = db.Column(db.String(21))  # 机房名称
    idc_type = db.Column(db.String(21))  # 机房类型
    idc_location = db.Column(db.String(30))  # 机房位置
    contract_date = db.Column(db.String(30))  # 合同时间
    idc_contacts = db.Column(db.String(11))  # 联系电话
    status = db.Column(db.String(10), default=0)  # 使用状态
    remark = db.Column(db.Text, nullable=True, default="")  # 备注

    def __repr__(self):
        return self.idc_name

    def to_basic_dict(self):
        return {
            "id": self.id,
            "idc_name": self.idc_name,
            "idc_type": self.idc_type,
            "idc_location": self.idc_location,
            "contract_date": self.contract_date,
            "idc_contacts": self.idc_contacts,
            "status": self.status,
            "remark": self.remark,
        }


class TypeInfo(BaseModel, db.Model):
    __tablename__ = "Type"

    id = db.Column(db.Integer, primary_key=True)
    faulttype = db.Column(db.String(255))  # 故障类型
    status = db.Column(db.String(10), default=0)

    def __repr__(self):
        return self.faulttype

    def __str__(self):
        return self.faulttype

    def values_list(self):
        return [(self.id, self.faulttype)]

    def to_basic_dict(self):
        return {
            "id": self.id,
            "faulttype": self.faulttype,
            "create_time": str(self.create_time).split(".")[0],
        }


fms_level = [u"非常严重", u"严重", u"中等", u"一般", u"无影响"]
fms_status = [u"处理中", u"已恢复", u"改进中", u"已完结"]
fms_improve = [u"开发", u"运维"u"机房", u"网络运营商", u"第三方"]


class FaultContent(BaseModel, db.Model):
    """故障分析"""
    __tablename__ = "FaultContent"

    # fms_level = (
    #     (0, u"非常严重"),
    #     (1, u"严重"),
    #     (2, u"中等"),
    #     (3, u"一般"),
    #     (4, u"无影响"),
    # )
    # fms_status = (
    #     (0, u"处理中"),
    #     (1, u"已恢复"),
    #     (2, u"改进中"),
    #     (3, u"已完结"),
    # )
    # fms_improve = (
    #     (0, u"开发"),
    #     (1, u"运维"),
    #     (2, u"机房"),
    #     (3, u"网络运营商"),
    #     (4, u"第三方"),
    #
    # )

    id = db.Column(db.Integer, primary_key=True)
    # fms_type = Type.objects.all().values_list('id', 'name')  # [(1, 'First entry'), ...]
    # fms_type = TypeInfo().values_list()  # [(1, 'First entry'), ...]
    title = db.Column(db.String(255))  # 故障简述
    typeinfo = db.Column(db.Integer, nullable=True)  # 故障类型 与TypeInfo的id关联，逻辑外键
    project = db.Column(db.Text)  # 影响项目
    effect = db.Column(db.Text, nullable=True)  # 故障影响
    reasons = db.Column(db.Text, nullable=True)  # 故障原因
    solution = db.Column(db.Text, nullable=True)  # 解决方案
    level = db.Column(db.Integer)  # 故障级别
    status = db.Column(db.String(10))  # 故障状态
    improve = db.Column(db.Integer)  # 主导改进
    # level = db.Column(ChoiceType(fms_level))  # 故障级别
    # status = db.Column(ChoiceType(fms_status))  # 故障状态
    # improve = db.Column(ChoiceType(fms_improve))  # 主导改进
    content = db.Column(db.Text, nullable=True)  # 故障分析
    faulttime = db.Column(db.DateTime, )  # 故障时间

    def to_basic_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "level": fms_level[int(self.level)],
            "typeinfo": self.typeinfo,
            "project": self.project,
            "effect": self.effect,
            "reasons": self.reasons,
            "solution": self.solution,
            "improve": fms_improve[int(self.improve)],
            "status": fms_status[int(self.status)],
            "content": self.content,
            "faulttime": self.faulttime,
            "create_time": str(self.create_time).split(".")[0],
        }

    def __repr__(self):
        return self.title

    def __str__(self):
        return self.title


class SystemInstall(BaseModel, db.Model):
    """
    装机列表
    System Install Manage
    """
    __tablename__ = "SystemInstall"

    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(21))  # 待装机IP
    hostname = db.Column(db.String(30))  # 主机名
    macaddress = db.Column(db.String(50), unique=True)  # MAC地址
    systemVersion = db.Column(db.String(20))  # 操作系统
    status = db.Column(db.String(20))  # 状态
    remark = db.Column(db.Text, nullable=True, default="")  # 备注

    def __repr__(self):
        return u'%s -- %s' % (self.ip, self.install_date)

    def to_basic_dict(self):
        return {
            "id": self.id,
            "ip": self.ip,
            "hostname": self.hostname,
            "macaddress": self.macaddress,
            "systemVersion": self.systemVersion,
            "status": self.status,
            "remark": self.remark,
            "create_time": str(self.create_time).split(".")[0],

        }


class InstallRecord(BaseModel, db.Model):
    """
    装机记录
    Server Install Recored
    """
    __tablename__ = "InstallRecord"

    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(21))  # 安装IP
    systemVersion = db.Column(db.String(20))  # 安装操作系统版本
    status = db.Column(db.String(20), default='online')  # 故障状态
    remark = db.Column(db.Text, nullable=True, default="")  # 备注

    def __repr__(self):
        return u'%s - %s' % (self.ip, self.system_version)

    def to_basic_dict(self):
        return {
            "id": self.id,
            "ip": self.ip,
            "systemVersion": self.systemVersion,
            "status": self.status,
            "remark": self.remark,
            "create_time": str(self.create_time).split(".")[0],

        }


class InterfaceList(BaseModel, db.Model):
    """接口信息列表"""
    __tablename__ = "InterfaceList"

    id = db.Column(db.Integer, primary_key=True)
    module = db.Column(db.String(20))  # 模块
    url = db.Column(db.String(100))  # 接口地址
    headers = db.Column(db.String(50), nullable=True, default="{'content-type': 'application/json'}")  # 头部
    body = db.Column(db.String(50), unique=True)  # 请求参数
    method = db.Column(db.String(10), default="http post", unique=True)  # 请求方式
    update_interval = db.Column(db.String(50), default="手工", unique=True)  # 请求频率
    status = db.Column(db.String(10))  # 状态
    response = db.Column(db.String(200))  # 返回结果
    remark = db.Column(db.String(50))  # 备注

    def __repr__(self):
        return u'%s - %s - %s' % (self.ip, self.status, self.response)

    def to_basic_dict(self):
        return {
            "id": self.id,
            "module": self.module,
            "url": self.url,
            "headers": self.headers,
            "body": self.body,
            "method": self.method,
            "update_interval": self.update_interval,
            "status": self.status,
            "response": self.response,
            "remark": self.remark,
            "create_time": str(self.create_time).split(".")[0],
        }


class Users(BaseModel, db.Model):
    """
    OMS User Manage
    """
    __tablename__ = "Users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))  # 用户名
    password_hash = db.Column(db.String(128), nullable=False)  # 加密的密码
    last_login = db.Column(db.DateTime, default=datetime.now)  # 最后一次登录时间

    def check_password(self, password):
        # 将未加密的密码按照相同的加密算法，再次加密，然后比较，返回一个BOOL值
        return check_password_hash(self.password_hash, password)

    def set_password_hash(self, password):
        # 1.将未加密的密码进行加密处理
        password_hash = generate_password_hash(password)
        # 2.将加密后的密码给password_hash赋值
        self.password_hash = password_hash

    @property
    def password(self):
        raise AttributeError("不允许获取密码")

    # 属性的setter方法，给其赋值的时候会触发set方法
    @password.setter
    def password(self, value):
        # 1.将未加密的密码进行加密处理
        password_hash = generate_password_hash(value)
        # 2.将加密后的密码给password_hash赋值
        self.password_hash = password_hash

    def __repr__(self):
        return self.username


class Message(BaseModel, db.Model):
    """
    平台审计信息
    """
    __tablename__ = "Message"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(10))  # 类型
    action = db.Column(db.String(10))  # 动作
    action_ip = db.Column(db.String(15))  # 执行IP
    content = db.Column(db.String(50))  # 内容

    def to_basic_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "action": self.action,
            "action_ip": self.action_ip,
            "content": self.content,
        }

    def __repr__(self):
        return self.username


if __name__ == '__main__':
    """"""
    # from appDev import app
    #
    # with app.app_context():
    #     # db.create_all()
