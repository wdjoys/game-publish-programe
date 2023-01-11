# -*- coding: utf-8 -*-
# @Author: xiaocao
# @Date:   2023-01-11 16:08:00
# @Last Modified by:   xiaocao
# @Last Modified time: 2023-01-11 16:11:15

from playhouse.shortcuts import ReconnectMixin
from peewee import MySQLDatabase


# 同步数据库
# 同步数据库断线重连类
class ReconnectMySQLDatabase(ReconnectMixin, MySQLDatabase):
    pass


DATABASE = ReconnectMySQLDatabase('game-publish', **{'charset': 'utf8', 'sql_mode': 'PIPES_AS_CONCAT',
                                                     'use_unicode': True, 'host': 'localhost', 'user': 'root', 'password': 'benniu'})
