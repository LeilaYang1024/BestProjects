# -*- coding: utf-8 -*-
# __init__.py

from .structures import AddrMap, Pca
from .structures import P,C,A,S

VERSION = (0, 4, 4)

__version__ = ".".join([str(x) for x in VERSION])


class CPCAException(Exception):
    pass

class InputTypeNotSuportException(CPCAException):
    input_type = \
        """
        输入应该为
        |省     |市    |区     |
        |江苏省 |扬州市 |邗江区 |
        格式的pandas.core.frame.DateFrame
        """
    pass


def _data_from_csv() -> (dict, AddrMap, AddrMap,AddrMap,AddrMap,AddrMap, dict):
    """
    从pcas.csv处理省市区县标准数据映射结构
    :return: map
    """
    # 省名 -> 省全名
    province_map = {}

    # 城市名及其简写(去掉‘市’,遇其他清洗情况增加map) -> 相关pca元组
    city_map = AddrMap()

    # 区县名及其简写(去掉‘市’,遇其他清洗情况增加map) -> 相关pca元组
    area_map = AddrMap()

    # 街道及其简写(去掉‘街道’,遇其他清洗情况增加map) -> 相关pca元组
    street_map = AddrMap()

    # (省名全称, 街道名全称) -> 相关pca元组
    province_area_map = AddrMap()

    # (省名全称, 街道名全称) -> 相关pca元组
    province_street_map = AddrMap()

    # (省名, 市名, 区名, 街道) -> (纬度,经度)
    latlng = {}

    # 数据约定:国家直辖市的sheng字段为直辖市名称, 省直辖县的city字段为空
    from pkg_resources import resource_stream
    with resource_stream('cpca.resources', 'pcas.csv') as pca_stream:
        from io import TextIOWrapper
        import csv
        text = TextIOWrapper(pca_stream, encoding='utf8')
        pca_csv = csv.DictReader(text)
        for record_dict in pca_csv:
            latlng[(record_dict['sheng'], record_dict['shi'], record_dict['qu'],record_dict['jie'])] = \
                (record_dict['lat'], record_dict['lng'])


            _fill_province_map(province_map, record_dict)
            _fill_city_map(city_map, record_dict)
            _fill_area_map(area_map, record_dict)
            _fill_street_map(street_map,record_dict)
            _fill_province_area_map(province_area_map, record_dict)
            _fill_province_street_map(province_street_map,record_dict)

    return province_map,city_map,area_map,street_map,province_area_map,province_street_map,latlng



def _fill_province_street_map(province_street_map: AddrMap, record_dict):
    pca_tuple = (record_dict['sheng'], record_dict['shi'], record_dict['qu'],record_dict['jie'])
    key = (record_dict['sheng'], record_dict['jie'])
    if key not in province_street_map.keys() and key[1]!='':
        province_street_map.append_relational_addr(key, pca_tuple, P)

def _fill_province_area_map(province_area_map: AddrMap, record_dict):
    pca_tuple = (record_dict['sheng'], record_dict['shi'], record_dict['qu'],record_dict['jie'])
    key = (record_dict['sheng'], record_dict['qu'])
    if key not in province_area_map.keys() and key[1]!='':
        province_area_map.append_relational_addr(key, pca_tuple, P)

def _fill_street_map(street_map: AddrMap, record_dict):
    street_name = record_dict['jie']
    pca_tuple = (record_dict['sheng'], record_dict['shi'], record_dict['qu'],record_dict['jie'])
    if street_name not in street_map.keys() and street_name!='':
        street_map.append_relational_addr(street_name, pca_tuple, S)
        # 处理镇/乡/路/街道简写情况
        if street_name.endswith('街道'):
            street_map.append_relational_addr(street_name[:-2], pca_tuple, A)
        if street_name.endswith('镇') and len(street_name)>2:
            street_map.append_relational_addr(street_name[:-1], pca_tuple, A)
        if street_name.endswith('乡') and len(street_name)>2:
            street_map.append_relational_addr(street_name[:-1], pca_tuple, A)
        if street_name.endswith('路') and len(street_name)>2:
            street_map.append_relational_addr(street_name[:-1], pca_tuple, A)


