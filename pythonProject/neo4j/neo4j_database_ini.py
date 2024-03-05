global MAIN_DATA, DATABASE_NAME, AUTH, URL
import neo4j_json_edit as nje


def MAIN_DATA_ini(file_path):
    global MAIN_DATA, DATABASE_NAME, URL
    """初始化全部数据库，注意：使用此函数会删除所有曾经存储的数据"""
    MAIN_DATA = {"URL": "bolt://localhost:7687", "默认用户": ("neo4j", "ai123hr456")}
    URL = "bolt://localhost:7687"
    nje.json_save(MAIN_DATA,file_path)


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

