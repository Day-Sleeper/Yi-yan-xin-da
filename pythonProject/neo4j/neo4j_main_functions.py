"""
所有点数据必须要包含至少一个属性为其名称/姓名/name等
"""
global MAIN_DATA, DATABASE_NAME, AUTH, URL
import neo4j_json_edit as nje


def MAIN_DATA_ini(file_path):
    global MAIN_DATA, DATABASE_NAME, URL
    """初始化全部数据库，注意：使用此函数会删除所有曾经存储的数据"""
    MAIN_DATA = {"URL": "bolt://localhost:7687", "默认用户": ("neo4j", "ai123hr456")}
    URL = "bolt://localhost:7687"
    nje.json_save(MAIN_DATA, file_path)


def DATABASE_ini(DATABASE_NAME):
    """用于初始化部分数据库，不会删除其他数据库的信息，但会清空这一数据库"""
    point_data = {}
    relationship_data = {}
    classification_data = {"点数据": point_data, "边数据": relationship_data}
    MAIN_DATA[DATABASE_NAME] = classification_data


def user_login(AUTH_id=None, AUTH_password=None):
    """处理用户登录的id和密码数据，可选择性接收输入"""
    global MAIN_DATA, DATABASE_NAME, AUTH, URL
    if AUTH_id is None:
        AUTH_id = input("您好，请登录您的个人数据账户\n账号(输入0为默认账户)：")
    if AUTH_id == "0" or AUTH_id is None:
        AUTH_id = "neo4j"
    if AUTH_password is None:
        AUTH_password = input("密码（若为默认账号请输入0）")
    if AUTH_password == "0" or AUTH_password is None:
        AUTH_password = "ai123hr456"
    DATABASE_NAME = input("创建或读取您的数据库：")
    AUTH = (AUTH_id, AUTH_password)
    if not (DATABASE_NAME in MAIN_DATA):  # 如果没有此数据库则初始化数据库
        DATABASE_ini(DATABASE_NAME)
    URL = "bolt://localhost:7687"
    AUTH = ("neo4j", "ai123hr456")


def MAIN_DATA_LOAD(file_path):
    global MAIN_DATA
    """从已存储的主数据库中读取数据"""
    MAIN_DATA = nje.json_load(file_path)


def MAIN_DATA_SAVE(file_path):
    global MAIN_DATA
    """将主数据库存储至本地"""
    MAIN_DATA = nje.json_save(MAIN_DATA, file_path)


def search_point(database_name, point_name):
    for key in MAIN_DATA[database_name]["点数据"][point_name].keys:
        pass


def clear_all_data(driver):
    """
    调试使用：清除数据库内所有数据
    """
    driver.execute_query("match (n) detach delete n", database_="neo4j", )


# def add_point(driver, database_name, name_call, point_name, main_label, attribute_name, attribute_value):
#     """需要指定neo4j驱动器，数据库名称，点名称的叫法，点的名称，点的主要分类标签，属性的名称和属性的值，"""
#     input_cypher = "MERGE (a:{main_label} {{ {name_call}: '{point_name}', {attribute_name}: '{attribute_value}' }}) " \
#         .format(main_label=main_label,
#                 name_call=name_call,
#                 point_name=point_name,
#                 attribute_name=attribute_name,
#                 attribute_value=attribute_value)
#     MAIN_DATA[database_name]["点数据"][point_name] = {"主标签": main_label, "名称叫法": name_call,
#                                                       name_call: point_name, attribute_name: attribute_value}
#     driver.execute_query(input_cypher, database_="neo4j", )

def add_point(driver, database_name, name_call, point_name, main_label, attribute_dic):
    """需要指定neo4j驱动器，数据库名称，点名称的叫法，点的名称，点的主要分类标签，属性的名称和属性的值，"""
    input_cypher = "MERGE (a:{main_label} {{ {name_call}: '{point_name}', {attribute_dic} }}) " \
        .format(main_label=main_label,
                name_call=name_call,
                point_name=point_name,
                attribute_dic=attribute_preprocess(attribute_dic))
    MAIN_DATA[database_name]["点数据"][point_name] = {"主标签": main_label, "名称叫法": name_call,
                                                      name_call: point_name}
    for key in attribute_dic.keys():
        MAIN_DATA[database_name]["点数据"][point_name][key] = attribute_dic[key]
    driver.execute_query(input_cypher, database_="neo4j", )