def _fill_area_map(area_map: AddrMap, record_dict):
    area_name = record_dict['qu']
    pca_tuple = (record_dict['sheng'], record_dict['shi'], record_dict['qu'],record_dict['jie'])
    if area_name not in area_map.keys() and area_name!='':
        area_map.append_relational_addr(area_name, pca_tuple, A)
        # 处理市/区/县/乡/镇简写情况
        if area_name.endswith('市') and len(area_name)>2:
            area_map.append_relational_addr(area_name[:-1], pca_tuple, A)
        elif area_name.endswith('区')and len(area_name)>2:
            area_map.append_relational_addr(area_name[:-1], pca_tuple, A)
        elif area_name.endswith('县') and len(area_name)>2:
            area_map.append_relational_addr(area_name[:-1], pca_tuple, A)
        elif area_name.endswith('乡')and len(area_name)>2:
            area_map.append_relational_addr(area_name[:-1], pca_tuple, A)
        elif area_name.endswith('镇')and len(area_name)>2:
            area_map.append_relational_addr(area_name[:-1], pca_tuple, A)

def _fill_city_map(city_map: AddrMap, record_dict):
    city_name = record_dict['shi']
    pca_tuple = (record_dict['sheng'], record_dict['shi'], record_dict['qu'],record_dict['jie'])
    city_map.append_relational_addr(city_name, pca_tuple, C)
    # 处理市/县/地区的简写情况
    if city_name.endswith('市'):
        city_map.append_relational_addr(city_name[:-1], pca_tuple, C)
    elif city_name.endswith('县'):
        city_map.append_relational_addr(city_name[:-1], pca_tuple, C)
    elif city_name.endswith('地区'):
        city_map.append_relational_addr(city_name[:-2], pca_tuple, C)

    # 自治县/自治州
    elif city_name == '黔西南布依族苗族自治州':
        city_map.append_relational_addr('黔西南', pca_tuple, C)
    elif city_name == '克孜勒苏柯尔克孜自治州':
        city_map.append_relational_addr('克州', pca_tuple, C)
    elif city_name == '湘西土家族苗族自治州':
        city_map.append_relational_addr('湘西', pca_tuple, C)
    elif city_name == '黔南布依族苗族自治州':
        city_map.append_relational_addr('黔南', pca_tuple, C)
    elif city_name == '黔东南苗族侗族自治州':
        city_map.append_relational_addr('黔东南', pca_tuple, C)
    elif city_name == '红河哈尼族彝族自治州':
        city_map.append_relational_addr('红河', pca_tuple, C)
    elif city_name == '海西蒙古族藏族自治州':
        city_map.append_relational_addr('海西', pca_tuple, C)
    elif city_name == '恩施土家族苗族自治州':
        city_map.append_relational_addr('恩施', pca_tuple, C)
    elif city_name == '德宏傣族景颇族自治州':
        city_map.append_relational_addr('德宏', pca_tuple, C)
    elif city_name == '西双版纳傣族自治州':
        city_map.append_relational_addr('西双版纳', pca_tuple, C)
    elif city_name == '文山壮族苗族自治州':
        city_map.append_relational_addr('文山', pca_tuple, C)
    elif city_name == '琼中黎族苗族自治县':
        city_map.append_relational_addr('琼中', pca_tuple, C)
    elif city_name == '博尔塔拉蒙古自治州':
        city_map.append_relational_addr('博尔塔拉', pca_tuple, C)
    elif city_name == '保亭黎族苗族自治县':
        city_map.append_relational_addr('保亭', pca_tuple, C)
    elif city_name == '巴音郭楞蒙古自治州':
        city_map.append_relational_addr('巴音郭楞', pca_tuple, C)
    elif city_name == '阿坝藏族羌族自治州':
        city_map.append_relational_addr('阿坝', pca_tuple, C)
    elif city_name == '伊犁哈萨克自治州':
        city_map.append_relational_addr('伊犁', pca_tuple, C)
    elif city_name == '延边朝鲜族自治州':
        city_map.append_relational_addr('延边', pca_tuple, C)
    elif city_name == '怒江傈僳族自治州':
        city_map.append_relational_addr('怒江傈', pca_tuple, C)
    elif city_name == '玉树藏族自治州':
        city_map.append_relational_addr('玉树', pca_tuple, C)
    elif city_name == '陵水黎族自治县':
        city_map.append_relational_addr('陵水', pca_tuple, C)
    elif city_name == '临夏回族自治州':
        city_map.append_relational_addr('临夏', pca_tuple, C)
    elif city_name == '凉山彝族自治州':
        city_map.append_relational_addr('凉山', pca_tuple, C)
    elif city_name == '乐东黎族自治县':
        city_map.append_relational_addr('乐东', pca_tuple, C)
    elif city_name == '黄南藏族自治州':
        city_map.append_relational_addr('黄南', pca_tuple, C)
    elif city_name == '海南藏族自治州':
        city_map.append_relational_addr('海南', pca_tuple, C)
    elif city_name == '海北藏族自治州':
        city_map.append_relational_addr('海北', pca_tuple, C)
    elif city_name == '果洛藏族自治州':
        city_map.append_relational_addr('果洛', pca_tuple, C)
    elif city_name == '甘孜藏族自治州':
        city_map.append_relational_addr('甘孜', pca_tuple, C)
    elif city_name == '甘南藏族自治州':
        city_map.append_relational_addr('甘南', pca_tuple, C)
    elif city_name == '迪庆藏族自治州':
        city_map.append_relational_addr('迪庆', pca_tuple, C)
    elif city_name == '大理白族自治州':
        city_map.append_relational_addr('大理', pca_tuple, C)
    elif city_name == '楚雄彝族自治州':
        city_map.append_relational_addr('楚雄', pca_tuple, C)
    elif city_name == '昌江黎族自治县':
        city_map.append_relational_addr('昌江', pca_tuple, C)
    elif city_name == '昌吉回族自治州':
        city_map.append_relational_addr('昌吉', pca_tuple, C)
    elif city_name == '白沙黎族自治县':
        city_map.append_relational_addr('白沙', pca_tuple, C)
    elif city_name == '锡林郭勒盟':
        city_map.append_relational_addr('锡林郭勒', pca_tuple, C)

    # 特别行政区
    elif city_name == '香港特别行政区':
        city_map.append_relational_addr('香港', pca_tuple, C)
    elif city_name == '澳门特别行政区':
        city_map.append_relational_addr('澳门', pca_tuple, C)

