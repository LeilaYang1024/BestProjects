# coding: utf-8

"""
Created on:
@brief:
@author: YangLei
@version: Python3
"""
import cpca

ad=['吉林省四平市铁西区平西乡致富村303国道北侧']

normal=cpca.transform(ad,pos_sensitive=True)
print(normal)




