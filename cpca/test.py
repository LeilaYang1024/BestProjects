# coding: utf-8

"""
Created on:
@brief:
@author: YangLei
@version: Python3
"""
import cpca

ad=['北京市海淀区信息路甲28号C座(二层)02B室-405']

normal=cpca.transform(ad,pos_sensitive=True)
print(normal)