def _fill_province_map(province_map, record_dict):
    sheng = record_dict['sheng']
    if sheng not in province_map:
        province_map[sheng] = sheng
        # 处理省的简写情况(普通省和直辖市)
        if sheng.endswith('省') or sheng.endswith('市'):
            province_map[sheng[:-1]] = sheng
        # 自治区
        elif sheng == '新疆维吾尔自治区':
            province_map['新疆'] = sheng
        elif sheng == '内蒙古自治区':
            province_map['内蒙古'] = sheng
        elif sheng == '广西壮族自治区':
            province_map['广西'] = sheng
            province_map['广西省'] = sheng
        elif sheng == '西藏自治区':
            province_map['西藏'] = sheng
        elif sheng == '宁夏回族自治区':
            province_map['宁夏'] = sheng
        # 特别行政区
        elif sheng == '香港特别行政区':
            province_map['香港'] = sheng
        elif sheng == '澳门特别行政区':
            province_map['澳门'] = sheng

province_map,city_map,area_map,street_map,province_area_map,province_street_map,latlng = _data_from_csv()



# 直辖市
munis = {'北京市', '天津市', '上海市', '重庆市'}


def is_munis(city_full_name):
    return city_full_name in munis


myumap = {
}


def transform(location_strs, umap=myumap, index=[],lookahead=15, pos_sensitive=False, open_warning=True):
    """
    将地址描述字符串转换以"省","市","区","街道"信息为列的DataFrame表格
    :param location_strs: 地址描述字符集合,可以是list, Series等任意可以进行for in循环的集合；比如:["徐汇区虹漕路461号58号楼5楼", "泉州市洛江区万安塘西工业区"]
    :param umap: 自定义的区级到市级的映射,主要用于解决区重名问题,如果定义的映射在模块中已经存在，则会覆盖模块中自带的映射
    :param index: 可以通过这个参数指定输出的DataFrame的index,默认情况下是range(len(data))
    :param lookahead: 最多允许向前看的字符的数量，默认值为8是为了能够发现"新疆维吾尔族自治区"这样的长地名，如果你的样本中都是短地名的话，可以考虑把这个数字调小一点以提高性能
    :param pos_sensitive: 如果为True则会多返回四列，分别提取出的省市区在字符串中的位置，如果字符串中不存在的话则显示-1
    :param open_warning: 是否打开umap警告, 默认打开
    :return: 一个Pandas的DataFrame类型的表格
    """
    #判断输入内容是否为可迭代对象
    from collections.abc import Iterable

    if not isinstance(location_strs, Iterable) or isinstance(location_strs,str):
        raise InputTypeNotSuportException('location_strs参数必须为可迭代的类型(比如list, Series等实现了__iter__方法的对象)')

    import pandas as pd
    result = pd.DataFrame(
        [_handle_one_record(addr, umap, lookahead, pos_sensitive, open_warning) for addr in location_strs],
        index=index) \
        if index else pd.DataFrame(
        [_handle_one_record(addr, umap,lookahead, pos_sensitive, open_warning) for addr in location_strs])


    # 这句的唯一作用是让列的顺序好看一些
    if pos_sensitive:
        return result.loc[:, ('省', '市', '区', '街','地址', '省_pos', '市_pos', '区_pos','街_pos')]
    else:
        return result.loc[:, ('省', '市', '区', '街')]


