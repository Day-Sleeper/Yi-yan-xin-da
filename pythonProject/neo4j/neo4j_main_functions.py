# -*- coding: utf-8 -*-
from typing import Optional
import neo4j_json_edit as nje

global main_data, database_name, auth, url


def main_data_ini(file_path):
    """用于初始化部分数据库，不会删除其他数据库的信息，但会清空这一数据库"""
    global main_data, database_name, auth, url
    main_data = {"url": "bolt://localhost:7687", "默认用户": ("neo4j", "ai123hr456")}
    url = "bolt://localhost:7687"
    nje.json_save(main_data, file_path)


def DATABASE_ini(database_name):
    """用于初始化部分数据库，不会删除其他数据库的信息，但会清空这一数据库"""
    point_data = {}
    relationship_data = {}
    classification_data = {"点数据": point_data, "边数据": relationship_data}
    main_data[database_name] = classification_data


def user_login(auth_id=None, auth_password=None, database_name=None):
    """处理用户登录的id和密码数据，可选择性接收输入"""
    global main_data, database_name, auth, url
    if auth_id is None:
        auth_id = input("您好，请登录您的个人数据账户\n账号(输入0为默认账户)：")
    if auth_id == "0" or auth_id is None:
        auth_id = "neo4j"
    if auth_password is None:
        auth_password = input("密码（若为默认账号请输入0）")
    if auth_password == "0" or auth_password is None:
        auth_password = "ai123hr456"
    if database_name is None:
        database_name = input("创建或读取您的数据库：")
    if database_name == "0" or database_name is None:
        database_name = "test"
    database_name = database_name
    auth = (auth_id, auth_password)
    if not (database_name in main_data):  # 如果没有此数据库则初始化数据库
        DATABASE_ini(database_name)
    url = "bolt://localhost:7687"
    auth = ("neo4j", "ai123hr456")


def change_operating_database(database_name):
    global main_data, database_name, auth, url
    database_name = database_name


def main_data_LOAD(file_path):
    global main_data
    """从已存储的主数据库中读取数据"""
    main_data = nje.json_load(file_path)


def main_data_SAVE(file_path):
    global main_data
    """将主数据库存储至本地"""
    main_data = nje.json_save(main_data, file_path)


def clear_all_data(driver):
    """
    调试使用：清除数据库内所有数据
    """
    driver.execute_query("match (n) detach delete n", database_="neo4j", )


def add_point(driver,
              name_call: str,
              point_name: str,
              main_label: str,
              attribute_dic: Optional[dict] = ''):
    """为neo4j数据库中初始化添加点，必要的数据有：neo4j驱动器，点的名称叫法，点的名称，点的主要分类主标签，可选的数据有：属性字典

       函数的基本原理是将输入的形参转换为标准的cypher语句并存储在独立的数据库之中
       Args:
           driver (driver): neo4j驱动程序，由语句： with GraphDatabase.driver(nmf.url, auth=nmf.auth) as driver生成
           name_call (str):点数据的名称指定方式
           point_name (str):点数据的名称
           main_label (str):点数据对象主要的分类标签
           attribute_dic (Optional[dict]):存储属性的字典

       """
    input_cypher = "MERGE (a:{main_label} {{ {name_call}: '{point_name}', {attribute_dic} }}) " \
        .format(main_label=main_label,
                name_call=name_call,
                point_name=point_name,
                attribute_dic=attribute_preprocess(attribute_dic))
    main_data[database_name]["点数据"][point_name] = {"主标签": main_label, "名称叫法": name_call, name_call: point_name}
    if type(attribute_dic) is dict:
        for key in attribute_dic.keys():
            main_data[database_name]["点数据"][point_name][key] = attribute_dic[key]
    driver.execute_query(input_cypher, database_="neo4j", )