def add_relationship(driver,
                     database_name,
                     relationship_start,
                     relationship_end,
                     relationship_label,
                     attribute_dic='') -> None:
    """为neo4j数据库中初始化添加数据关系，必要的数据有：neo4j驱动器，数据库名称，关系起始点，关系终止点，关系主标签，可选的数据有属性字典

    函数的基本原理是将输入的形参转换为标准的cypher语句并存储在独立的数据库之中
    Args:
        driver (driver): neo4j驱动程序，由语句： with GraphDatabase.driver(nmf.URL, auth=nmf.AUTH) as driver生成
        database_name (str): 数据库的名称
        relationship_start (str)：关系开始的点的名称
        relationship_end (str)：关系结束的点的名称
        relationship_label (str):关系的名称或标签
        attribute_dic (optional[dict])：存储属性的字典

    """
    input_cypher = """MATCH (a:{relationship_start_main_label} {{{relationship_start_name_call}: '{relationship_start}'}}), (b:{relationship_end_main_label} {{{relationship_end_name_call}: '{relationship_end}'}})
    MERGE (a)-[r:{relationship_label} {{{attribute_dic}}}]->(b)""" \
        .format(relationship_start=relationship_start,
                relationship_end=relationship_end,
                relationship_start_main_label=MAIN_DATA[database_name]["点数据"][relationship_start]["主标签"],
                relationship_end_main_label=MAIN_DATA[database_name]["点数据"][relationship_end]["主标签"],
                relationship_start_name_call=MAIN_DATA[database_name]["点数据"][relationship_start]["名称叫法"],
                relationship_end_name_call=MAIN_DATA[database_name]["点数据"][relationship_end]["名称叫法"],
                relationship_label=relationship_label,
                attribute_dic=attribute_preprocess(attribute_dic))
    print(input_cypher)
    MAIN_DATA[database_name]["边数据"][relationship_label + '：' + relationship_start + "->" + relationship_end] = \
        {"关系": relationship_start + "->" + relationship_end,
         "主标签": relationship_label}
    for key in attribute_dic.keys():
        MAIN_DATA[database_name]["边数据"][relationship_label + '：' + relationship_start + "->" + relationship_end][
            key] = \
            attribute_dic[key]
    driver.execute_query(input_cypher, database_="neo4j", )


def add_attribute(driver, database_name, point_name, attribute_name, attribute_value):
    if point_name in MAIN_DATA[database_name]["点数据"]:
        input_cypher = """MATCH (a{{{name_call}:'{point_name}'}})
                          SET a.{attribute_name} = '{attribute_value}' 
                        """ \
            .format(name_call=MAIN_DATA[database_name]["点数据"][point_name]["名称叫法"],
                    point_name=point_name,
                    attribute_name=attribute_name,
                    attribute_value=attribute_value)
        MAIN_DATA[database_name]["点数据"][point_name][attribute_name] = attribute_value
        driver.execute_query(input_cypher, database_="neo4j", )


def add_relationship_attribute(driver, database_name, point_name, attribute_name, attribute_value):
    pass


def attribute_preprocess(attribute_dic: dict | str) -> dict | str:
    """将python中常规的属性键值对转换为neo4j中cypher能接受的数据格式，将key值去掉单双引号来实现

        Args:
            attribute_dic (dict| str): 可以为存储属性键值对的字典，若为字符串则不进行任何操作
        Returns:
            dict: 转换格式之后的字典
        """
    if type(attribute_dic) is dict:
        attribute_dic = ', '.join(f"{k}: '{v}'" for k, v in attribute_dic.items())
    return attribute_dic