def _handle_one_record(addr, umap, lookahead, pos_sensitive, open_warning):
    """
    处理一条地址记录
    :param addr: 从输入集中取出一条地址记录
    :param umap:
    :param lookahead:
    :param pos_sensitive:
    :param open_warning:
    :return:
    """
    # 空记录
    if not isinstance(addr, str) or addr == '' or addr is None:
        empty = {'省': '', '市': '', '区': '','街':''}
        if pos_sensitive:
            empty['省_pos'] = -1
            empty['市_pos'] = -1
            empty['区_pos'] = -1
            empty['街_pos'] = -1
        return empty

    # 省/市/区县提取
    pca, addr = _full_text_extract(addr, lookahead)


    #缺失省/市/区填充，多个依据优先级高于单个依据
    _fill_area(pca,umap,open_warning)

    _fill_city(pca, umap, open_warning)

    _fill_province(pca)

    result = pca.propertys_dict(pos_sensitive)
    result["地址"] = addr

    return result


def _fill_province(pca):
    """
    填充省
    :param pca:
    :return:
    """
    if (not pca.province) and pca.city and (pca.city in city_map):
        pca.province = city_map.get_value(pca.city, P)


def _fill_area(pca, umap, open_warning):
    """
    填充区
    :param pca:
    :param umap:
    :param open_warning:
    :return:
    """

    if not pca.area:

        # 优先从 省,街道 映射
        if pca.street and pca.province:
            newKey = (pca.province, pca.street)
            if newKey in province_street_map and province_street_map.is_unique_value(newKey):
                pca.area = province_street_map.get_value(newKey, A)
                return

        # 从 街道 映射
        if pca.street:
            # 从umap中映射
            if umap.get(pca.street):
                pca.area = umap.get(pca.street)
                return
            if pca.street in street_map and street_map.is_unique_value(pca.street):
                pca.area = street_map.get_value(pca.street, A)
                return

        if open_warning:
            import logging
            logging.warning("%s 无法映射, 建议添加进umap中", pca.street)


def _fill_city(pca, umap, open_warning):
    """
    填充市
    :param pca:
    :param umap:
    :param open_warning:
    :return:
    """
    if not pca.city:
        # 从 省,区 映射
        if pca.area and pca.province:
            newKey = (pca.province, pca.area)
            if newKey in province_area_map and province_area_map.is_unique_value(newKey):
                pca.city = province_area_map.get_value(newKey, C)
                return

        # 从 区 映射
        if pca.area:
            # 从umap中映射
            if umap.get(pca.area):
                pca.city = umap.get(pca.area)
                return

            if pca.area in area_map and area_map.is_unique_value(pca.area):
                pca.city = area_map.get_value(pca.area, C)
                return

        if open_warning:
            import logging
            logging.warning("%s 无法映射, 建议添加进umap中", pca.area)


def _full_text_extract(addr, lookahead):
    """
    全文匹配进行提取省/市/区县
    :param addr:
    :param lookahead:
    :return:
    """
    result = Pca()

    truncate = 0

    def _set_pca(pca_property, pos, name, full_name):
        """

        :param pca_property: 'province', 'city' or 'area'
        :param pos:
        :param name:
        :param full_name:
        :return:
        """
        def _defer_set():
            if not getattr(result, pca_property):
                setattr(result, pca_property, full_name)
                setattr(result, pca_property + "_pos", pos)
                if is_munis(full_name):
                    setattr(result, "province_pos", pos)
                nonlocal truncate
                if pos == truncate:
                    truncate += len(name)
            return len(name)
        return _defer_set

    # i为起始位置
    i = 0
    while i < len(addr):
        # 用于设置pca属性的函数
        defer_fun = None
        # l为从起始位置开始的长度,从中提取出最长的地址
        for length in range(1, lookahead + 1):
            if i + length > len(addr):
                break
            word = addr[i:i + length]


            if word in province_map:
                defer_fun = _set_pca('province', i, word, province_map.get(word))
                continue
            elif word in city_map:
                defer_fun = _set_pca('city', i, word, city_map.get_full_name(word))
                continue
            elif word in area_map:
                defer_fun = _set_pca('area', i, word, area_map.get_full_name(word))
                continue
            elif word in street_map:
                defer_fun = _set_pca('street', i, word, street_map.get_full_name(word))
                continue

        if defer_fun:
            i += defer_fun()
        else:
            i += 1
    return result, addr[truncate:]