def add_relationship(driver,
                     relationship_start: str,
                     relationship_end: str,
                     relationship_label: str,
                     attribute_dic: Optional[dict] = '') -> None:
    """为neo4j数据库中初始化添加数据关系，必要的数据有：neo4j驱动器，关系起始点，关系终止点，关系主标签，可选的数据有：属性字典

    函数的基本原理是将输入的形参转换为标准的cypher语句并存储在独立的数据库之中
    Args:
        driver (driver): neo4j驱动程序，由语句： with GraphDatabase.driver(nmf.url, auth=nmf.auth) as driver生成
        relationship_start (str):关系开始的点的名称
        relationship_end (str):关系结束的点的名称
        relationship_label (str):关系的名称或标签
        attribute_dic (Optional[dict]):存储属性的字典

    """
    relationship_name = relationship_label + '：' + relationship_start + "->" + relationship_end
    input_cypher = """MATCH (a {{{relationship_start_name_call}:'{relationship_start}'}}), (b {{{relationship_end_name_call}:'{relationship_end}'}})
    MERGE (a)-[r:{relationship_label} {{{attribute_dic}}}]->(b)""" \
        .format(relationship_start=relationship_start,
                relationship_end=relationship_end,
                relationship_start_name_call=main_data[database_name]["点数据"][relationship_start]["名称叫法"],
                relationship_end_name_call=main_data[database_name]["点数据"][relationship_end]["名称叫法"],
                relationship_label=relationship_label,
                attribute_dic=attribute_preprocess(attribute_dic))
    main_data[database_name]["边数据"][relationship_name] = \
        {"关系": relationship_start + "->" + relationship_end,
         "主标签": relationship_label}
    for key in attribute_dic.keys():
        main_data[database_name]["边数据"][relationship_name][key] = attribute_dic[key]
    driver.execute_query(input_cypher, database_="neo4j", )


def add_point_attribute(driver,
                        database_name,
                        point_name,
                        attribute_dic):
    if point_name in main_data[database_name]["点数据"]:
        for key in attribute_dic.keys():
            input_cypher = """MATCH (a {{{name_call}:'{point_name}'}})
                              SET a.{attribute_name} = '{attribute_value}' """ \
                .format(name_call=main_data[database_name]["点数据"][point_name]["名称叫法"],
                        point_name=point_name,
                        attribute_name=key,
                        attribute_value=attribute_dic[key])
            main_data[database_name]["点数据"][point_name][key] = attribute_dic[key]
            driver.execute_query(input_cypher, database_="neo4j", )


def add_relationship_attribute(driver,
                               database_name,
                               relationship_label,
                               relationship_start,
                               relationship_end,
                               attribute_dic):
    relationship_name = relationship_label + '：' + relationship_start + "->" + relationship_end
    if relationship_name in main_data[database_name]["边数据"]:
        for key in attribute_dic.keys():
            input_cypher = """MATCH (a {{{relationship_start_name_call}:'{relationship_start}'}})-[r:{relationship_label}]->(b {{{relationship_end_name_call}:'{relationship_end}'}})
                              SET r.{attribute_name} = '{attribute_value}'""" \
                .format(relationship_start=relationship_start,
                        relationship_end=relationship_end,
                        relationship_start_name_call=main_data[database_name]["点数据"][relationship_start]["名称叫法"],
                        relationship_end_name_call=main_data[database_name]["点数据"][relationship_end]["名称叫法"],
                        relationship_label=relationship_label,
                        attribute_name=key,
                        attribute_value=attribute_dic[key])
            main_data[database_name]["边数据"][relationship_name][key] = attribute_dic[key]
            driver.execute_query(input_cypher, database_="neo4j", )
    pass


def attribute_preprocess(attribute_dic: Optional[dict]) -> dict | str:
    """将python中常规的属性键值对转换为neo4j中cypher能接受的数据格式，将key值去掉单双引号来实现

        Args:
            attribute_dic (Optional[dict]| str): 可以为存储属性键值对的字典，若为字符串则不进行任何操作
        Returns:
            dict: 转换格式之后的字典
        """
    if type(attribute_dic) is dict:
        return ', '.join(f"{k}: '{v}'" for k, v in attribute_dic.items())
