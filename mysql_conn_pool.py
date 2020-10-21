# coding: utf-8

"""
Created on:
@brief:
@author: YangLei
@version: Python3
"""

from configparser import ConfigParser
from mysql_pool import MySqlPool
import requests

# 读取配置文件
cfg = ConfigParser()
cfg.read('../config.ini',encoding='utf-8')

#配置连接
adb_ba = MySqlPool(db='ba', host=cfg.get('mysql-ads', 'host'), port=int(cfg.get('mysql-ads', 'port')), user=cfg.get('mysql-ads', 'user'), passwd=cfg.get('mysql-ads', 'password'))
