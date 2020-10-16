# coding: utf-8

"""
Created on:
@brief:
@author: YangLei
@version: Python3
"""
import cpca

ad=['芒市']

normal=cpca.transform(ad,pos_sensitive=True)
print(normal)




